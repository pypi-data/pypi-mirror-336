"""
Tests for the SQL generator module.
"""

import pytest
from unittest.mock import MagicMock

from hyperxql.sql_generator import SQLGenerator, SQLResponse
from hyperxql.exceptions import SQLGenerationError

@pytest.fixture
def mock_llm_client():
    """Create a mock LLM client."""
    client = MagicMock()
    return client

def test_generate_sql_success(mock_llm_client):
    """Test successful SQL generation."""
    # Set up the mock response
    mock_llm_client.generate_sql_from_nl.return_value = {
        "sql": "SELECT * FROM users",
        "explanation": "This query selects all users",
        "execute": True,
        "display_format": "table",
        "metadata": {"query_type": "select"},
        "provider": "openai",
        "model": "gpt-4o"
    }
    
    generator = SQLGenerator(mock_llm_client)
    
    # Call the generate_sql method
    response = generator.generate_sql("List all users")
    
    # Verify the response
    assert isinstance(response, SQLResponse)
    assert response.sql == "SELECT * FROM users"
    assert response.explanation == "This query selects all users"
    assert response.execute is True
    assert response.display_format == "table"
    assert response.metadata == {"query_type": "select"}
    assert response.provider == "openai"
    assert response.model == "gpt-4o"
    
    # Verify the client was called with the right arguments
    mock_llm_client.generate_sql_from_nl.assert_called_once_with("List all users", None)

def test_generate_sql_with_db_info(mock_llm_client):
    """Test SQL generation with database information."""
    # Set up the mock response
    mock_llm_client.generate_sql_from_nl.return_value = {
        "sql": "SELECT * FROM users",
        "explanation": "This query selects all users",
        "execute": True,
        "display_format": "table",
        "metadata": {"query_type": "select"}
    }
    
    generator = SQLGenerator(mock_llm_client)
    
    # Create test database info
    db_info = {
        "db_type": "sqlite",
        "tables": [
            {
                "name": "users",
                "columns": [
                    {"name": "id", "type": "INTEGER", "is_primary_key": True},
                    {"name": "name", "type": "TEXT"}
                ]
            }
        ]
    }
    
    # Call the generate_sql method with database info
    response = generator.generate_sql("List all users", db_info)
    
    # Verify the response
    assert response.sql == "SELECT * FROM users"
    
    # Verify the client was called with the right arguments
    mock_llm_client.generate_sql_from_nl.assert_called_once_with("List all users", db_info)

def test_generate_sql_empty_response(mock_llm_client):
    """Test handling of empty SQL response."""
    # Set up the mock response with empty SQL
    mock_llm_client.generate_sql_from_nl.return_value = {
        "sql": "",
        "explanation": "I couldn't generate SQL for this query.",
        "execute": False,
        "display_format": "text",
        "metadata": {}
    }
    
    generator = SQLGenerator(mock_llm_client)
    
    # Call should raise an exception
    with pytest.raises(SQLGenerationError, match="No SQL generated"):
        generator.generate_sql("Invalid query")

def test_generate_sql_client_error(mock_llm_client):
    """Test handling of client errors."""
    # Set up the mock to raise an exception
    mock_llm_client.generate_sql_from_nl.side_effect = Exception("API error")
    
    generator = SQLGenerator(mock_llm_client)
    
    # Call should raise an exception
    with pytest.raises(SQLGenerationError, match="Failed to generate SQL"):
        generator.generate_sql("List all users")
