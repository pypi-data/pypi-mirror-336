"""
Tests for the CLI module.
"""

import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from hyperxql.cli import cli
from hyperxql.exceptions import ConfigurationError, LLMAPIError, DatabaseError

@pytest.fixture
def cli_runner():
    """Create a Click CLI test runner."""
    return CliRunner()

def test_version(cli_runner):
    """Test that the CLI displays version information."""
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()

@patch("hyperxql.cli.initialize_config")
def test_init_command(mock_init_config, cli_runner):
    """Test the init command."""
    # Mock successful initialization
    mock_init_config.return_value = MagicMock()
    
    result = cli_runner.invoke(cli, ["init"])
    assert result.exit_code == 0
    assert "configuration completed successfully" in result.output.lower()
    
    # Test error handling
    mock_init_config.side_effect = ConfigurationError("Test error")
    result = cli_runner.invoke(cli, ["init"])
    assert result.exit_code == 1
    assert "error during configuration" in result.output.lower()
    assert "test error" in result.output.lower()

@patch("hyperxql.cli.Config")
@patch("hyperxql.cli.LLMClient")
@patch("hyperxql.cli.DatabaseManager")
@patch("hyperxql.cli.SQLGenerator")
@patch("hyperxql.cli.get_current_db_info")
def test_query_command(
    mock_get_db_info, 
    mock_sql_generator_class, 
    mock_db_manager_class, 
    mock_llm_client_class, 
    mock_config_class,
    cli_runner
):
    """Test the query command."""
    # Set up mocks
    mock_config = MagicMock()
    mock_config_class.return_value = mock_config
    
    mock_llm_client = MagicMock()
    mock_llm_client_class.return_value = mock_llm_client
    
    mock_db_manager = MagicMock()
    mock_db_manager_class.return_value = mock_db_manager
    
    mock_sql_generator = MagicMock()
    mock_sql_generator_class.return_value = mock_sql_generator
    
    # Mock DB info
    mock_get_db_info.return_value = {
        "db_type": "sqlite",
        "db_name": "test.db",
        "tables": [{"name": "users", "columns": [{"name": "id", "type": "INTEGER"}]}]
    }
    
    # Mock SQL generation response
    mock_sql_response = MagicMock()
    mock_sql_response.sql = "SELECT * FROM users"
    mock_sql_response.explanation = "This query selects all users"
    mock_sql_response.execute = True
    mock_sql_response.display_format = "table"
    mock_sql_response.metadata = {"query_type": "select"}
    
    mock_sql_generator.generate_sql.return_value = mock_sql_response
    
    # Mock execution result
    mock_db_manager.execute_sql.return_value = {
        "success": True,
        "query_type": "select",
        "columns": ["id", "name"],
        "rows": [(1, "Alice"), (2, "Bob")],
        "row_count": 2
    }
    
    # Test successful query execution
    result = cli_runner.invoke(cli, ["query", "list", "all", "users"])
    assert result.exit_code == 0
    assert "your query" in result.output.lower()
    assert "generated sql" in result.output.lower()
    
    # Test without arguments
    result = cli_runner.invoke(cli, ["query"])
    assert result.exit_code == 0
    assert "please provide a natural language query" in result.output.lower()
    
    # Test error handling - configuration error
    mock_config_class.side_effect = ConfigurationError("Config error")
    result = cli_runner.invoke(cli, ["query", "list", "users"])
    assert "configuration error" in result.output.lower()
    
    # Reset mock for next test
    mock_config_class.side_effect = None
    mock_config_class.return_value = mock_config
    
    # Test error handling - LLM API error
    mock_llm_client_class.side_effect = LLMAPIError("API error")
    result = cli_runner.invoke(cli, ["query", "list", "users"])
    assert "llm api error" in result.output.lower()
    
    # Reset mock for next test
    mock_llm_client_class.side_effect = None
    mock_llm_client_class.return_value = mock_llm_client
    
    # Test error handling - Database error
    mock_db_manager_class.side_effect = DatabaseError("DB error")
    result = cli_runner.invoke(cli, ["query", "list", "users"])
    assert "database error" in result.output.lower()

@patch("hyperxql.cli.Config")
@patch("hyperxql.cli.initialize_config")
def test_config_command(mock_init_config, mock_config_class, cli_runner):
    """Test the config command."""
    # Set up mock
    mock_config = MagicMock()
    mock_config.llm_provider = "openai"
    mock_config.db_config = {
        "db_type": "sqlite",
        "database": "test.db"
    }
    mock_config_class.return_value = mock_config
    
    # Test viewing config (no update)
    with patch("click.confirm", return_value=False):
        result = cli_runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "current configuration" in result.output.lower()
        assert "openai" in result.output.lower()
        assert "sqlite" in result.output.lower()
    
    # Test updating config
    with patch("click.confirm", return_value=True):
        result = cli_runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "current configuration" in result.output.lower()
        mock_init_config.assert_called_once()
    
    # Test error handling
    mock_config_class.side_effect = ConfigurationError("Config error")
    result = cli_runner.invoke(cli, ["config"])
    assert "configuration error" in result.output.lower()
