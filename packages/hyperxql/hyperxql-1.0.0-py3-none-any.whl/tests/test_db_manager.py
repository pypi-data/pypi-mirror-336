"""
Tests for the database manager module.
"""

import pytest
from unittest.mock import patch, MagicMock, call

from hyperxql.db_manager import DatabaseManager
from hyperxql.exceptions import DatabaseError

@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    config = MagicMock()
    config.db_config = {
        "db_type": "sqlite",
        "database": ":memory:"
    }
    return config

@pytest.fixture
def mock_engine():
    """Create a mock SQLAlchemy engine."""
    engine = MagicMock()
    connection = MagicMock()
    engine.connect.return_value = connection
    return engine

@patch("hyperxql.db_manager.create_engine")
def test_create_engine_sqlite(mock_create_engine, mock_config):
    """Test engine creation with SQLite."""
    mock_create_engine.return_value = MagicMock()
    
    db_manager = DatabaseManager(mock_config)
    
    mock_create_engine.assert_called_once()
    args, kwargs = mock_create_engine.call_args
    assert "sqlite:///:memory:" in args[0]
    
    # Test with missing configuration
    mock_config.db_config = {}
    with pytest.raises(DatabaseError, match="Database not configured"):
        DatabaseManager(mock_config)

@patch("hyperxql.db_manager.create_engine")
def test_create_engine_postgresql(mock_create_engine):
    """Test engine creation with PostgreSQL."""
    mock_create_engine.return_value = MagicMock()
    
    # Test with connection string
    config = MagicMock()
    config.db_config = {
        "db_type": "postgresql",
        "connection_string": "postgresql://user:pass@localhost/testdb"
    }
    
    db_manager = DatabaseManager(config)
    
    mock_create_engine.assert_called_once()
    args, kwargs = mock_create_engine.call_args
    assert "postgresql://user:pass@localhost/testdb" in args[0]
    
    # Test with individual parameters
    mock_create_engine.reset_mock()
    config.db_config = {
        "db_type": "postgresql",
        "host": "localhost",
        "port": "5432",
        "database": "testdb",
        "user": "testuser",
        "password": "testpass"
    }
    
    db_manager = DatabaseManager(config)
    
    mock_create_engine.assert_called_once()
    args, kwargs = mock_create_engine.call_args
    assert "postgresql://testuser:testpass@localhost:5432/testdb" in args[0]

@patch("hyperxql.db_manager.create_engine")
def test_create_engine_mysql(mock_create_engine):
    """Test engine creation with MySQL."""
    mock_create_engine.return_value = MagicMock()
    
    config = MagicMock()
    config.db_config = {
        "db_type": "mysql",
        "host": "localhost",
        "port": "3306",
        "database": "testdb",
        "user": "testuser",
        "password": "testpass"
    }
    
    db_manager = DatabaseManager(config)
    
    mock_create_engine.assert_called_once()
    args, kwargs = mock_create_engine.call_args
    assert "mysql+pymysql://testuser:testpass@localhost:3306/testdb" in args[0]

@patch("hyperxql.db_manager.create_engine")
def test_unsupported_db_type(mock_create_engine):
    """Test with unsupported database type."""
    config = MagicMock()
    config.db_config = {
        "db_type": "unsupported"
    }
    
    with pytest.raises(DatabaseError, match="Unsupported database type"):
        DatabaseManager(config)

@patch("hyperxql.db_manager.create_engine")
def test_execute_sql_select(mock_create_engine, mock_engine):
    """Test executing SELECT SQL query."""
    mock_create_engine.return_value = mock_engine
    
    config = MagicMock()
    config.db_config = {"db_type": "sqlite", "database": ":memory:"}
    
    db_manager = DatabaseManager(config)
    
    # Mock the connection and result
    connection = mock_engine.connect.return_value
    result = MagicMock()
    connection.execute.return_value = result
    
    # Set up the result for SELECT query
    result.keys.return_value = ["id", "name"]
    result.fetchall.return_value = [(1, "Alice"), (2, "Bob")]
    
    # Execute a SELECT query
    response = db_manager.execute_sql("SELECT * FROM users")
    
    # Verify the response
    assert response["success"] is True
    assert response["query_type"] == "select"
    assert response["columns"] == ["id", "name"]
    assert response["rows"] == [(1, "Alice"), (2, "Bob")]
    assert response["row_count"] == 2
    
    # Verify the SQL was executed
    connection.execute.assert_called_once()
    from sqlalchemy import text
    assert str(connection.execute.call_args[0][0]) == str(text("SELECT * FROM users"))

