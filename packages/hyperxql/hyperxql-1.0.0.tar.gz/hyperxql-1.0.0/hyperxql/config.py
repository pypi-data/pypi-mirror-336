"""
Configuration module for HyperXQL.
Handles loading and saving configuration settings and API keys.
"""

import os
import json
from pathlib import Path
import click
from dotenv import load_dotenv
import getpass
from typing import Dict, Any, Optional

from .exceptions import ConfigurationError

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Configuration class for HyperXQL."""
    
    DEFAULT_CONFIG_DIR = Path.home() / ".hyperxql"
    DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.json"
    
    def __init__(self, config_file_path: Optional[Path] = None):
        """Initialize configuration from file."""
        self.config_file_path = config_file_path or self.DEFAULT_CONFIG_FILE
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if not self.config_file_path.exists():
            raise ConfigurationError(
                f"Configuration file not found at {self.config_file_path}. "
                "Run 'hyperxql init' to set up your configuration."
            )
        
        try:
            with open(self.config_file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ConfigurationError(f"Invalid JSON in configuration file: {self.config_file_path}")
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration: {str(e)}")
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            # Ensure the directory exists
            self.config_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            raise ConfigurationError(f"Error saving configuration: {str(e)}")
    
    @property
    def llm_provider(self) -> str:
        """Get the configured LLM provider."""
        return self.config.get("llm_provider", "")
    
    @property
    def openai_api_key(self) -> str:
        """Get the OpenAI API key."""
        # Try from environment first, then from config
        return os.environ.get("OPENAI_API_KEY") or self.config.get("openai_api_key", "")
    
    @property
    def together_api_key(self) -> str:
        """Get the Together AI API key."""
        # Try from environment first, then from config
        return os.environ.get("TOGETHER_API_KEY") or self.config.get("together_api_key", "")
    
    @property
    def openai_model(self) -> str:
        """Get the OpenAI model to use."""
        return self.config.get("openai_model", "gpt-4o")
    
    @property
    def together_model(self) -> str:
        """Get the Together AI model to use."""
        return self.config.get("together_model", "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free")
    
    @property
    def db_config(self) -> Dict[str, Any]:
        """Get the database configuration."""
        db_config = self.config.get("db_config", {})
        
        # Check for environment variables for database connection
        if "db_type" in db_config and db_config["db_type"] == "postgresql":
            # Try to get PostgreSQL connection info from environment variables
            if os.environ.get("DATABASE_URL"):
                db_config["connection_string"] = os.environ.get("DATABASE_URL")
            else:
                # Try individual components
                db_config["host"] = os.environ.get("PGHOST", db_config.get("host", ""))
                db_config["port"] = os.environ.get("PGPORT", db_config.get("port", ""))
                db_config["database"] = os.environ.get("PGDATABASE", db_config.get("database", ""))
                db_config["user"] = os.environ.get("PGUSER", db_config.get("user", ""))
                db_config["password"] = os.environ.get("PGPASSWORD", db_config.get("password", ""))
        
        return db_config
    
    def update_config(self, new_config: Dict[str, Any]):
        """Update configuration with new values."""
        self.config.update(new_config)
        self._save_config()


def initialize_config() -> Config:
    """Initialize or update HyperXQL configuration through interactive prompts."""
    config_path = Config.DEFAULT_CONFIG_FILE
    
    # Check if config file already exists
    config_exists = config_path.exists()
    
    if config_exists:
        try:
            config = Config()
            current_config = config.config
        except Exception:
            current_config = {}
    else:
        current_config = {}
    
    # Start with new config dictionary
    new_config = {}
    
    # LLM Provider selection
    click.echo("\n[1/3] LLM Provider Configuration")
    click.echo("------------------------------")
    
    default_provider = current_config.get("llm_provider", "openai")
    llm_provider = click.prompt(
        "Select LLM provider",
        type=click.Choice(["openai", "together"]),
        default=default_provider
    )
    new_config["llm_provider"] = llm_provider
    
    # API Key for selected provider
    if llm_provider == "openai":
        default_key = os.environ.get("OPENAI_API_KEY") or current_config.get("openai_api_key", "")
        api_key = click.prompt(
            "OpenAI API Key",
            default=default_key,
            hide_input=True,
            show_default=bool(default_key)
        )
        new_config["openai_api_key"] = api_key
        
        # Model selection for OpenAI
        default_model = current_config.get("openai_model", "gpt-4o")
        openai_model = click.prompt(
            "OpenAI Model",
            default=default_model,
            type=click.Choice(["gpt-4o", "gpt-3.5-turbo"])
        )
        new_config["openai_model"] = openai_model
        
    elif llm_provider == "together":
        default_key = os.environ.get("TOGETHER_API_KEY") or current_config.get("together_api_key", "")
        api_key = click.prompt(
            "Together AI API Key",
            default=default_key,
            hide_input=True,
            show_default=bool(default_key)
        )
        new_config["together_api_key"] = api_key
        
        # Model selection for Together AI
        together_models = [
            "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo-classifier",
            "mistralai/Mixtral-8x22B-Instruct-v0.1",
            "Qwen/Qwen2.5-Coder-32B-Instruct",
            "google/gemma-2b-it",
            "Gryphe/MythoMax-L2-13b",
            "togethercomputer/llama-2-70b-chat"
        ]
        default_model = current_config.get("together_model", "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free")
        together_model = click.prompt(
            "Together AI Model",
            type=click.Choice(together_models),
            default=default_model
        )
        new_config["together_model"] = together_model
    
    # Database configuration
    click.echo("\n[2/3] Database Configuration")
    click.echo("-------------------------")
    
    db_types = ["sqlite", "postgresql", "mysql"]
    default_db_type = current_config.get("db_config", {}).get("db_type", "sqlite")
    db_type = click.prompt(
        "Database Type",
        type=click.Choice(db_types),
        default=default_db_type
    )
    
    db_config = {"db_type": db_type}
    
    if db_type == "sqlite":
        default_path = current_config.get("db_config", {}).get("database", "hyperxql.db")
        db_path = click.prompt(
            "SQLite Database Path",
            default=default_path
        )
        db_config["database"] = db_path
        
    elif db_type == "postgresql":
        # Use environment variables if available
        if os.environ.get("DATABASE_URL"):
            click.echo("Using PostgreSQL connection from DATABASE_URL environment variable.")
            db_config["connection_string"] = os.environ.get("DATABASE_URL")
        elif all(os.environ.get(var) for var in ["PGHOST", "PGDATABASE", "PGUSER", "PGPASSWORD"]):
            click.echo("Using PostgreSQL connection from PG* environment variables.")
            db_config["host"] = os.environ.get("PGHOST")
            db_config["port"] = os.environ.get("PGPORT", "5432")
            db_config["database"] = os.environ.get("PGDATABASE")
            db_config["user"] = os.environ.get("PGUSER")
            db_config["password"] = os.environ.get("PGPASSWORD")
        else:
            # Prompt for connection details
            db_config["host"] = click.prompt(
                "PostgreSQL Host",
                default=current_config.get("db_config", {}).get("host", "localhost")
            )
            db_config["port"] = click.prompt(
                "PostgreSQL Port",
                default=current_config.get("db_config", {}).get("port", "5432")
            )
            db_config["database"] = click.prompt(
                "PostgreSQL Database Name",
                default=current_config.get("db_config", {}).get("database", "postgres")
            )
            db_config["user"] = click.prompt(
                "PostgreSQL Username",
                default=current_config.get("db_config", {}).get("user", "postgres")
            )
            db_config["password"] = getpass.getpass(
                f"PostgreSQL Password (Enter to keep existing): "
            ) or current_config.get("db_config", {}).get("password", "")
            
    elif db_type == "mysql":
        db_config["host"] = click.prompt(
            "MySQL Host",
            default=current_config.get("db_config", {}).get("host", "localhost")
        )
        db_config["port"] = click.prompt(
            "MySQL Port",
            default=current_config.get("db_config", {}).get("port", "3306")
        )
        db_config["database"] = click.prompt(
            "MySQL Database Name",
            default=current_config.get("db_config", {}).get("database", "mysql")
        )
        db_config["user"] = click.prompt(
            "MySQL Username",
            default=current_config.get("db_config", {}).get("user", "root")
        )
        db_config["password"] = getpass.getpass(
            f"MySQL Password (Enter to keep existing): "
        ) or current_config.get("db_config", {}).get("password", "")
    
    new_config["db_config"] = db_config
    
    # Advanced options
    click.echo("\n[3/3] Advanced Options")
    click.echo("-------------------")
    
    default_execution = current_config.get("auto_execute", True)
    auto_execute = click.confirm(
        "Automatically execute generated SQL? (Set to False for review-only mode)",
        default=default_execution
    )
    new_config["auto_execute"] = auto_execute
    
    # Save the configuration
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, "w") as f:
        # Merge with existing config if updating
        if config_exists:
            final_config = current_config.copy()
            final_config.update(new_config)
        else:
            final_config = new_config
        
        json.dump(final_config, f, indent=2)
    
    return Config(config_path)
