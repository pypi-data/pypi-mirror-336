"""
LLM client module for HyperXQL.
Handles communication with LLM providers (OpenAI and Together AI).
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List, Union

from .config import Config
from .exceptions import LLMAPIError

logger = logging.getLogger(__name__)

class LLMClient:
    """Client for interacting with LLM providers."""
    
    def __init__(self, config: Config):
        """Initialize the LLM client with configuration."""
        self.config = config
        self.provider = config.llm_provider
        
        # Validate configuration
        if self.provider == "openai" and not config.openai_api_key:
            raise LLMAPIError("OpenAI API key is not configured. Run 'hyperxql init' to set it up.")
        elif self.provider == "together" and not config.together_api_key:
            raise LLMAPIError("Together AI API key is not configured. Run 'hyperxql init' to set it up.")
    
    def generate_completion(self, 
                           messages: List[Dict[str, str]],
                           temperature: float = 0.3,
                           response_format: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Generate a completion from the LLM.
        
        Args:
            messages: List of message dictionaries with role and content
            temperature: Temperature for generation (0-1)
            response_format: Optional format specification for response
            
        Returns:
            Dictionary containing completion result
        """
        if self.provider == "openai":
            return self._generate_openai_completion(messages, temperature, response_format)
        elif self.provider == "together":
            return self._generate_together_completion(messages, temperature)
        else:
            raise LLMAPIError(f"Unsupported LLM provider: {self.provider}")
    
    def _generate_openai_completion(self, 
                                  messages: List[Dict[str, str]],
                                  temperature: float,
                                  response_format: Optional[Dict[str, str]]) -> Dict[str, Any]:
        """Generate a completion using OpenAI API."""
        try:
            # Import here to avoid dependency if not used
            from openai import OpenAI
            
            # Initialize client
            client = OpenAI(api_key=self.config.openai_api_key)
            
            # Build request parameters
            params = {
                "model": self.config.openai_model,  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
                "messages": messages,
                "temperature": temperature,
            }
            
            # Add response format if specified
            if response_format:
                params["response_format"] = response_format
            
            # Make the request
            response = client.chat.completions.create(**params)
            
            # Extract the content
            content = response.choices[0].message.content
            
            # Try to parse JSON if response_format is json_object
            if response_format and response_format.get("type") == "json_object":
                try:
                    content = json.loads(content)
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON response from OpenAI")
            
            return {
                "content": content,
                "provider": "openai",
                "model": self.config.openai_model
            }
            
        except ImportError:
            raise LLMAPIError("OpenAI package is not installed. Install it with 'pip install openai'.")
        except Exception as e:
            logger.exception("Error calling OpenAI API")
            raise LLMAPIError(f"OpenAI API error: {str(e)}")
    
    def _generate_together_completion(self, 
                                    messages: List[Dict[str, str]],
                                    temperature: float) -> Dict[str, Any]:
        """Generate a completion using Together AI API."""
        try:
            import requests
            
            api_key = self.config.together_api_key
            model = self.config.together_model
            
            # Together AI API endpoint
            url = "https://api.together.xyz/v1/chat/completions"
            
            # Build request
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 2048
            }
            
            # Make the request
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code != 200:
                raise LLMAPIError(f"Together AI API error: {response.text}")
            
            response_data = response.json()
            content = response_data["choices"][0]["message"]["content"]
            
            return {
                "content": content,
                "provider": "together",
                "model": model
            }
        
        except ImportError:
            raise LLMAPIError("Requests package is not installed. Install it with 'pip install requests'.")
        except Exception as e:
            logger.exception("Error calling Together AI API")
            raise LLMAPIError(f"Together AI API error: {str(e)}")
    
    def generate_sql_from_nl(self, 
                           query: str, 
                           db_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate SQL from natural language query.
        
        Args:
            query: Natural language query
            db_info: Optional database schema information
            
        Returns:
            Dictionary with SQL and metadata
        """
        # Build the system message with instructions
        system_message = {
            "role": "system",
            "content": self._build_system_prompt(db_info)
        }
        
        # User message with the query
        user_message = {
            "role": "user",
            "content": query
        }
        
        # Define the expected response format
        response_format = {"type": "json_object"} if self.provider == "openai" else None
        
        # Generate completion
        result = self.generate_completion(
            messages=[system_message, user_message],
            temperature=0.3,
            response_format=response_format
        )
        
        # Parse content as JSON if it's a string (Together AI response)
        content = result["content"]
        if isinstance(content, str) and self.provider == "together":
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON response from Together AI")
                # Try to extract JSON from the text response using a simple approach
                try:
                    start_idx = content.find('{')
                    end_idx = content.rfind('}') + 1
                    if start_idx >= 0 and end_idx > start_idx:
                        json_str = content[start_idx:end_idx]
                        content = json.loads(json_str)
                except Exception:
                    logger.exception("Failed to extract JSON from Together AI response")
                    content = {
                        "sql": "",
                        "explanation": "Failed to parse response. The model did not return valid JSON.",
                        "execute": False,
                        "display_format": "text",
                        "metadata": {}
                    }
        
        # Add provider information
        if isinstance(content, dict):
            content["provider"] = result["provider"]
            content["model"] = result["model"]
        
        return content
    
    def _build_system_prompt(self, db_info: Optional[Dict[str, Any]] = None) -> str:
        """
        Build system prompt for SQL generation.
        
        Args:
            db_info: Optional database schema information
            
        Returns:
            System prompt string
        """
        prompt = """You are HyperXQL, an advanced Natural Language to SQL conversion assistant. 
Your task is to convert natural language requests into SQL queries.

Guidelines:
1. Generate valid SQL based on the user's natural language request
2. Provide clear explanations of the SQL code
3. Consider database schema information when provided
4. Always use safe SQL practices (parameterization when needed)
5. Include metadata about what the query does

ALWAYS RESPOND IN THIS JSON FORMAT:
{
    "sql": "SQL query string",
    "explanation": "Clear explanation of what the SQL does",
    "execute": true/false,  // whether the SQL should be executed
    "display_format": "table/text",  // how results should be displayed
    "metadata": {
        "query_type": "select/insert/update/delete/create/other",
        "tables_affected": ["table_names"],
        "db_update": true/false  // whether schema was modified
    }
}

For CREATE TABLE statements, include appropriate data types and constraints.
For INSERT statements, use parameterized queries with placeholder values.
"""

        # Add database information if available
        if db_info:
            prompt += "\n\nCURRENT DATABASE INFORMATION:\n"
            
            if "db_type" in db_info:
                prompt += f"Database Type: {db_info['db_type']}\n"
            
            if "tables" in db_info:
                prompt += "\nTables:\n"
                for table_info in db_info["tables"]:
                    prompt += f"- {table_info['name']}\n"
                    
                    if "columns" in table_info:
                        for col in table_info["columns"]:
                            col_desc = f"  - {col['name']} ({col['type']})"
                            if col.get("is_primary_key"):
                                col_desc += " PRIMARY KEY"
                            if col.get("is_foreign_key"):
                                col_desc += f" REFERENCES {col['references']}"
                            if not col.get("is_nullable", True):
                                col_desc += " NOT NULL"
                            prompt += col_desc + "\n"
        
        return prompt
