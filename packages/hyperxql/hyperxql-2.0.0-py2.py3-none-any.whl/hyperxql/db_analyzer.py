"""
Database analyzer module for enhanced schema detection and relationship mapping.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
import sqlalchemy as sa
from sqlalchemy import inspect, MetaData, Table, ForeignKey
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.sql import select, func

try:
    import pandas as pd
except ImportError:
    logging.warning("pandas not installed. Some DatabaseAnalyzer functionality will be limited.")
    pd = None

logger = logging.getLogger(__name__)

class DatabaseAnalyzer:
    """Analyzer for extracting comprehensive database structure information."""
    
    def __init__(self, engine: Engine):
        """Initialize with SQLAlchemy engine."""
        self.engine = engine
        self.metadata = MetaData()
        self.cache = {}
        
        # Check pandas availability
        self._pandas_available = pd is not None
        if not self._pandas_available:
            logger.warning("pandas not available - some advanced analytics features will be disabled.")
        
    def get_full_database_info(self, refresh: bool = False) -> Dict[str, Any]:
        """
        Extract comprehensive database information including relationships and statistics.
        
        Args:
            refresh: Force refresh the schema cache
            
        Returns:
            Dictionary with complete database information
        """
        if not refresh and 'full_schema' in self.cache:
            return self.cache['full_schema']
            
        inspector = inspect(self.engine)
        db_type = self.engine.name
        
        tables = []
        relationships = []
        
        # First pass: collect all tables
        for table_name in inspector.get_table_names():
            try:
                # Get basic table info
                columns = []
                primary_keys = inspector.get_pk_constraint(table_name).get('constrained_columns', [])
                foreign_keys = inspector.get_foreign_keys(table_name)
                indices = inspector.get_indexes(table_name)
                
                # Get column details
                for column in inspector.get_columns(table_name):
                    col_info = {
                        'name': column['name'],
                        'type': str(column['type']),
                        'is_nullable': column.get('nullable', True),
                        'is_primary_key': column['name'] in primary_keys,
                        'default': str(column.get('default', 'NULL')),
                    }
                    columns.append(col_info)
                
                # Get table statistics
                row_count = self._get_table_row_count(table_name)
                
                # Create table info
                table_info = {
                    'name': table_name,
                    'columns': columns,
                    'row_count': row_count,
                    'has_primary_key': len(primary_keys) > 0,
                    'primary_keys': primary_keys,
                    'indices': [{'name': idx.get('name'), 'columns': idx.get('column_names')} for idx in indices],
                }
                
                # Get sample data (up to 5 rows)
                sample_data = self._get_sample_data(table_name)
                if sample_data:
                    table_info['sample_data'] = sample_data
                
                tables.append(table_info)
                
                # Collect foreign key relationships
                for fk in foreign_keys:
                    relationships.append({
                        'source_table': table_name,
                        'source_columns': fk['constrained_columns'],
                        'target_table': fk['referred_table'],
                        'target_columns': fk['referred_columns'],
                        'name': fk.get('name')
                    })
                    
                    # Mark columns with foreign key references
                    for col in columns:
                        if col['name'] in fk['constrained_columns']:
                            col['is_foreign_key'] = True
                            col['references'] = f"{fk['referred_table']}({','.join(fk['referred_columns'])})"
            
            except Exception as e:
                logger.warning(f"Error analyzing table {table_name}: {str(e)}")
        
        # Second pass: detect potential implicit relationships (naming conventions)
        implicit_relationships = self._detect_implicit_relationships(tables)
        
        # Detect common patterns in data
        data_patterns = self._detect_data_patterns(tables)
        
        # Final schema
        full_schema = {
            'db_type': db_type,
            'tables': tables,
            'explicit_relationships': relationships,
            'implicit_relationships': implicit_relationships,
            'data_patterns': data_patterns
        }
        
        # Cache the result
        self.cache['full_schema'] = full_schema
        
        return full_schema
    
    def _get_table_row_count(self, table_name: str) -> int:
        """Get approximate row count for a table."""
        try:
            with self.engine.connect() as conn:
                query = f"SELECT COUNT(*) FROM {table_name}"
                result = conn.execute(sa.text(query))
                count = result.scalar()
                return count
        except Exception as e:
            logger.warning(f"Could not get row count for {table_name}: {str(e)}")
            return -1
    
    def _get_sample_data(self, table_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get sample data from a table."""
        try:
            table = sa.Table(table_name, self.metadata, autoload_with=self.engine)
            query = select(table).limit(limit)
            
            with self.engine.connect() as conn:
                result = conn.execute(query)
                columns = result.keys()
                sample_data = []
                
                for row in result:
                    row_dict = {}
                    for idx, col in enumerate(columns):
                        # Convert to string to avoid serialization issues
                        row_dict[col] = str(row[idx]) if row[idx] is not None else "NULL"
                    sample_data.append(row_dict)
                
                return sample_data
        except Exception as e:
            logger.warning(f"Could not get sample data for {table_name}: {str(e)}")
            return []
    
    def _detect_implicit_relationships(self, tables: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect potential implicit relationships based on naming conventions."""
        implicit_relationships = []
        table_by_name = {table['name']: table for table in tables}
        
        for table_name, table_info in table_by_name.items():
            for column in table_info['columns']:
                col_name = column['name'].lower()
                
                # Look for columns like 'user_id', 'order_id' etc.
                if col_name.endswith('_id') and not column.get('is_foreign_key', False):
                    potential_table = col_name[:-3]  # remove '_id'
                    
                    # Check if there's a table with this name (singular or plural)
                    if potential_table in table_by_name:
                        target_table = potential_table
                    elif f"{potential_table}s" in table_by_name:  # Check plural
                        target_table = f"{potential_table}s"
                    else:
                        continue
                    
                    # Check if the target table has a primary key named 'id'
                    target_pk = None
                    for col in table_by_name[target_table]['columns']:
                        if col['is_primary_key'] and col['name'].lower() == 'id':
                            target_pk = 'id'
                            break
                    
                    if target_pk:
                        implicit_relationships.append({
                            'source_table': table_name,
                            'source_column': column['name'],
                            'target_table': target_table,
                            'target_column': target_pk,
                            'confidence': 'medium',
                            'type': 'implicit'
                        })
        
        return implicit_relationships
    
    def _detect_data_patterns(self, tables: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect common patterns in the data to inform query generation."""
        patterns = {}
        
        for table in tables:
            table_name = table['name']
            # Skip tables with no data
            if table.get('row_count', 0) <= 0:
                continue
                
            # Check if there are timestamp/datetime columns for time-series data
            time_columns = []
            for col in table['columns']:
                col_type = col['type'].lower()
                if any(time_type in col_type for time_type in ['timestamp', 'datetime', 'date']):
                    time_columns.append(col['name'])
            
            if time_columns:
                if 'time_series_tables' not in patterns:
                    patterns['time_series_tables'] = []
                patterns['time_series_tables'].append({
                    'table': table_name,
                    'time_columns': time_columns
                })
                
            # Identify potential lookup tables (small tables with few columns)
            if (
                table.get('row_count', float('inf')) < 100 and
                len(table['columns']) <= 3 and
                any(col.get('is_primary_key', False) for col in table['columns'])
            ):
                if 'lookup_tables' not in patterns:
                    patterns['lookup_tables'] = []
                patterns['lookup_tables'].append(table_name)
        
        return patterns
    
    def analyze_query_patterns(self, connection_string: str) -> Dict[str, Any]:
        """
        Analyze database query patterns using the system catalog (if available).
        This is more advanced and DB-specific.
        """
        if 'postgresql' in self.engine.name:
            try:
                # For PostgreSQL, analyze from pg_stat_statements
                query = """
                SELECT query, calls, total_time, mean_time, rows
                FROM pg_stat_statements
                ORDER BY total_time DESC
                LIMIT 20
                """
                
                with self.engine.connect() as conn:
                    result = conn.execute(sa.text(query))
                    return {
                        'common_queries': [dict(row) for row in result]
                    }
            except Exception as e:
                logger.warning(f"Could not analyze query patterns: {str(e)}")
        
        return {}
