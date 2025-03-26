"""
Database manager module for HyperXQL.
Handles database connections and query execution.
"""

import logging
import re
from typing import Dict, Any, List, Optional, Union, Tuple
from pathlib import Path
import sqlite3
from contextlib import contextmanager

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

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
                db_path = Path(db_config.get("database", "hyperxql.db")).expanduser().resolve()
                # Create parent directory if it doesn't exist
                db_path.parent.mkdir(parents=True, exist_ok=True)
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
    
    def execute_sql(self, sql: str) -> Dict[str, Any]:
        """
        Execute SQL query and return results.
        
        Args:
            sql: SQL query to execute
            
        Returns:
            Dictionary with query results
        """
        # Validate SQL query
        if not sql or not sql.strip():
            raise DatabaseError("Empty SQL query")
        
        # Determine query type
        query_type = self._determine_query_type(sql)
        
        try:
            with self.get_connection() as conn:
                # Execute the query
                result = conn.execute(text(sql))
                
                # For SELECT queries, fetch and return rows
                if query_type == "select":
                    columns = result.keys()
                    rows = result.fetchall()
                    
                    return {
                        "success": True,
                        "query_type": query_type,
                        "columns": columns,
                        "rows": rows,
                        "row_count": len(rows)
                    }
                
                # For other query types
                else:
                    # Get affected row count for DML statements
                    row_count = result.rowcount if hasattr(result, "rowcount") else 0
                    
                    # Special handling for CREATE TABLE - we want to return schema info
                    if query_type == "create_table":
                        table_name = self._extract_table_name(sql, "create")
                        message = f"Table '{table_name}' created successfully."
                    # UPDATE/DELETE/INSERT message
                    elif query_type in ["update", "delete", "insert"]:
                        message = f"{row_count} row(s) affected."
                    # Other DDL statements
                    else:
                        message = "Operation completed successfully."
                    
                    return {
                        "success": True,
                        "query_type": query_type,
                        "message": message,
                        "row_count": row_count
                    }
                
        except SQLAlchemyError as e:
            logger.exception("SQL execution error")
            raise DatabaseError(f"SQL execution error: {str(e)}")
        except Exception as e:
            logger.exception("Unexpected error executing SQL")
            raise DatabaseError(f"Error executing SQL: {str(e)}")
    
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
