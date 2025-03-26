"""
Tests for the LLM client module.
"""

import pytest
from unittest.mock import patch, MagicMock

from hyperxql.llm_client import LLMClient
from hyperxql.exceptions import LLMAPIError

@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    config = MagicMock()
    config.llm_provider = "openai"
    config.openai_api_key = "test_key"
    config.openai_model = "gpt-4o"
    config.together_api_key = "test_together_key"
    config.together_model = "togethercomputer/llama-2-70b-chat"
    return config

def test_init_with_missing_api_key():
    """Test initialization with missing API key."""
    config = MagicMock()
    config.llm_provider = "openai"
    config.openai_api_key = ""
    
    with pytest.raises(LLMAPIError, match="OpenAI API key is not configured"):
        LLMClient(config)
    
    config.llm_provider = "together"
    config.together_api_key = ""
    
    with pytest.raises(LLMAPIError, match="Together AI API key is not configured"):
        LLMClient(config)

def test_init_with_unsupported_provider():
    """Test initialization with unsupported provider."""
    config = MagicMock()
    config.llm_provider = "unsupported"
    client = LLMClient(config)
    
    messages = [{"role": "user", "content": "Hello"}]
    with pytest.raises(LLMAPIError, match="Unsupported LLM provider"):
        client.generate_completion(messages)

@patch("openai.OpenAI")
def test_openai_completion(mock_openai, mock_config):
    """Test OpenAI completion generation."""
    # Set up OpenAI mock
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Test response"
    mock_client.chat.completions.create.return_value = mock_response
    
    # Create client and test
    client = LLMClient(mock_config)
    messages = [{"role": "user", "content": "Hello"}]
    result = client._generate_openai_completion(messages, 0.5, None)
    
    assert result["content"] == "Test response"
    assert result["provider"] == "openai"
    assert result["model"] == mock_config.openai_model
    
    # Test with JSON response format
    mock_response.choices[0].message.content = '{"result": "Test JSON"}'
    result = client._generate_openai_completion(messages, 0.5, {"type": "json_object"})
    
    assert result["content"] == {"result": "Test JSON"}
    
    # Test error handling
    mock_client.chat.completions.create.side_effect = Exception("API error")
    with pytest.raises(LLMAPIError, match="OpenAI API error"):
        client._generate_openai_completion(messages, 0.5, None)

@patch("requests.post")
def test_together_completion(mock_post, mock_config):
    """Test Together AI completion generation."""
    # Set up requests mock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Test response"}}]
    }
    mock_post.return_value = mock_response
    
    # Create client and test
    mock_config.llm_provider = "together"
    client = LLMClient(mock_config)
    messages = [{"role": "user", "content": "Hello"}]
    result = client._generate_together_completion(messages, 0.5)
    
    assert result["content"] == "Test response"
    assert result["provider"] == "together"
    assert result["model"] == mock_config.together_model
    
    # Test error response
    mock_response.status_code = 400
    mock_response.text = "Bad request"
    with pytest.raises(LLMAPIError, match="Together AI API error"):
        client._generate_together_completion(messages, 0.5)
    
    # Test exception
    mock_post.side_effect = Exception("API error")
    with pytest.raises(LLMAPIError, match="Together AI API error"):
        client._generate_together_completion(messages, 0.5)

def test_generate_sql_from_nl(mock_config):
    """Test SQL generation from natural language."""
    client = LLMClient(mock_config)
    
    # Mock the generate_completion method
    client.generate_completion = MagicMock()
    client.generate_completion.return_value = {
        "content": {
            "sql": "SELECT * FROM users",
            "explanation": "This query selects all users",
            "execute": True,
            "display_format": "table",
            "metadata": {"query_type": "select"}
        },
        "provider": "openai",
        "model": "gpt-4o"
    }
    
    result = client.generate_sql_from_nl("List all users")
    
    assert result["sql"] == "SELECT * FROM users"
    assert result["explanation"] == "This query selects all users"
    assert result["execute"] is True
    assert result["provider"] == "openai"
    assert result["model"] == "gpt-4o"
    
    # Test with string response (Together AI)
    mock_config.llm_provider = "together"
    client = LLMClient(mock_config)
    client.generate_completion = MagicMock()
    client.generate_completion.return_value = {
        "content": '{"sql": "SELECT * FROM users", "explanation": "This query selects all users", "execute": true, "display_format": "table", "metadata": {"query_type": "select"}}',
        "provider": "together",
        "model": "llama-2-70b"
    }
    
    result = client.generate_sql_from_nl("List all users")
    
    assert result["sql"] == "SELECT * FROM users"
    assert result["explanation"] == "This query selects all users"
    assert result["execute"] is True
    assert result["provider"] == "together"
    assert result["model"] == "llama-2-70b"

def test_build_system_prompt(mock_config):
    """Test building system prompt."""
    client = LLMClient(mock_config)
    
    # Test without DB info
    prompt = client._build_system_prompt()
    assert "You are HyperXQL" in prompt
    assert "ALWAYS RESPOND IN THIS JSON FORMAT" in prompt
    
    # Test with DB info
    db_info = {
        "db_type": "sqlite",
        "tables": [
            {
                "name": "users",
                "columns": [
                    {"name": "id", "type": "INTEGER", "is_primary_key": True, "is_nullable": False},
                    {"name": "name", "type": "TEXT"}
                ]
            }
        ]
    }
    
    prompt = client._build_system_prompt(db_info)
    assert "CURRENT DATABASE INFORMATION" in prompt
    assert "Database Type: sqlite" in prompt
    assert "- users" in prompt
    assert "- id (INTEGER) PRIMARY KEY NOT NULL" in prompt
    assert "- name (TEXT)" in prompt
