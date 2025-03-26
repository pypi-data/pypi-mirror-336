"""
Custom exceptions for HyperXQL.
"""

class HyperXQLException(Exception):
    """Base exception for all HyperXQL errors."""
    pass

class ConfigurationError(HyperXQLException):
    """Error related to configuration issues."""
    pass

class LLMAPIError(HyperXQLException):
    """Error related to LLM API calls."""
    pass

class DatabaseError(HyperXQLException):
    """Error related to database operations."""
    pass

class SQLGenerationError(HyperXQLException):
    """Error related to SQL generation."""
    pass

class SchemaAnalysisError(HyperXQLException):
    """Error related to database schema analysis."""
    pass

class OptimizationError(HyperXQLException):
    """Error related to query optimization."""
    pass

class ValidationError(HyperXQLException):
    """Error related to SQL validation."""
    pass
