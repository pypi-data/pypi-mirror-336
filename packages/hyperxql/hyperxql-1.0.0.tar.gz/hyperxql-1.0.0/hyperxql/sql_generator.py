"""
SQL Generator module for HyperXQL.
Handles generation of SQL from natural language using LLM.
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

from .llm_client import LLMClient
from .exceptions import SQLGenerationError

logger = logging.getLogger(__name__)

@dataclass
class SQLResponse:
    """Class for storing SQL generation response."""
    sql: str
    explanation: str
    execute: bool
    display_format: str
    metadata: Dict[str, Any]
    provider: str = ""
    model: str = ""

class SQLGenerator:
    """Generator for SQL from natural language."""
    
    def __init__(self, llm_client: LLMClient):
        """Initialize the SQL generator with an LLM client."""
        self.llm_client = llm_client
    
    def generate_sql(self, 
                   query: str, 
                   db_info: Optional[Dict[str, Any]] = None) -> SQLResponse:
        """
        Generate SQL from natural language query.
        
        Args:
            query: Natural language query
            db_info: Optional database schema information
            
        Returns:
            SQLResponse object with generated SQL and metadata
        """
        try:
            # Log the query (without sensitive information)
            logger.info(f"Generating SQL for query: {query}")
            
            # Call LLM to generate SQL
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
            
            return SQLResponse(
                sql=sql,
                explanation=explanation,
                execute=execute,
                display_format=display_format,
                metadata=metadata,
                provider=provider,
                model=model
            )
            
        except Exception as e:
            logger.exception("Error generating SQL")
            raise SQLGenerationError(f"Failed to generate SQL: {str(e)}")
