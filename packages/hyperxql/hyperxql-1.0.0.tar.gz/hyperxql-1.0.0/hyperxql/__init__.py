"""
HyperXQL: A Python library that enables non-technical users to 
perform SQL database operations using natural language processed by LLMs.

Features:
- Natural language to SQL conversion
- Interactive web interface
- CLI interface for quick queries
- Database schema visualization
- Multiple LLM provider support (OpenAI and Together AI)
- Detailed query explanation and verification
"""

__version__ = "1.0.0"

from hyperxql.config import Config, initialize_config
from hyperxql.llm_client import LLMClient
from hyperxql.db_manager import DatabaseManager
from hyperxql.sql_generator import SQLGenerator, SQLResponse
from hyperxql.exceptions import (
    HyperXQLException,
    ConfigurationError,
    LLMAPIError,
    DatabaseError,
    SQLGenerationError
)
