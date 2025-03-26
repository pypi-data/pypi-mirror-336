"""
Database manager module for HyperXQL.
Handles database connections and query execution.
"""

import logging
import re
import time
from typing import Dict, Any, List, Optional, Union, Tuple
from pathlib import Path
import sqlite3
from contextlib import contextmanager

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError, ResourceClosedError

from .config import Config
from .exceptions import DatabaseError

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manager for database connections and operations."""
    
    def __init__(self, config: Config):
        """Initialize the database manager with configuration."""
        self.config = config
        self.engine = self._create_engine()
    
    def _create_engine(self):
        """Create SQLAlchemy engine from configuration."""
        db_config = self.config.db_config
        
        if not db_config:
            raise DatabaseError("Database not configured. Run 'hyperxql init' to configure.")
        
        try:
            db_type = db_config.get("db_type")
            
            if db_type == "sqlite":
                # Handle database path
                db_path_str = db_config.get("database", "hyperxql.db")
                
                # Convert to Path object if it's a string
                db_path = Path(db_path_str).expanduser().resolve()
                
                # Ensure parent directory exists
                db_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Log the absolute path for debugging
                logger.info(f"Using SQLite database at: {db_path}")
                
                # Create URI connection string with correct path format
                conn_str = f"sqlite:///{db_path}"
                
            elif db_type == "postgresql":
                # Check if connection string is provided directly
                if "connection_string" in db_config:
                    conn_str = db_config["connection_string"]
                else:
                    host = db_config.get("host", "localhost")
                    port = db_config.get("port", "5432")
                    database = db_config.get("database", "postgres")
                    user = db_config.get("user", "postgres")
                    password = db_config.get("password", "")
                    
                    conn_str = f"postgresql://{user}:{password}@{host}:{port}/{database}"
                
            elif db_type == "mysql":
                host = db_config.get("host", "localhost")
                port = db_config.get("port", "3306")
                database = db_config.get("database", "mysql")
                user = db_config.get("user", "root")
                password = db_config.get("password", "")
                
                conn_str = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
                
            else:
                raise DatabaseError(f"Unsupported database type: {db_type}")
            
            # Create engine with connection pooling
            return create_engine(
                conn_str,
                pool_pre_ping=True,
                pool_recycle=300,
                connect_args={"connect_timeout": 10} if db_type != "sqlite" else {}
            )
            
        except Exception as e:
            logger.exception("Error creating database engine")
            raise DatabaseError(f"Failed to create database connection: {str(e)}")
    
    @contextmanager
    def get_connection(self):
        """Get a database connection as a context manager."""
        connection = None
        try:
            connection = self.engine.connect()
            yield connection
        except SQLAlchemyError as e:
            logger.exception("Database connection error")
            raise DatabaseError(f"Database connection error: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def is_connected(self):
        """Check if database connection is established and working.
        
        Returns:
            bool: True if connected, False otherwise
        """
        if not hasattr(self, 'engine') or self.engine is None:
            return False
        
        try:
            # Try a simple query to verify connection
            with self.get_connection() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.debug(f"Database connection check failed: {str(e)}")
            return False

    def execute_sql(self, sql):
        """Execute SQL query and return results.
        
        Args:
            sql (str): SQL query to execute
            
        Returns:
            dict: Query results with success/error status
        """
        start_time = time.time()
        
        try:
            # Split multiple statements (for SQLite compatibility)
            statements = [stmt.strip() for stmt in sql.split(';') if stmt.strip()]
            
            results = []
            affected_rows_total = 0
            
            with self.get_connection() as conn:
                for statement in statements:
                    if not statement:
                        continue
                        
                    stmt_result = {
                        "statement": statement,
                        "columns": [],
                        "data": [],
                        "affected_rows": None,
                        "success": True,
                        "error": None
                    }
                    
                    try:
                        # Execute the statement
                        result = conn.execute(text(statement))
                        
                        # Get column names if available (safely)
                        try:
                            if result.returns_rows:
                                stmt_result["columns"] = result.keys()
                                # Fetch data for SELECT statements
                                stmt_result["data"] = [list(row) for row in result.fetchall()]
                        except ResourceClosedError:
                            # This is normal for non-SELECT statements (CREATE, INSERT, etc.)
                            pass
                        
                        # Get affected rows count
                        affected_rows = result.rowcount if result.rowcount >= 0 else None
                        stmt_result["affected_rows"] = affected_rows
                        
                        if affected_rows:
                            affected_rows_total += affected_rows
                            
                    except Exception as stmt_error:
                        # Record the error but continue with other statements
                        stmt_result["success"] = False
                        stmt_result["error"] = str(stmt_error)
                        logger.error(f"Error executing statement: {stmt_error}")
                    
                    results.append(stmt_result)
            
            # Combine results for return
            execution_time = time.time() - start_time
            
            if len(results) == 1:
                stmt_result = results[0]
                return {
                    "success": stmt_result["success"],
                    "error": stmt_result["error"],
                    "columns": stmt_result["columns"],
                    "data": stmt_result["data"],
                    "affected_rows": stmt_result["affected_rows"],
                    "execution_time": execution_time
                }
            else:
                # Check if any statement failed
                any_failed = any(not result["success"] for result in results)
                all_errors = [r["error"] for r in results if r["error"]]
                
                return {
                    "success": not any_failed,
                    "error": "; ".join(all_errors) if all_errors else None,
                    "multi_statements": True,
                    "results": results,
                    "affected_rows": affected_rows_total,
                    "execution_time": execution_time
                }
                
        except Exception as e:
            logger.error("Unexpected error executing SQL", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "execution_time": time.time() - start_time
            }

    def _determine_query_type(self, sql: str) -> str:
        """
        Determine the type of SQL query.
        
        Args:
            sql: SQL query string
            
        Returns:
            Query type string
        """
        sql_lower = sql.lower().strip()
        
        if sql_lower.startswith("select"):
            return "select"
        elif sql_lower.startswith("insert"):
            return "insert"
        elif sql_lower.startswith("update"):
            return "update"
        elif sql_lower.startswith("delete"):
            return "delete"
        elif sql_lower.startswith("create table"):
            return "create_table"
        elif sql_lower.startswith("create database") or sql_lower.startswith("create schema"):
            return "create_database"
        elif sql_lower.startswith("alter table"):
            return "alter_table"
        elif sql_lower.startswith("drop table"):
            return "drop_table"
        else:
            return "other"
    
    def _extract_table_name(self, sql: str, operation: str) -> str:
        """
        Extract table name from SQL statement.
        
        Args:
            sql: SQL query string
            operation: Operation type (create, alter, etc.)
            
        Returns:
            Table name or empty string if not found
        """
        sql_lower = sql.lower()
        
        if operation == "create":
            # Match pattern: CREATE TABLE [IF NOT EXISTS] table_name
            pattern = r"create\s+table\s+(?:if\s+not\s+exists\s+)?[\[\'\"\`]?([a-zA-Z0-9_]+)[\]\'\"\`]?"
        elif operation == "alter":
            # Match pattern: ALTER TABLE table_name
            pattern = r"alter\s+table\s+[\[\'\"\`]?([a-zA-Z0-9_]+)[\]\'\"\`]?"
        elif operation == "drop":
            # Match pattern: DROP TABLE [IF EXISTS] table_name
            pattern = r"drop\s+table\s+(?:if\s+exists\s+)?[\[\'\"\`]?([a-zA-Z0-9_]+)[\]\'\"\`]?"
        else:
            return ""
        
        match = re.search(pattern, sql_lower)
        if match:
            return match.group(1)
        return ""
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Get information about the current database.
        
        Returns:
            Dictionary with database information
        """
        try:
            db_type = self.config.db_config.get("db_type", "")
            db_name = self.config.db_config.get("database", "")
            
            tables = []
            
            with self.get_connection() as conn:
                inspector = inspect(self.engine)
                table_names = inspector.get_table_names()
                
                for table_name in table_names:
                    columns = []
                    for column in inspector.get_columns(table_name):
                        column_info = {
                            "name": column["name"],
                            "type": str(column["type"]),
                            "is_nullable": column.get("nullable", True)
                        }
                        columns.append(column_info)
                    
                    # Get primary keys
                    primary_keys = inspector.get_pk_constraint(table_name).get("constrained_columns", [])
                    for col in columns:
                        if col["name"] in primary_keys:
                            col["is_primary_key"] = True
                    
                    # Get foreign keys
                    foreign_keys = inspector.get_foreign_keys(table_name)
                    for fk in foreign_keys:
                        for col_name in fk.get("constrained_columns", []):
                            for col in columns:
                                if col["name"] == col_name:
                                    col["is_foreign_key"] = True
                                    col["references"] = f"{fk.get('referred_table')}.{fk.get('referred_columns')[0]}"
                    
                    table_info = {
                        "name": table_name,
                        "columns": columns
                    }
                    tables.append(table_info)
            
            return {
                "db_type": db_type,
                "db_name": db_name,
                "tables": tables
            }
            
        except Exception as e:
            logger.exception("Error getting database information")
            raise DatabaseError(f"Failed to get database information: {str(e)}")
