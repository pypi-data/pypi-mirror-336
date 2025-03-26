"""
Tests for the DatabaseAgent class.
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os
from pathlib import Path
import json
import tempfile
import sqlite3

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hyperxql.agent import DatabaseAgent
from hyperxql.config import Config
from hyperxql.exceptions import DatabaseError, SQLGenerationError

class TestDatabaseAgent(unittest.TestCase):
    """Test cases for the DatabaseAgent class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary SQLite database for testing
        self.temp_db_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db_path = Path(self.temp_db_file.name)
        self.temp_db_file.close()  # Close the file so SQLite can open it
        
        # Initialize test database
        self.conn = sqlite3.connect(str(self.temp_db_path))
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            value TEXT
        )
        ''')
        self.cursor.execute("INSERT INTO test_table (name, value) VALUES (?, ?)", 
                           ("test_entry", "Test value"))
        self.conn.commit()
        self.conn.close()
        
        # Create a temporary config file
        self.temp_config_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w')
        self.temp_config_path = Path(self.temp_config_file.name)
        
        # Write test configuration
        config_data = {
            "llm_provider": "test_provider",
            "test_provider_api_key": "test_key",
            "test_provider_model": "test_model",
            "db_config": {
                "db_type": "sqlite",
                "database": str(self.temp_db_path)
            }
        }
        json.dump(config_data, self.temp_config_file)
        self.temp_config_file.close()
        
        # Mock the Config class
        self.mock_config = MagicMock()
        self.mock_config.db_config = {
            "db_type": "sqlite",
            "database": str(self.temp_db_path)
        }
        
        # Create patches for the required dependencies
        self.db_manager_patch = patch('hyperxql.agent.DatabaseManager')
        self.llm_client_patch = patch('hyperxql.agent.LLMClient')
        self.sql_generator_patch = patch('hyperxql.agent.SQLGenerator')
        self.console_patch = patch('hyperxql.agent.Console')
        
        # Start the patches
        self.mock_db_manager = self.db_manager_patch.start()
        self.mock_llm_client = self.llm_client_patch.start()
        self.mock_sql_generator = self.sql_generator_patch.start()
        self.mock_console = self.console_patch.start()
        
        # Configure the mocks
        self.mock_db_manager_instance = MagicMock()
        self.mock_db_manager.return_value = self.mock_db_manager_instance
        
        self.mock_llm_client_instance = MagicMock()
        self.mock_llm_client.return_value = self.mock_llm_client_instance
        
        self.mock_sql_generator_instance = MagicMock()
        self.mock_sql_generator.return_value = self.mock_sql_generator_instance
        
        self.mock_console_instance = MagicMock()
        self.mock_console.return_value = self.mock_console_instance
        
        # Create the agent with mocked dependencies
        self.agent = DatabaseAgent(self.mock_config, verbose=False)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Stop all the patches
        self.db_manager_patch.stop()
        self.llm_client_patch.stop()
        self.sql_generator_patch.stop()
        self.console_patch.stop()
        
        # Remove temporary files
        if self.temp_db_path.exists():
            os.unlink(str(self.temp_db_path))
        
        if self.temp_config_path.exists():
            os.unlink(str(self.temp_config_path))
    
    def test_initialization(self):
        """Test the initialization of DatabaseAgent."""
        self.assertEqual(self.agent.config, self.mock_config)
        self.assertEqual(self.agent.db_manager, self.mock_db_manager_instance)
        self.assertEqual(self.agent.llm_client, self.mock_llm_client_instance)
        self.assertEqual(self.agent.sql_generator, self.mock_sql_generator_instance)
        self.assertEqual(self.agent.console, self.mock_console_instance)
        self.assertFalse(self.agent.verbose)
    
    def test_analyze_database(self):
        """Test the analyze_database method."""
        # Configure the mock
        mock_db_info = {
            "tables": [
                {
                    "name": "test_table",
                    "columns": [
                        {"name": "id", "type": "INTEGER"},
                        {"name": "name", "type": "TEXT"},
                        {"name": "value", "type": "TEXT"}
                    ]
                }
            ]
        }
        self.mock_db_manager_instance.get_database_info.return_value = mock_db_info
        
        # Call the method
        result = self.agent.analyze_database()
        
        # Verify the result
        self.assertEqual(result, mock_db_info)
        self.mock_db_manager_instance.get_database_info.assert_called_once()
    
    def test_analyze_database_error(self):
        """Test analyze_database method when an error occurs."""
        # Configure the mock to raise an exception
        self.mock_db_manager_instance.get_database_info.side_effect = DatabaseError("Test error")
        
        # Call the method
        result = self.agent.analyze_database()
        
        # Verify the result
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Test error")
    
    def test_execute_operation(self):
        """Test the execute_operation method."""
        # Configure the mocks
        mock_db_info = {
            "tables": [
                {
                    "name": "test_table",
                    "columns": [
                        {"name": "id", "type": "INTEGER"},
                        {"name": "name", "type": "TEXT"},
                        {"name": "value", "type": "TEXT"}
                    ]
                }
            ]
        }
        self.mock_db_manager_instance.get_database_info.return_value = mock_db_info
        
        mock_sql_response = MagicMock()
        mock_sql_response.sql = "SELECT * FROM test_table"
        mock_sql_response.explanation = "This is a test explanation"
        
        self.mock_sql_generator_instance.generate_sql.return_value = mock_sql_response
        
        # Configure execute_sql to return success
        mock_execute_result = {
            "success": True,
            "columns": ["id", "name", "value"],
            "data": [(1, "test_entry", "Test value")],
            "affected_rows": None
        }
        self.mock_db_manager_instance.execute_sql.return_value = mock_execute_result
        
        # Mock the console input to return 'yes'
        self.mock_console_instance.input.return_value = "yes"
        
        # Call the method
        operation_nl = "Show me all data from test_table"
        result = self.agent.execute_operation(operation_nl)
        
        # Verify the result
        self.assertTrue(result["success"])
        self.assertIn("Operation completed successfully", result["message"])
        self.assertIn("details", result)
        self.assertIn("statement_1", result["details"])
        
        # Verify method calls
        self.mock_db_manager_instance.get_database_info.assert_called()
        self.mock_sql_generator_instance.generate_sql.assert_called_with(operation_nl, mock_db_info)
        self.mock_db_manager_instance.execute_sql.assert_called_with("SELECT * FROM test_table")
    
    def test_execute_operation_cancelled(self):
        """Test the execute_operation method when cancelled by user."""
        # Configure the mocks
        mock_db_info = {"tables": []}
        self.mock_db_manager_instance.get_database_info.return_value = mock_db_info
        
        mock_sql_response = MagicMock()
        mock_sql_response.sql = "SELECT * FROM test_table"
        mock_sql_response.explanation = "This is a test explanation"
        
        self.mock_sql_generator_instance.generate_sql.return_value = mock_sql_response
        
        # Mock the console input to return 'no'
        self.mock_console_instance.input.return_value = "no"
        
        # Call the method
        operation_nl = "Show me all data from test_table"
        result = self.agent.execute_operation(operation_nl)
        
        # Verify the result
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Operation cancelled by user")
        
        # Verify that execute_sql was not called
        self.mock_db_manager_instance.execute_sql.assert_not_called()
    
    def test_execute_operation_sql_generation_error(self):
        """Test execute_operation when SQL generation fails."""
        # Configure the mocks
        mock_db_info = {"tables": []}
        self.mock_db_manager_instance.get_database_info.return_value = mock_db_info
        
        # Make generate_sql raise an error
        self.mock_sql_generator_instance.generate_sql.side_effect = SQLGenerationError("Test SQL generation error")
        
        # Call the method
        operation_nl = "Show me all data from non_existent_table"
        result = self.agent.execute_operation(operation_nl)
        
        # Verify the result
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Test SQL generation error")
    
    def test_analyze_error(self):
        """Test the _analyze_error method."""
        # Test unique constraint error
        error_msg = "UNIQUE constraint failed: users.id"
        error_type, error_details = self.agent._analyze_error(error_msg)
        
        self.assertEqual(error_type, "unique_constraint")
        self.assertEqual(error_details.get("table"), "users")
        self.assertEqual(error_details.get("column"), "id")
        
        # Test foreign key constraint error
        error_msg = "FOREIGN KEY constraint failed"
        error_type, error_details = self.agent._analyze_error(error_msg)
        
        self.assertEqual(error_type, "foreign_key_constraint")
        
        # Test table not exists error
        error_msg = "no such table: non_existent_table"
        error_type, error_details = self.agent._analyze_error(error_msg)
        
        self.assertEqual(error_type, "table_not_exists")
        self.assertEqual(error_details.get("table"), "non_existent_table")
    
    def test_suggest_error_fix(self):
        """Test the _suggest_error_fix method."""
        # Test unique constraint error fix
        error_type = "unique_constraint"
        error_details = {"table": "users", "column": "id"}
        sql = "INSERT INTO users (id, name) VALUES (1, 'John')"
        
        suggestion = self.agent._suggest_error_fix(error_type, error_details, sql)
        
        self.assertIn("duplicate values", suggestion)
        self.assertIn("users.id", suggestion)
        self.assertIn("INSERT OR IGNORE/REPLACE", suggestion)
        
        # Test table not exists error fix
        error_type = "table_not_exists"
        error_details = {"table": "non_existent_table"}
        sql = "SELECT * FROM non_existent_table"
        
        suggestion = self.agent._suggest_error_fix(error_type, error_details, sql)
        
        self.assertIn("table 'non_existent_table' doesn't exist", suggestion.lower())
        self.assertIn("create it first", suggestion.lower())
    
    def test_fix_unique_constraint_error(self):
        """Test the _fix_unique_constraint_error method."""
        # Test fixing INSERT statement
        sql = "INSERT INTO users (id, name) VALUES (1, 'John')"
        table = "users"
        column = "id"
        
        fixed_sql = self.agent._fix_unique_constraint_error(sql, table, column)
        
        self.assertEqual(fixed_sql, "INSERT OR REPLACE INTO users (id, name) VALUES (1, 'John')")
        
        # Test with a non-INSERT statement (should return unchanged)
        sql = "SELECT * FROM users"
        fixed_sql = self.agent._fix_unique_constraint_error(sql, table, column)
        
        self.assertEqual(fixed_sql, sql)
    
    def test_extract_table_name(self):
        """Test the _extract_table_name method."""
        # Test simple SELECT
        sql = "SELECT * FROM users"
        table_name = self.agent._extract_table_name(sql)
        self.assertEqual(table_name, "users")
        
        # Test with semicolon
        sql = "SELECT * FROM users;"
        table_name = self.agent._extract_table_name(sql)
        self.assertEqual(table_name, "users")
        
        # Test with WHERE clause
        sql = "SELECT * FROM users WHERE id = 1"
        table_name = self.agent._extract_table_name(sql)
        self.assertEqual(table_name, "users")
        
        # Test without FROM clause
        sql = "INSERT INTO users (id, name) VALUES (1, 'John')"
        table_name = self.agent._extract_table_name(sql)
        self.assertEqual(table_name, "")

if __name__ == '__main__':
    unittest.main()
