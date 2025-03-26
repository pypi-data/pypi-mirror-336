"""
Client for interacting with LLM providers.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List, Tuple, Union

import requests
from openai import OpenAI
from .exceptions import LLMAPIError, ConfigurationError

logger = logging.getLogger(__name__)

class LLMClient:
    """Client for interacting with LLM providers."""
    
    def __init__(self, config):
        """Initialize the LLM client with configuration."""
        self.config = config
        self.provider = config.llm_provider
        
        # Validate configuration
        if self.provider == "openai" and not config.openai_api_key:
            raise LLMAPIError("OpenAI API key is not configured")
        elif self.provider == "together" and not config.together_api_key:
            raise LLMAPIError("Together AI API key is not configured")
            
        # Initialize prompt templates
        self.prompt_templates = {
            "default": self._get_default_prompt_template(),
            "mysql": self._get_mysql_prompt_template(),
            "postgresql": self._get_postgresql_prompt_template(),
            "sqlite": self._get_sqlite_prompt_template(),
            "oracle": self._get_oracle_prompt_template(),
            "sqlserver": self._get_sqlserver_prompt_template(),
        }
        
        # Setup response history for context
        self.response_history = []
        self.max_history_items = 5
    
    def generate_completion(self, 
                           messages: List[Dict[str, str]] = None,
                           system_prompt: str = None, 
                           user_prompt: str = None, 
                           temperature: float = 0.1, 
                           max_tokens: int = 4000,
                           response_format: Optional[Dict[str, str]] = None,
                           stream: bool = False) -> Dict[str, Any]:
        """
        Generate a completion from the LLM.
        
        Args:
            messages: List of message dictionaries (overrides system_prompt and user_prompt)
            system_prompt: System instructions
            user_prompt: User query
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            response_format: Format specification for the response
            stream: Whether to stream the response
            
        Returns:
            Completion response
        """
        # If individual prompts are provided, convert to messages format
        if messages is None and system_prompt is not None and user_prompt is not None:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        
        if messages is None:
            raise ValueError("Either messages or both system_prompt and user_prompt must be provided")
        
        if self.provider == "openai":
            return self._generate_openai_completion(
                messages, temperature, response_format, max_tokens, stream
            )
        elif self.provider == "together":
            return self._generate_together_completion(
                messages, temperature, max_tokens, stream
            )
        else:
            raise LLMAPIError(f"Unsupported LLM provider: {self.provider}")
    
    def _generate_openai_completion(self, 
                                   messages: List[Dict[str, str]],
                                   temperature: float,
                                   response_format: Optional[Dict[str, str]] = None,
                                   max_tokens: int = 4000,
                                   stream: bool = False) -> Dict[str, Any]:
        """Generate a completion using OpenAI."""
        try:
            client = OpenAI(api_key=self.config.openai_api_key)
            
            completion_args = {
                "model": self.config.openai_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream
            }
            
            if response_format:
                completion_args["response_format"] = response_format
                
            response = client.chat.completions.create(**completion_args)
            
            if stream:
                # Return a generator for streaming
                return {"provider": "openai", "model": self.config.openai_model, "stream": response}
            else:
                # Return the completion
                completion = response.choices[0].message.content
                
                # Handle JSON format if requested
                if response_format and response_format.get("type") == "json_object":
                    try:
                        content = json.loads(completion)
                    except json.JSONDecodeError:
                        content = {"error": "Failed to parse JSON response", "raw": completion}
                else:
                    content = completion
                    
                result = {
                    "completion": content,
                    "provider": "openai",
                    "model": self.config.openai_model
                }
                
                # Store in history
                self._update_history(result)
                
                return result
                
        except Exception as e:
            logger.exception(f"Error generating OpenAI completion: {str(e)}")
            raise LLMAPIError(f"OpenAI API error: {str(e)}")
    
    def _generate_together_completion(self, 
                                     messages: List[Dict[str, str]],
                                     temperature: float,
                                     max_tokens: int = 4000,
                                     stream: bool = False) -> Dict[str, Any]:
        """Generate a completion using Together AI."""
        try:
            url = "https://api.together.xyz/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.config.together_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.config.together_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream
            }
            
            if stream:
                # Set up streaming
                response = requests.post(url, json=payload, headers=headers, stream=True)
                response.raise_for_status()
                return {
                    "provider": "together",
                    "model": self.config.together_model,
                    "stream": response
                }
            else:
                # Regular request
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                result = response.json()
                
                completion = result["choices"][0]["message"]["content"]
                
                result = {
                    "completion": completion,
                    "provider": "together",
                    "model": self.config.together_model
                }
                
                # Store in history
                self._update_history(result)
                
                return result
                
        except requests.exceptions.RequestException as e:
            logger.exception(f"Error generating Together AI completion: {str(e)}")
            status_code = getattr(e.response, 'status_code', None)
            error_text = getattr(e.response, 'text', str(e))
            raise LLMAPIError(f"Together AI API error: {error_text} (Status: {status_code})")
        except Exception as e:
            logger.exception(f"Unexpected error with Together AI: {str(e)}")
            raise LLMAPIError(f"Together AI error: {str(e)}")
    
    def _update_history(self, result: Dict[str, Any]) -> None:
        """Update response history for context in future queries."""
        self.response_history.append(result)
        
        # Limit history size
        if len(self.response_history) > self.max_history_items:
            self.response_history.pop(0)
    
    def generate_sql_from_nl(self, 
                            query: str, 
                            db_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate SQL from natural language with enhanced database context.
        
        Args:
            query: Natural language query
            db_info: Database schema information
            
        Returns:
            Dictionary with SQL and related information
        """
        # Build system prompt with DB info
        system_prompt = self._build_system_prompt(db_info)
        
        # Add few-shot examples if available for this database type
        if db_info and 'db_type' in db_info:
            examples = self._get_few_shot_examples(db_type=db_info['db_type'])
            if examples:
                system_prompt += f"\n\n{examples}"
        
        # Generate the response
        response = self.generate_completion(
            system_prompt=system_prompt,
            user_prompt=query,
            temperature=0.1,
            response_format={"type": "json_object"} if self.provider == "openai" else None
        )
        
        # Process the response based on provider
        if self.provider == "openai":
            result = response["completion"]
            if not isinstance(result, dict):
                # Should not happen with response_format=json_object
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse OpenAI response as JSON: {result}")
                    result = {
                        "sql": "",
                        "explanation": "Failed to generate valid SQL response",
                        "execute": False,
                        "display_format": "text",
                        "metadata": {"error": "json_parse_failure"}
                    }
        else:
            # Together AI doesn't support response_format, so we parse it manually
            try:
                completion = response["completion"]
                
                # Try to extract JSON block if present
                if "```json" in completion:
                    json_content = completion.split("```json")[1].split("```")[0]
                    result = json.loads(json_content)
                elif "```" in completion:
                    # Check if there's a pure JSON block
                    json_content = completion.split("```")[1]
                    result = json.loads(json_content)
                else:
                    # Try to parse the whole thing as JSON
                    result = json.loads(completion)
            except (json.JSONDecodeError, IndexError):
                logger.error(f"Failed to parse Together AI response as JSON: {response['completion']}")
                result = {
                    "sql": "",
                    "explanation": "Failed to generate valid SQL response",
                    "execute": False,
                    "display_format": "text",
                    "metadata": {"error": "json_parse_failure"}
                }
        
        # Add provider and model to the result
        result["provider"] = response["provider"]
        result["model"] = response["model"]
        
        return result
    
    def _build_system_prompt(self, db_info: Optional[Dict[str, Any]] = None) -> str:
        """
        Build system prompt for SQL generation with enhanced DB context.
        
        Args:
            db_info: Optional database schema information
            
        Returns:
            System prompt string
        """
        # Select template based on database type
        db_type = db_info.get("db_type", "default") if db_info else "default"
        if db_type in self.prompt_templates:
            prompt_template = self.prompt_templates[db_type]
        else:
            prompt_template = self.prompt_templates["default"]
            
        # Create the base prompt
        prompt = prompt_template
        
        # Add database information if available
        if db_info:
            prompt += "\n\nCURRENT DATABASE INFORMATION:\n"
            
            if "db_type" in db_info:
                prompt += f"Database Type: {db_info['db_type']}\n"
            
            # Add explicit relationships if available
            if "explicit_relationships" in db_info and db_info["explicit_relationships"]:
                prompt += "\nExplicit Relationships:\n"
                for rel in db_info["explicit_relationships"]:
                    prompt += f"- {rel['source_table']}({','.join(rel['source_columns'])}) → " \
                              f"{rel['target_table']}({','.join(rel['target_columns'])})\n"
            
            # Add implicit relationships if available
            if "implicit_relationships" in db_info and db_info["implicit_relationships"]:
                prompt += "\nPotential Implicit Relationships (detected by naming convention):\n"
                for rel in db_info["implicit_relationships"]:
                    prompt += f"- {rel['source_table']}({rel['source_column']}) → " \
                              f"{rel['target_table']}({rel['target_column']}) (confidence: {rel['confidence']})\n"
            
            # Add data patterns if available
            if "data_patterns" in db_info and db_info["data_patterns"]:
                prompt += "\nData Patterns:\n"
                
                if "time_series_tables" in db_info["data_patterns"]:
                    prompt += "Time-Series Tables:\n"
                    for ts in db_info["data_patterns"]["time_series_tables"]:
                        prompt += f"- {ts['table']} (time columns: {', '.join(ts['time_columns'])})\n"
                        
                if "lookup_tables" in db_info["data_patterns"]:
                    prompt += "Lookup Tables (small tables used for classifications/categories):\n"
                    prompt += f"- {', '.join(db_info['data_patterns']['lookup_tables'])}\n"
            
            # Add tables information
            if "tables" in db_info:
                prompt += "\nTables:\n"
                for table_info in db_info["tables"]:
                    prompt += f"- {table_info['name']}"
                    if "row_count" in table_info and table_info["row_count"] >= 0:
                        prompt += f" (~{table_info['row_count']} rows)"
                    prompt += "\n"
                    
                    # Add columns
                    if "columns" in table_info:
                        for col in table_info["columns"]:
                            col_desc = f"  - {col['name']} ({col['type']})"
                            if col.get("is_primary_key"):
                                col_desc += " PRIMARY KEY"
                            if col.get("is_foreign_key"):
                                col_desc += f" REFERENCES {col['references']}"
                            if not col.get("is_nullable", True):
                                col_desc += " NOT NULL"
                            if col.get("default") and col.get("default") != "NULL":
                                col_desc += f" DEFAULT {col['default']}"
                            prompt += col_desc + "\n"
                    
                    # Add sample data if available and not too large
                    if "sample_data" in table_info and table_info["sample_data"]:
                        prompt += f"  Sample data ({min(3, len(table_info['sample_data']))} rows):\n"
                        for i, row in enumerate(table_info["sample_data"][:3]):  # Show up to 3 rows
                            row_str = ", ".join([f"{k}={v}" for k, v in row.items()])
                            prompt += f"    Row {i+1}: {row_str}\n"
        else:
            prompt += "\n\nNo existing database schema information available. You can create new tables as needed."
        
        # Add context from previous queries if available
        if self.response_history:
            prompt += "\n\nRECENT QUERY HISTORY (for context):\n"
            for i, item in enumerate(self.response_history[-3:]):  # Show last 3 items
                if isinstance(item.get("completion"), dict) and "sql" in item["completion"]:
                    sql = item["completion"]["sql"]
                    explanation = item["completion"].get("explanation", "")
                    prompt += f"{i+1}. SQL: {sql}\n   Explanation: {explanation}\n\n"
                elif isinstance(item.get("completion"), str):
                    # Try to extract SQL if it's a JSON string
                    try:
                        parsed = json.loads(item["completion"])
                        if "sql" in parsed:
                            prompt += f"{i+1}. SQL: {parsed['sql']}\n"
                            if "explanation" in parsed:
                                prompt += f"   Explanation: {parsed['explanation']}\n\n"
                    except (json.JSONDecodeError, TypeError):
                        pass
        
        return prompt
    
    def _get_default_prompt_template(self) -> str:
        """Get the default prompt template."""
        return """You are HyperXQL, an advanced Natural Language to SQL conversion assistant. 
Your task is to convert natural language requests into SQL queries.

Guidelines:
1. Generate valid SQL based on the user's natural language request
2. Provide clear explanations of the SQL code
3. Consider database schema information when provided
4. Always use safe SQL practices (parameterization when needed)
5. Include metadata about what the query does
6. Be aware of the exact database structure shared below
7. Understand relationships between tables to create proper JOINs
8. Use appropriate SQL functions for the specific database type

ALWAYS RESPOND IN THIS JSON FORMAT:
{
    "sql": "SQL query string",
    "explanation": "Clear explanation of what the SQL does and why it addresses the user's request",
    "execute": true/false,  // whether the SQL should be executed
    "display_format": "table/text/graph/json",  // how results should be displayed
    "metadata": {
        "query_type": "select/insert/update/delete/create/other",
        "tables_affected": ["table_names"],
        "db_update": true/false,  // whether schema was modified
        "relations_used": ["relation1", "relation2"],  // relationships leveraged in query
        "estimated_complexity": "low/medium/high"  // complexity of the generated SQL
    }
}

For CREATE TABLE statements, include appropriate data types and constraints.
For INSERT statements, use parameterized queries with placeholder values.
For complex JOIN operations, ensure proper relationship understanding.
"""

    def _get_mysql_prompt_template(self) -> str:
        """Get MySQL-specific prompt template."""
        base = self._get_default_prompt_template()
        return base + """
MySQL-Specific Guidelines:
1. Use backticks (`table_name`) for table and column identifiers
2. Use AUTO_INCREMENT for auto-incrementing columns
3. Consider InnoDB storage engine for tables with relationships (supports foreign keys)
4. Use appropriate MySQL functions (e.g., DATE_FORMAT(), CONCAT())
5. For TEXT or BLOB columns, consider maximum size constraints
"""

    def _get_postgresql_prompt_template(self) -> str:
        """Get PostgreSQL-specific prompt template."""
        base = self._get_default_prompt_template()
        return base + """
PostgreSQL-Specific Guidelines:
1. Use double quotes for identifiers when needed ("table_name")
2. Use serial or IDENTITY for auto-incrementing columns
3. Consider using appropriate PostgreSQL data types (e.g., jsonb, array types)
4. Leverage PostgreSQL-specific features like RETURNING clause, CTEs
5. Use appropriate PostgreSQL functions (to_char(), string_agg(), etc.)
"""

    def _get_sqlite_prompt_template(self) -> str:
        """Get SQLite-specific prompt template."""
        base = self._get_default_prompt_template()
        return base + """
SQLite-Specific Guidelines:
1. Use AUTOINCREMENT for rowid-like functionality
2. Remember SQLite has flexible typing (TEXT, INTEGER, REAL, BLOB, NULL)
3. Use SQLite datetime functions correctly (datetime(), date(), time())
4. Be aware of SQLite limitations (e.g., ALTER TABLE limitations)
5. Consider PRAGMA statements for configuring database behavior
"""

    def _get_oracle_prompt_template(self) -> str:
        """Get Oracle-specific prompt template."""
        base = self._get_default_prompt_template()
        return base + """
Oracle-Specific Guidelines:
1. Use sequences and triggers for auto-incrementing columns
2. Consider tablespace specifications when creating tables
3. Use dual for queries that don't need a specific table
4. Use Oracle-specific functions (TO_CHAR, NVL, etc.)
5. Use ROWNUM or ROW_NUMBER() for pagination
"""

    def _get_sqlserver_prompt_template(self) -> str:
        """Get SQL Server-specific prompt template."""
        base = self._get_default_prompt_template()
        return base + """
SQL Server-Specific Guidelines:
1. Use square brackets [table_name] for identifiers
2. Use IDENTITY for auto-incrementing columns
3. Use appropriate SQL Server functions (CONVERT(), ISNULL(), etc.)
4. Consider using TOP clause for limiting results
5. Use SQL Server specific datatypes (e.g., datetime2, varchar(max))
"""

    def _get_few_shot_examples(self, db_type: str) -> str:
        """Get few-shot examples for specific database type."""
        if db_type == "mysql":
            return """
Few-shot examples:

User: "Find all customers who placed orders in the last month"
Response:
```json
{
    "sql": "SELECT c.customer_id, c.name, COUNT(o.order_id) AS order_count FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH) GROUP BY c.customer_id, c.name ORDER BY order_count DESC",
    "explanation": "This query joins the customers and orders tables, filters orders from the last month using DATE_SUB, counts orders per customer, and sorts by order count.",
    "execute": true,
    "display_format": "table",
    "metadata": {
        "query_type": "select",
        "tables_affected": ["customers", "orders"],
        "db_update": false,
        "relations_used": ["customers-orders"],
        "estimated_complexity": "medium"
    }
}
```

User: "Add a new product with name 'Wireless Headphones', price $89.99, and category 'Electronics'"
Response:
```json
{
    "sql": "INSERT INTO products (name, price, category, created_at) VALUES ('Wireless Headphones', 89.99, 'Electronics', NOW())",
    "explanation": "This query inserts a new product with the specified name, price, and category into the products table. The created_at field is set to the current timestamp.",
    "execute": true,
    "display_format": "text",
    "metadata": {
        "query_type": "insert",
        "tables_affected": ["products"],
        "db_update": true,
        "relations_used": [],
        "estimated_complexity": "low"
    }
}
```
"""
        # Add other database types as needed
        return ""
