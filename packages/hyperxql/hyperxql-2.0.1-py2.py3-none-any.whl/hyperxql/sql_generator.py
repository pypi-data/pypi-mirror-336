"""
SQL Generator module for HyperXQL.
Handles generation of SQL from natural language using LLM.
"""

import logging
import json
from typing import Dict, Any, Optional, Generator, Union
from dataclasses import dataclass

from .llm_client import LLMClient
from .exceptions import SQLGenerationError
from .db_analyzer import DatabaseAnalyzer

logger = logging.getLogger(__name__)

@dataclass
class SQLResponse:
    """Class for storing SQL generation response."""
    sql: str
    explanation: str
    execute: bool
    display_format: str
    metadata: Dict[str, Any]
    provider: str
    model: str
    db_info: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "sql": self.sql,
            "explanation": self.explanation,
            "execute": self.execute,
            "display_format": self.display_format,
            "metadata": self.metadata,
            "provider": self.provider,
            "model": self.model
        }

class SQLGenerator:
    """Generator for SQL from natural language."""
    
    def __init__(self, llm_client: LLMClient, db_analyzer: Optional[DatabaseAnalyzer] = None):
        """
        Initialize the SQL generator with an LLM client and optional DB analyzer.
        
        Args:
            llm_client: LLMClient instance
            db_analyzer: Optional DatabaseAnalyzer instance
        """
        self.llm_client = llm_client
        self.db_analyzer = db_analyzer
        self.sql_cache = {}  # Cache for frequently used queries
    
    def generate_sql(self, query: str, db_info: Optional[Dict[str, Any]] = None) -> SQLResponse:
        """
        Generate SQL from natural language.
        
        Args:
            query: Natural language query
            db_info: Optional database schema information
            
        Returns:
            SQLResponse object
        """
        # Generate a cache key
        cache_key = f"{query}_{hash(str(db_info)) if db_info else 'no_db_info'}"
        
        # Check if we have a cached response
        if (cache_key in self.sql_cache):
            logger.info(f"Using cached SQL response for query: {query}")
            return self.sql_cache[cache_key]
        
        try:
            # If we have a db_analyzer but no db_info, try to get full schema information
            if self.db_analyzer is not None and db_info is None:
                logger.info("No DB info provided, using DatabaseAnalyzer to get schema")
                try:
                    db_info = self.db_analyzer.get_full_database_info()
                    logger.info(f"Retrieved schema for {len(db_info.get('tables', []))} tables")
                except Exception as e:
                    logger.warning(f"Error getting database schema: {str(e)}")
            
            # Generate SQL using LLM
            response = self.llm_client.generate_sql_from_nl(query, db_info)
            
            # Extract fields from the response
            sql = response.get("sql", "")
            explanation = response.get("explanation", "")
            execute = response.get("execute", True)
            display_format = response.get("display_format", "table")
            metadata = response.get("metadata", {})
            provider = response.get("provider", "")
            model = response.get("model", "")
            
            # Validate SQL
            if not sql or not sql.strip():
                raise SQLGenerationError("No SQL generated. Please try rephrasing your query.")
            
            # Log the generated SQL (without sensitive information)
            logger.info(f"Generated SQL: {sql}")
            
            # Create SQL response
            sql_response = SQLResponse(
                sql=sql,
                explanation=explanation,
                execute=execute,
                display_format=display_format,
                metadata=metadata,
                provider=provider,
                model=model,
                db_info=db_info
            )
            
            # Cache the result if it's valid
            self.sql_cache[cache_key] = sql_response
            
            # Limit cache size
            if len(self.sql_cache) > 100:  # Limit to last 100 queries
                # Remove oldest item (simplified approach)
                self.sql_cache.pop(next(iter(self.sql_cache)))
            
            return sql_response
            
        except Exception as e:
            logger.exception("Error generating SQL")
            # Provide a more user-friendly error message
            error_msg = str(e)
            if "Service unavailable" in error_msg:
                error_msg = "Together AI service is temporarily unavailable. Trying alternative LLM providers or please try again later."
            elif "rate limit" in error_msg.lower():
                error_msg = "Rate limit exceeded. Please try again in a few moments."
            elif "api key" in error_msg.lower():
                error_msg = "API key issue. Please check your configuration."
            elif "model" in error_msg.lower() and "not found" in error_msg.lower():
                error_msg = "The specified model was not found. Please check your model configuration."
            
            raise SQLGenerationError(f"Failed to generate SQL: {error_msg}")
    
    def validate_sql(self, sql: str, db_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate generated SQL against database schema.
        
        Args:
            sql: SQL query to validate
            db_info: Database schema information
            
        Returns:
            Dictionary with validation results
        """
        if not self.db_analyzer:
            return {"valid": None, "reason": "No database analyzer available for validation"}
        
        # Use LLM to validate SQL against schema
        system_prompt = """You are a SQL validation expert. Analyze the provided SQL query
against the database schema and identify potential issues, syntax errors, or schema mismatches.
Do not execute the query, just analyze it statically."""
        
        # Build prompt with DB schema and SQL
        schema_str = json.dumps(db_info, indent=2) if db_info else "No schema available"
        user_prompt = f"""
Database Schema:
{schema_str}

SQL Query to Validate:
{sql}

Analyze this SQL for:
1. Syntax errors
2. References to non-existent tables or columns
3. Type mismatches
4. JOIN conditions correctness
5. Other potential issues

Return your analysis in this format:
{{
    "valid": true/false,
    "errors": ["error1", "error2"],
    "warnings": ["warning1", "warning2"],
    "suggestions": ["suggestion1", "suggestion2"]
}}
"""
        
        try:
            response = self.llm_client.generate_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.1,
                response_format={"type": "json_object"} if self.llm_client.provider == "openai" else None
            )
            
            # Extract the validation result
            completion = response.get("completion", "")
            if isinstance(completion, dict):
                result = completion
            else:
                # Try to parse as JSON
                try:
                    result = json.loads(completion)
                except json.JSONDecodeError:
                    result = {
                        "valid": False,
                        "errors": ["Failed to parse validation result"],
                        "warnings": [],
                        "suggestions": ["Try simplifying your query"]
                    }
            
            return result
            
        except Exception as e:
            logger.exception(f"Error validating SQL: {str(e)}")
            return {
                "valid": False,
                "errors": [f"Validation failed: {str(e)}"],
                "warnings": [],
                "suggestions": []
            }

    def validate_sql(self, sql: str, db_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate SQL against database schema
        
        Args:
            sql: SQL query to validate
            db_info: Database schema information
            
        Returns:
            Dict with validation results
        """
        if not db_info or not db_info.get('tables'):
            return {
                "valid": None,
                "message": "No database schema available for validation"
            }
        
        # Extract table names from database info
        available_tables = {table['name'].lower(): table for table in db_info.get('tables', [])}
        
        # Basic validation for table existence
        errors = []
        warnings = []
        suggestions = []
        
        # Check for UNION operations with tables that have different structures
        if " union " in sql.lower() or " union all " in sql.lower():
            tables_in_union = []
            
            # Extract table names from UNION query parts
            parts = re.split(r'\s+union\s+all\s+|\s+union\s+', sql.lower())
            for part in parts:
                # Extract table name from each SELECT part
                table_match = re.search(r'from\s+([a-z0-9_]+)', part)
                if table_match:
                    tables_in_union.append(table_match.group(1))
            
            # Check if tables in UNION have the same column count
            if len(tables_in_union) > 1:
                column_counts = {}
                
                for table_name in tables_in_union:
                    if table_name in available_tables:
                        column_counts[table_name] = len(available_tables[table_name].get('columns', []))
                    
                # If we have different column counts, that will cause a UNION error
                if len(set(column_counts.values())) > 1:
                    errors.append(
                        f"Tables in UNION have different column counts: {column_counts}. "
                        f"UNION requires all SELECT statements to have the same number of columns."
                    )
                    suggestions.append(
                        "Either select the same number of columns from each table or use individual queries instead."
                    )
        
        # Extract table references from SQL
        table_matches = re.finditer(r'from\s+([a-z0-9_]+)|join\s+([a-z0-9_]+)|into\s+([a-z0-9_]+)|update\s+([a-z0-9_]+)|insert\s+into\s+([a-z0-9_]+)|create\s+table\s+([a-z0-9_]+)|alter\s+table\s+([a-z0-9_]+)|drop\s+table\s+([a-z0-9_]+)', sql.lower())
        
        for match in table_matches:
            # Find the matched group (table name)
            table_name = next((group for group in match.groups() if group), None)
            
            if table_name and table_name not in available_tables:
                if 'create table' in sql.lower() and table_name in match.group(6):
                    # Creating a new table is fine
                    continue
                    
                # Table doesn't exist
                errors.append(f"Table '{table_name}' does not exist in the database")
                
                # Suggest similar table names if available
                similar_tables = [t for t in available_tables.keys() if len(set(t) & set(table_name)) > len(t) / 2]
                if similar_tables:
                    suggestions.append(f"Did you mean one of these tables: {', '.join(similar_tables)}?")
        
        # Check if we're querying for columns that don't exist
        column_matches = re.finditer(r'select\s+(?!.*from)(.+?)\s+from|where\s+([a-z0-9_]+)\.([a-z0-9_]+)|order\s+by\s+([a-z0-9_]+)|group\s+by\s+([a-z0-9_]+)', sql.lower())
        
        # More validation logic here...
        
        # Return validation results
        is_valid = len(errors) == 0
        
        return {
            "valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions
        }
