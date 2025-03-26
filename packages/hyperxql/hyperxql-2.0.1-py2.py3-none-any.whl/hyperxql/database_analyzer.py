import logging
from sqlalchemy import inspect, text
import json
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class DatabaseAnalyzer:
    """
    A class to analyze database structure and performance.
    """
    
    def __init__(self, connection=None):
        """
        Initialize the database analyzer.
        
        Args:
            connection: Database connection object
        """
        self.connection = connection
        self._schema_cache = None
    
    def get_full_database_info(self, refresh=False):
        """
        Get complete information about the database schema.
        
        Args:
            refresh (bool): Whether to refresh cached schema info
            
        Returns:
            dict: Complete database schema information
        """
        if self._schema_cache is not None and not refresh:
            return self._schema_cache
            
        try:
            inspector = inspect(self.connection)
            
            # Get database type
            db_type = self.connection.dialect.name if self.connection else "unknown"
            
            # Get list of all tables
            tables = []
            for table_name in inspector.get_table_names():
                table_info = {
                    "name": table_name,
                    "columns": [],
                    "primary_key": [],
                    "indexes": [],
                    "foreign_keys": []
                }
                
                # Get columns
                for column in inspector.get_columns(table_name):
                    col_info = {
                        "name": column["name"],
                        "type": str(column["type"]),
                        "nullable": column.get("nullable", True),
                        "default": str(column.get("default", "")) if column.get("default") is not None else None,
                        "autoincrement": column.get("autoincrement", False)
                    }
                    table_info["columns"].append(col_info)
                
                # Get primary key
                pk = inspector.get_pk_constraint(table_name)
                if pk and "constrained_columns" in pk:
                    table_info["primary_key"] = pk["constrained_columns"]
                
                # Get indexes
                for index in inspector.get_indexes(table_name):
                    index_info = {
                        "name": index["name"],
                        "columns": index["column_names"],
                        "unique": index["unique"]
                    }
                    table_info["indexes"].append(index_info)
                
                # Get foreign keys
                for fk in inspector.get_foreign_keys(table_name):
                    fk_info = {
                        "name": fk.get("name"),
                        "columns": fk["constrained_columns"],
                        "referenced_table": fk["referred_table"],
                        "referenced_columns": fk["referred_columns"]
                    }
                    table_info["foreign_keys"].append(fk_info)
                
                tables.append(table_info)
            
            # Extract relationships
            explicit_relationships = []
            for table in tables:
                for fk in table["foreign_keys"]:
                    rel = {
                        "from_table": table["name"],
                        "from_columns": fk["columns"],
                        "to_table": fk["referenced_table"],
                        "to_columns": fk["referenced_columns"],
                        "type": "foreign_key"
                    }
                    explicit_relationships.append(rel)
            
            # Look for implicit relationships (columns with similar names)
            implicit_relationships = []
            
            # Build complete schema
            schema = {
                "db_type": db_type,
                "tables": tables,
                "explicit_relationships": explicit_relationships,
                "implicit_relationships": implicit_relationships
            }
            
            # Cache the result
            self._schema_cache = schema
            return schema
            
        except Exception as e:
            logger.error(f"Error analyzing database: {str(e)}", exc_info=True)
            return {"error": str(e)}
    
    def analyze_database(self, database_name):
        """
        Analyze the structure of a database.
        
        Args:
            database_name: Name of the database to analyze
            
        Returns:
            dict: Analysis results
        """
        # This method now delegates to get_full_database_info
        return self.get_full_database_info(refresh=True)
    
    def _get_tables(self):
        """
        Get list of tables in the database.
        
        Returns:
            list: Table information
        """
        if not self.connection:
            return []
            
        try:
            inspector = inspect(self.connection)
            return inspector.get_table_names()
        except Exception as e:
            logger.error(f"Error getting tables: {str(e)}")
            return []
    
    def _get_indices(self):
        """
        Get list of indices in the database.
        
        Returns:
            list: Index information
        """
        if not self.connection:
            return []
            
        try:
            inspector = inspect(self.connection)
            indices = []
            
            for table_name in inspector.get_table_names():
                for index in inspector.get_indexes(table_name):
                    index["table_name"] = table_name
                    indices.append(index)
                    
            return indices
        except Exception as e:
            logger.error(f"Error getting indices: {str(e)}")
            return []
    
    def _get_database_size(self):
        """
        Get size information about the database.
        
        Returns:
            dict: Size information
        """
        # Database size query is highly database-specific
        # Here's a generic implementation that might work for some systems
        if not self.connection:
            return {"size_mb": 0}
            
        try:
            # SQLite specific
            if self.connection.dialect.name == 'sqlite':
                return {"size_mb": 0, "note": "Size estimation not supported for SQLite"}
                
            # PostgreSQL specific
            elif self.connection.dialect.name == 'postgresql':
                with self.connection.connect() as conn:
                    result = conn.execute(text(
                        "SELECT pg_database_size(current_database())/1024/1024 as size_mb"
                    )).fetchone()
                    if result:
                        return {"size_mb": result[0]}
                        
            # MySQL/MariaDB specific
            elif self.connection.dialect.name in ('mysql', 'mariadb'):
                with self.connection.connect() as conn:
                    result = conn.execute(text(
                        "SELECT SUM(data_length + index_length)/1024/1024 as size_mb "
                        "FROM information_schema.tables"
                    )).fetchone()
                    if result:
                        return {"size_mb": result[0] or 0}
            
            # Default fallback
            return {"size_mb": 0, "note": "Size estimation not supported for this database type"}
            
        except Exception as e:
            logger.error(f"Error getting database size: {str(e)}")
            return {"size_mb": 0, "error": str(e)}
