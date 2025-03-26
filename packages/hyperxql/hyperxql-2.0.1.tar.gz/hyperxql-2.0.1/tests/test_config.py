"""
Tests for the Config class and related configuration functions.
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
from pathlib import Path
import json
import tempfile

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hyperxql.config import Config, initialize_database
from hyperxql.exceptions import ConfigurationError

class TestConfig(unittest.TestCase):
    """Test cases for the Config class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_config_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w')
        self.temp_config_path = Path(self.temp_config_file.name)
        
        # Write test configuration
        config_data = {
            "llm_provider": "test_provider",
            "test_provider_api_key": "test_key",
            "test_provider_model": "test_model",
            "db_config": {
                "db_type": "sqlite",
                "database": "/path/to/database.db"
            }
        }
        json.dump(config_data, self.temp_config_file)
        self.temp_config_file.close()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.temp_config_path.exists():
            os.unlink(str(self.temp_config_path))
    
    def test_load_config(self):
        """Test loading configuration from file."""
        config = Config(self.temp_config_path)
        
        self.assertEqual(config.llm_provider, "test_provider")
        self.assertEqual(config.db_config["db_type"], "sqlite")
        self.assertEqual(config.db_config["database"], "/path/to/database.db")
    
    def test_load_config_file_not_found(self):
        """Test loading configuration when file doesn't exist."""
        non_existent_path = Path("/non/existent/path/config.json")
        
        with self.assertRaises(ConfigurationError) as context:
            Config(non_existent_path)
        
        self.assertIn("Configuration file not found", str(context.exception))
    
    def test_load_config_invalid_json(self):
        """Test loading configuration with invalid JSON."""
        invalid_json_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        invalid_json_path = Path(invalid_json_file.name)
        
        # Write invalid JSON
        invalid_json_file.write(b"{invalid json")
        invalid_json_file.close()
        
        try:
            with self.assertRaises(ConfigurationError) as context:
                Config(invalid_json_path)
            
            self.assertIn("Invalid JSON", str(context.exception))
        finally:
            if invalid_json_path.exists():
                os.unlink(str(invalid_json_path))
    
    def test_update_config(self):
        """Test updating configuration."""
        config = Config(self.temp_config_path)
        
        # Update configuration
        new_config = {
            "llm_provider": "new_provider",
            "db_config": {
                "db_type": "postgresql",
                "host": "localhost"
            }
        }
        config.update_config(new_config)
        
        # Reload configuration to verify it was saved
        updated_config = Config(self.temp_config_path)
        
        self.assertEqual(updated_config.llm_provider, "new_provider")
        self.assertEqual(updated_config.db_config["db_type"], "postgresql")
        self.assertEqual(updated_config.db_config["host"], "localhost")
        
        # The original database path should still be present
        self.assertEqual(updated_config.db_config["database"], "/path/to/database.db")
    
    def test_environment_variables_override(self):
        """Test that environment variables override configuration values."""
        # Set environment variables
        os.environ["OPENAI_API_KEY"] = "env_api_key"
        os.environ["TOGETHER_API_KEY"] = "env_together_key"
        
        try:
            config = Config(self.temp_config_path)
            
            # Check that environment variables take precedence
            self.assertEqual(config.openai_api_key, "env_api_key")
            self.assertEqual(config.together_api_key, "env_together_key")
        finally:
            # Clean up environment variables
            if "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]
            if "TOGETHER_API_KEY" in os.environ:
                del os.environ["TOGETHER_API_KEY"]
    
    @patch('hyperxql.config.sqlite3')
    @patch('hyperxql.config.Path')
    def test_initialize_database(self, mock_path, mock_sqlite3):
        """Test initializing a SQLite database."""
        # Configure mocks
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.absolute.return_value = mock_path_instance
        mock_path_instance.parent.mkdir.return_value = None
        mock_path_instance.exists.return_value = True
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Configure access permissions
        mock_path_instance.parent.exists.return_value = True
        mock_os_access = patch('hyperxql.config.os.access', return_value=True).start()
        
        # Call the function
        result = initialize_database(Path("/path/to/database.db"))
        
        # Verify the result
        self.assertTrue(result)
        mock_path_instance.parent.mkdir.assert_called_with(parents=True, exist_ok=True)
        mock_sqlite3.connect.assert_called_with("/path/to/database.db")
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        
        # Clean up
        patch('hyperxql.config.os.access').stop()
    
    @patch('hyperxql.config.sqlite3')
    @patch('hyperxql.config.Path')
    def test_initialize_database_permission_error(self, mock_path, mock_sqlite3):
        """Test initializing a SQLite database with permission error."""
        # Configure mocks
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.absolute.return_value = mock_path_instance
        
        # Configure access permissions - not writable
        mock_os_access = patch('hyperxql.config.os.access', return_value=False).start()
        
        # Call the function
        result = initialize_database(Path("/path/to/database.db"))
        
        # Verify the result
        self.assertFalse(result)
        mock_sqlite3.connect.assert_not_called()
        
        # Clean up
        patch('hyperxql.config.os.access').stop()

if __name__ == '__main__':
    unittest.main()
