"""
Query optimizer module for improving generated SQL.
"""

import logging
import json
from typing import Dict, Any, Optional, List

from .llm_client import LLMClient
from .exceptions import OptimizationError

logger = logging.getLogger(__name__)

class QueryOptimizer:
    """
    A class to optimize HyperXQL queries for better performance.
    """
    
    def __init__(self, llm_client):
        """
        Initialize the query optimizer.
        
        Args:
            llm_client: LLM client instance
        """
        self.llm_client = llm_client
    
    def _analyze_and_transform(self, query):
        """
        Analyze the query and transform it for better performance.
        
        Args:
            query: The original query
            
        Returns:
            str: The transformed query
        """
        # This would contain logic to:
        # - Reorder operations for efficiency
        # - Apply query rewriting rules
        # - Optimize join operations
        # - etc.
        
        # For now, just return the original query
        return query
    
    def _generate_optimization_notes(self, original_query, optimized_query):
        """
        Generate notes about the optimizations performed.
        
        Args:
            original_query: The original query
            optimized_query: The optimized query
            
        Returns:
            list: Notes about optimizations performed
        """
        # Placeholder implementation
        return ["No optimizations applied."]
    
    def explain_query(self, query):
        """
        Generate an execution plan explanation for a query.
        
        Args:
            query: The query to explain
            
        Returns:
            dict: Explanation of how the query would be executed
        """
        # Placeholder implementation
        return {
            "query": query,
            "execution_plan": "Sequential scan",
            "estimated_cost": 0
        }
    
    def optimize_query(self, sql: str, db_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Optimize a SQL query for better performance.
        
        Args:
            sql: The SQL query to optimize
            db_info: Database schema information
            
        Returns:
            Dictionary with optimized SQL and explanations
        """
        # Build system prompt for optimization
        system_prompt = """You are a SQL optimization expert. Analyze the SQL query
and suggest optimizations to improve performance. Consider:

1. Proper indexing strategies
2. Query structure improvements
3. JOIN optimizations
4. Subquery vs JOIN tradeoffs
5. Redundant operations
6. More efficient function usage

Keep the query semantically equivalent - it must return the same results.
"""
        
        # Build user prompt with DB schema and SQL
        schema_str = json.dumps(db_info, indent=2) if db_info else "No schema available"
        user_prompt = f"""
Database Schema:
{schema_str}

SQL Query to Optimize:
{sql}

Provide optimization in this format:
{{
    "optimized_sql": "The optimized SQL query",
    "improvements": [
        {{
            "type": "index/join/restructure/function/etc",
            "description": "Description of the improvement",
            "impact": "high/medium/low"
        }}
    ],
    "performance_impact": "Estimated performance improvement",
    "explanation": "Detailed explanation of all optimizations"
}}
"""
        
        try:
            response = self.llm_client.generate_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.1,
                response_format={"type": "json_object"} if self.llm_client.provider == "openai" else None
            )
            
            # Extract the optimization result
            completion = response.get("completion", "")
            if isinstance(completion, dict):
                result = completion
            else:
                # Try to parse as JSON
                try:
                    # Check if wrapped in code block
                    if "```json" in completion:
                        json_content = completion.split("```json")[1].split("```")[0]
                        result = json.loads(json_content)
                    elif "```" in completion:
                        json_content = completion.split("```")[1]
                        result = json.loads(json_content)
                    else:
                        result = json.loads(completion)
                except (json.JSONDecodeError, IndexError):
                    logger.error(f"Failed to parse optimization response: {completion}")
                    result = {
                        "optimized_sql": sql,  # Use original SQL
                        "improvements": [],
                        "performance_impact": "none",
                        "explanation": "Could not generate optimization suggestions."
                    }
            
            # Ensure the optimized SQL is not empty
            if not result.get("optimized_sql"):
                result["optimized_sql"] = sql
                result["explanation"] = "No optimization needed or possible."
            
            return result
            
        except Exception as e:
            logger.exception(f"Error optimizing query: {str(e)}")
            raise OptimizationError(f"Failed to optimize query: {str(e)}")
    
    def suggest_indexes(self, sql: str, db_info: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Suggest index creation statements for a query.
        
        Args:
            sql: The SQL query to analyze
            db_info: Database schema information
            
        Returns:
            List of suggested index creation statements with explanations
        """
        # Build system prompt for index suggestion
        system_prompt = """You are an database indexing expert. Analyze the SQL query
and suggest appropriate indexes to improve its performance. Consider:

1. Tables involved in WHERE clauses
2. JOIN conditions
3. ORDER BY and GROUP BY columns
4. Multi-column index opportunities
5. Index selectivity
6. DB-specific index types (if db_type is known)

Provide practical CREATE INDEX statements.
"""
        
        # Build user prompt
        db_type = db_info.get("db_type", "unknown") if db_info else "unknown"
        schema_str = json.dumps(db_info, indent=2) if db_info else "No schema available"
        user_prompt = f"""
Database Type: {db_type}
Database Schema:
{schema_str}

SQL Query to analyze for indexing:
{sql}

Return suggestions in this format:
{{
    "index_suggestions": [
        {{
            "create_statement": "CREATE INDEX idx_name ON table(columns)",
            "reason": "Detailed explanation why this index would help",
            "impact": "high/medium/low"
        }}
    ],
    "explanation": "Overall indexing strategy explanation"
}}
"""
        
        try:
            response = self.llm_client.generate_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.1,
                response_format={"type": "json_object"} if self.llm_client.provider == "openai" else None
            )
            
            # Extract the suggestions
            completion = response.get("completion", "")
            if isinstance(completion, dict):
                result = completion
            else:
                # Try to parse as JSON
                try:
                    # Check if wrapped in code block
                    if "```json" in completion:
                        json_content = completion.split("```json")[1].split("```")[0]
                        result = json.loads(json_content)
                    elif "```" in completion:
                        json_content = completion.split("```")[1]
                        result = json.loads(json_content)
                    else:
                        result = json.loads(completion)
                except (json.JSONDecodeError, IndexError):
                    logger.error(f"Failed to parse index suggestion response: {completion}")
                    result = {
                        "index_suggestions": [],
                        "explanation": "Could not generate index suggestions."
                    }
            
            return result.get("index_suggestions", [])
            
        except Exception as e:
            logger.exception(f"Error suggesting indexes: {str(e)}")
            return []
