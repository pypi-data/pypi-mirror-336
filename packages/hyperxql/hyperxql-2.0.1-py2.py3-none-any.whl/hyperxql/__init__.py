"""
HyperXQL - Natural Language to SQL Database Operations
"""

__version__ = "2.0.1"  # Updated version with AI agent

from hyperxql.config import Config, initialize_config
from hyperxql.llm_client import LLMClient
from hyperxql.db_manager import DatabaseManager
from hyperxql.db_analyzer import DatabaseAnalyzer
from hyperxql.sql_generator import SQLGenerator, SQLResponse
from hyperxql.query_optimizer import QueryOptimizer
from hyperxql.exceptions import (
    HyperXQLException,
    ConfigurationError,
    LLMAPIError,
    DatabaseError,
    SQLGenerationError,
    SchemaAnalysisError,
    OptimizationError,
    ValidationError
)