@patch("hyperxql.db_manager.create_engine")
def test_execute_sql_insert(mock_create_engine, mock_engine):
    """Test executing INSERT SQL query."""
    mock_create_engine.return_value = mock_engine
    
    config = MagicMock()
    config.db_config = {"db_type": "sqlite", "database": ":memory:"}
    
    db_manager = DatabaseManager(config)
    
    # Mock the connection and result
    connection = mock_engine.connect.return_value
    result = MagicMock()
    connection.execute.return_value = result
    
    # Set up the result for INSERT query
    result.rowcount = 1
    
    # Execute an INSERT query
    response = db_manager.execute_sql("INSERT INTO users (name) VALUES ('Alice')")
    
    # Verify the response
    assert response["success"] is True
    assert response["query_type"] == "insert"
    assert response["message"] == "1 row(s) affected."
    assert response["row_count"] == 1

@patch("hyperxql.db_manager.create_engine")
def test_execute_sql_create_table(mock_create_engine, mock_engine):
    """Test executing CREATE TABLE SQL query."""
    mock_create_engine.return_value = mock_engine
    
    config = MagicMock()
    config.db_config = {"db_type": "sqlite", "database": ":memory:"}
    
    db_manager = DatabaseManager(config)
    
    # Mock the connection and result
    connection = mock_engine.connect.return_value
    result = MagicMock()
    connection.execute.return_value = result
    
    # Execute a CREATE TABLE query
    response = db_manager.execute_sql("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    
    # Verify the response
    assert response["success"] is True
    assert response["query_type"] == "create_table"
    assert response["message"] == "Table 'users' created successfully."

@patch("hyperxql.db_manager.create_engine")
def test_execute_sql_error(mock_create_engine, mock_engine):
    """Test SQL execution error."""
    mock_create_engine.return_value = mock_engine
    
    config = MagicMock()
    config.db_config = {"db_type": "sqlite", "database": ":memory:"}
    
    db_manager = DatabaseManager(config)
    
    # Mock the connection to raise an error
    connection = mock_engine.connect.return_value
    connection.execute.side_effect = Exception("SQL error")
    
    # Execute a query that will raise an error
    with pytest.raises(DatabaseError, match="Error executing SQL"):
        db_manager.execute_sql("SELECT * FROM nonexistent_table")

@patch("hyperxql.db_manager.create_engine")
def test_determine_query_type(mock_create_engine, mock_engine):
    """Test query type determination."""
    mock_create_engine.return_value = mock_engine
    
    config = MagicMock()
    config.db_config = {"db_type": "sqlite", "database": ":memory:"}
    
    db_manager = DatabaseManager(config)
    
    # Test various query types
    assert db_manager._determine_query_type("SELECT * FROM users") == "select"
    assert db_manager._determine_query_type("INSERT INTO users VALUES (1, 'Alice')") == "insert"
    assert db_manager._determine_query_type("UPDATE users SET name = 'Bob' WHERE id = 1") == "update"
    assert db_manager._determine_query_type("DELETE FROM users WHERE id = 1") == "delete"
    assert db_manager._determine_query_type("CREATE TABLE users (id INT, name TEXT)") == "create_table"
    assert db_manager._determine_query_type("ALTER TABLE users ADD COLUMN email TEXT") == "alter_table"
    assert db_manager._determine_query_type("DROP TABLE users") == "drop_table"
    assert db_manager._determine_query_type("CREATE DATABASE testdb") == "create_database"
    assert db_manager._determine_query_type("PRAGMA table_info(users)") == "other"

@patch("hyperxql.db_manager.create_engine")
def test_extract_table_name(mock_create_engine, mock_engine):
    """Test table name extraction."""
    mock_create_engine.return_value = mock_engine
    
    config = MagicMock()
    config.db_config = {"db_type": "sqlite", "database": ":memory:"}
    
    db_manager = DatabaseManager(config)
    
    # Test CREATE TABLE
    assert db_manager._extract_table_name("CREATE TABLE users (id INT)", "create") == "users"
    assert db_manager._extract_table_name("CREATE TABLE IF NOT EXISTS users (id INT)", "create") == "users"
    assert db_manager._extract_table_name("CREATE TABLE `users` (id INT)", "create") == "users"
    assert db_manager._extract_table_name("CREATE TABLE \"users\" (id INT)", "create") == "users"
    
    # Test ALTER TABLE
    assert db_manager._extract_table_name("ALTER TABLE users ADD COLUMN email TEXT", "alter") == "users"
    
    # Test DROP TABLE
    assert db_manager._extract_table_name("DROP TABLE users", "drop") == "users"
    assert db_manager._extract_table_name("DROP TABLE IF EXISTS users", "drop") == "users"
    
    # Test invalid operation
    assert db_manager._extract_table_name("SELECT * FROM users", "invalid") == ""

@patch("hyperxql.db_manager.create_engine")
@patch("hyperxql.db_manager.inspect")
def test_get_database_info(mock_inspect, mock_create_engine, mock_engine):
    """Test getting database information."""
    mock_create_engine.return_value = mock_engine
    
    config = MagicMock()
    config.db_config = {
        "db_type": "sqlite",
        "database": "test.db"
    }
    
    # Set up mock inspector
    inspector = MagicMock()
    mock_inspect.return_value = inspector
    
    # Mock inspector methods
    inspector.get_table_names.return_value = ["users", "posts"]
    
    # Mock column data
    users_columns = [
        {"name": "id", "type": "INTEGER", "nullable": False},
        {"name": "name", "type": "TEXT", "nullable": True}
    ]
    posts_columns = [
        {"name": "id", "type": "INTEGER", "nullable": False},
        {"name": "title", "type": "TEXT", "nullable": False},
        {"name": "user_id", "type": "INTEGER", "nullable": True}
    ]
    
    def get_columns(table_name):
        if table_name == "users":
            return users_columns
        elif table_name == "posts":
            return posts_columns
        return []
    
    inspector.get_columns.side_effect = get_columns
    
    # Mock primary keys
    def get_pk_constraint(table_name):
        if table_name == "users":
            return {"constrained_columns": ["id"]}
        elif table_name == "posts":
            return {"constrained_columns": ["id"]}
        return {"constrained_columns": []}
    
    inspector.get_pk_constraint.side_effect = get_pk_constraint
    
    # Mock foreign keys
    def get_foreign_keys(table_name):
        if table_name == "posts":
            return [{"constrained_columns": ["user_id"], "referred_table": "users", "referred_columns": ["id"]}]
        return []
    
    inspector.get_foreign_keys.side_effect = get_foreign_keys
    
    # Create database manager and get info
    db_manager = DatabaseManager(config)
    db_info = db_manager.get_database_info()
    
    # Verify the result
    assert db_info["db_type"] == "sqlite"
    assert db_info["db_name"] == "test.db"
    assert len(db_info["tables"]) == 2
    
    # Check users table
    users_table = next(t for t in db_info["tables"] if t["name"] == "users")
    assert len(users_table["columns"]) == 2
    assert users_table["columns"][0]["name"] == "id"
    assert users_table["columns"][0]["is_primary_key"] is True
    
    # Check posts table
    posts_table = next(t for t in db_info["tables"] if t["name"] == "posts")
    assert len(posts_table["columns"]) == 3
    assert posts_table["columns"][2]["name"] == "user_id"
    assert posts_table["columns"][2]["is_foreign_key"] is True
    assert posts_table["columns"][2]["references"] == "users.id"
    
    # Test error handling
    inspector.get_table_names.side_effect = Exception("DB error")
    with pytest.raises(DatabaseError, match="Failed to get database information"):
        db_manager.get_database_info()
