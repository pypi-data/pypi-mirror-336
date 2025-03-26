"""
Utility to verify and create the database from existing configuration.
This script can be run directly to check if the database exists and create it if needed.
"""

import os
import sys
import json
import logging
import sqlite3
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("hyperxql.verify_db")

# Initialize rich console for output
console = Console()

def find_hyperxql_config():
    """Find the HyperXQL configuration file."""
    # Standard config location in user's home directory
    home_config = Path.home() / ".hyperxql" / "config.json"
    if home_config.exists():
        return home_config
    
    # Try current working directory
    cwd_config = Path.cwd() / ".hyperxql" / "config.json"
    if cwd_config.exists():
        return cwd_config
        
    # Try parent directory of current script
    script_dir = Path(__file__).resolve().parent
    parent_config = script_dir.parent / ".hyperxql" / "config.json"
    if parent_config.exists():
        return parent_config
    
    return None

def load_config(config_path):
    """Load configuration from file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return None

def create_sqlite_database(db_path):
    """Create SQLite database with basic structure."""
    try:
        # Ensure parent directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Try to create the database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create a test table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            value TEXT
        )
        ''')
        
        # Add a sample record
        cursor.execute('''
        INSERT INTO test_table (name, value) 
        VALUES (?, ?)
        ''', ('verify_db_test', 'Database created by verify_db.py'))
        
        # Commit changes and close
        conn.commit()
        conn.close()
        
        # Verify creation
        if db_path.exists():
            return True
        else:
            logger.error(f"Database file still doesn't exist at: {db_path}")
            return False
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        return False

def create_current_dir_database():
    """Create a database in the current directory."""
    try:
        db_path = Path.cwd() / "hyperxql.db"
        logger.info(f"Creating database in current directory: {db_path}")
        
        if create_sqlite_database(db_path):
            # Create a minimal config file
            config = {
                "db_config": {
                    "db_type": "sqlite",
                    "database": str(db_path.absolute())
                }
            }
            
            # Save this config to current directory
            config_dir = Path.cwd() / ".hyperxql"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_path = config_dir / "config.json"
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
                
            logger.info(f"Created new config at: {config_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error creating current directory database: {e}")
        return False

def main():
    """Main function to verify the database."""
    console.print(Panel.fit(
        "HyperXQL Database Verification Utility", 
        title="HyperXQL", 
        border_style="blue"
    ))
    
    # Find configuration
    config_path = find_hyperxql_config()
    if not config_path:
        console.print("[yellow]No HyperXQL configuration found.[/yellow]")
        console.print("Would you like to create a SQLite database in the current directory?")
        response = input("Create database here? (y/n): ").strip().lower()
        
        if response == 'y':
            if create_current_dir_database():
                console.print("[bold green]✓[/bold green] Database created successfully in current directory.")
                return True
            else:
                console.print("[bold red]✗[/bold red] Failed to create database.")
                return False
        else:
            console.print("Please run 'hyperxql init' to set up a configuration first.")
            return False
    
    console.print(f"[blue]Found configuration at:[/blue] {config_path}")
    
    # Load configuration
    config = load_config(config_path)
    if not config:
        console.print("[bold red]✗[/bold red] Could not load configuration.")
        return False
    
    # Check database configuration
    db_config = config.get("db_config", {})
    db_type = db_config.get("db_type")
    
    if not db_type:
        console.print("[bold red]✗[/bold red] No database type specified in configuration.")
        return False
    
    console.print(f"[blue]Database type:[/blue] {db_type}")
    
    # Handle SQLite database
    if db_type == "sqlite":
        db_path_str = db_config.get("database")
        if not db_path_str:
            console.print("[bold red]✗[/bold red] No database path specified in configuration.")
            return False
        
        # Convert to Path object
        db_path = Path(db_path_str).expanduser().resolve()
        console.print(f"[blue]Database path:[/blue] {db_path}")
        
        # Check if database exists
        if db_path.exists():
            # Verify it's a valid SQLite database
            try:
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                cursor.execute("PRAGMA integrity_check")
                result = cursor.fetchone()
                conn.close()
                
                if result and result[0] == "ok":
                    console.print("[bold green]✓[/bold green] Database exists and is valid.")
                    return True
                else:
                    console.print("[yellow]Database exists but may be corrupted. Creating a new one...[/yellow]")
            except Exception as e:
                console.print(f"[yellow]Error verifying database: {e}[/yellow]")
                console.print("[yellow]Attempting to create a new database...[/yellow]")
        else:
            console.print("[yellow]Database file does not exist. Creating it now...[/yellow]")
        
        # Create database
        if create_sqlite_database(db_path):
            console.print(f"[bold green]✓[/bold green] Database created successfully at: {db_path}")
            return True
        else:
            console.print(f"[bold red]✗[/bold red] Failed to create database at: {db_path}")
            
            # Try creating in current directory instead
            console.print("[yellow]Attempting to create database in current directory...[/yellow]")
            current_dir_db = Path.cwd() / "hyperxql.db"
            
            if create_sqlite_database(current_dir_db):
                console.print(f"[bold green]✓[/bold green] Database created in current directory: {current_dir_db}")
                console.print("[yellow]Consider updating your configuration to use this database.[/yellow]")
                return True
            
            return False
    else:
        console.print(f"[blue]Non-SQLite database type ({db_type}) detected.[/blue]")
        console.print("[yellow]This utility only checks SQLite databases.[/yellow]")
        console.print("[yellow]Please ensure your database server is running and configured correctly.[/yellow]")
        return True

if __name__ == "__main__":
    success = main()
    if success:
        console.print("\n[bold green]Database verification completed successfully.[/bold green]")
        sys.exit(0)
    else:
        console.print("\n[bold red]Database verification failed.[/bold red]")
        sys.exit(1)
