"""
CLI interface for HyperXQL.
Provides commands for initializing and interacting with the database using natural language.
"""

import os
import sys
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import box
import logging
from pathlib import Path
from rich.table import Table
from rich.prompt import Confirm  # Add Confirm import
import subprocess
import importlib.util
import webbrowser
import time
import signal
import threading
import json  # Make sure json is imported

from hyperxql.config import Config, initialize_config
from hyperxql.llm_client import LLMClient
from hyperxql.db_manager import DatabaseManager
from hyperxql.sql_generator import SQLGenerator
from hyperxql.exceptions import (
    ConfigurationError, 
    LLMAPIError, 
    DatabaseError,
    SQLGenerationError
)
from hyperxql.utils import get_current_db_info
from .database_analyzer import DatabaseAnalyzer
from .query_optimizer import QueryOptimizer

# Import version information
from hyperxql import __version__

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("hyperxql")

# Initialize rich console for pretty output
console = Console()

def print_banner():
    """Print HyperXQL banner."""
    banner = f"""
    ╔═══════════════════════════════════════════════════╗
    ║                   HyperXQL v{__version__}                     ║
    ║ Natural Language to SQL - Powered by LLM          ║
    ╚═══════════════════════════════════════════════════╝
    """
    console.print(Panel.fit(banner, box=box.ROUNDED))

@click.group()
@click.version_option(version=__version__)
def cli():
    """
    HyperXQL - Natural Language to SQL Database Operations
    
    This CLI tool allows non-technical users to perform database operations
    using natural language, powered by LLMs.
    """
    pass

# Update the init command to verify database creation and display more details

@cli.command()
def init():
    """Initialize HyperXQL configuration."""
    print_banner()
    console.print("\n[bold green]Welcome to HyperXQL setup![/bold green]\n")
    
    try:
        config = initialize_config()
        
        # Import init_database to create the database file explicitly
        from hyperxql.config import initialize_database
        from pathlib import Path
        
        # Get the configured database path for SQLite
        if config.db_config.get("db_type") == "sqlite":
            db_path_str = config.db_config.get("database")
            
            if db_path_str:
                db_path = Path(db_path_str).expanduser().resolve()
                
                # Verify the database file exists
                if not db_path.exists():
                    # Initialize the database explicitly
                    with console.status("[bold yellow]Database file not found. Creating now...[/bold yellow]", spinner="dots"):
                        if initialize_database(db_path):
                            console.print(f"[bold green]✓[/bold green] Database initialized at: [cyan]{db_path}[/cyan]")
                        else:
                            console.print(f"[bold red]![/bold red] Failed to create database at: [cyan]{db_path}[/cyan]")
                            
                            # Try to create in the current directory
                            current_db = Path.cwd() / "hyperxql.db"
                            if initialize_database(current_db):
                                console.print(f"[bold green]✓[/bold green] Created database in current directory: [cyan]{current_db}[/cyan]")
                                
                                # Update config to use this database
                                if click.confirm("Update configuration to use this database?", default=True):
                                    config.update_config({"db_config": {"db_type": "sqlite", "database": str(current_db.absolute())}})
                                    console.print("[green]Configuration updated to use the new database location.[/green]")
                            else:
                                console.print("[yellow]Please run: python verify_database.py to create a working database[/yellow]")
                else:
                    # Database exists, confirm to user
                    console.print(f"[bold green]✓[/bold green] Database already exists at: [cyan]{db_path}[/cyan]")
                    # Check if it's writable
                    try:
                        import sqlite3
                        conn = sqlite3.connect(str(db_path))
                        conn.execute("SELECT 1")
                        conn.close()
                        console.print("[green]Database is accessible and ready to use.[/green]")
                    except Exception as db_err:
                        console.print(f"[yellow]Warning: Database exists but may not be accessible: {str(db_err)}[/yellow]")
                        
                        # Try to find a working database
                        current_db = Path.cwd() / "hyperxql.db"
                        if current_db.exists():
                            if click.confirm(f"Use existing database at {current_db} instead?", default=True):
                                config.update_config({"db_config": {"db_type": "sqlite", "database": str(current_db.absolute())}})
                                console.print("[green]Configuration updated to use the database in current directory.[/green]")
        
        console.print("[bold green]✓[/bold green] Configuration completed successfully!")
        console.print(f"Your settings are saved to: [cyan]{config.config_file_path}[/cyan]")
        console.print("\nTo use HyperXQL, run: [cyan]hyperxql query [YOUR NATURAL LANGUAGE COMMAND][/cyan]")
    except ConfigurationError as e:
        console.print(f"[bold red]Error during configuration:[/bold red] {str(e)}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {str(e)}")
        logger.exception("Unexpected error during initialization")
        sys.exit(1)

@cli.command()
@click.argument("query", nargs=-1)
@click.option("--optimize", is_flag=True, help="Optimize the generated SQL for performance")
@click.option("--validate", is_flag=True, help="Validate the generated SQL against schema")
@click.option("--suggest-indexes", is_flag=True, help="Suggest indexes for the query")
@click.option("--refresh-schema", is_flag=True, help="Force refresh of database schema")
def query(query, optimize, validate, suggest_indexes, refresh_schema):
    """Execute a natural language database query."""
    print_banner()
    
    if not query:
        console.print("[bold yellow]Please provide a natural language query.[/bold yellow]")
        console.print("Example: [cyan]hyperxql query create a database of users with name and email fields[/cyan]")
        return
    
    # Join all arguments to form the complete query
    query_text = " ".join(query)
    
    try:
        # Load configuration
        config = Config()
        
        # Set up LLM client
        llm_client = LLMClient(config)
        
        # Set up database manager
        db_manager = DatabaseManager(config)
        
        # Set up database analyzer if connected
        db_analyzer = None
        db_info = None
        
        if db_manager.is_connected():
            try:
                db_analyzer = DatabaseAnalyzer(db_manager.engine)
                db_info = db_analyzer.get_full_database_info(refresh=refresh_schema)
                
                # Show schema visualization summary
                table_count = len(db_info.get('tables', []))
                relationship_count = len(db_info.get('explicit_relationships', [])) + len(db_info.get('implicit_relationships', []))
                
                console.print(Panel.fit(
                    f"[bold]Database Schema:[/bold] {table_count} tables, {relationship_count} relationships detected", 
                    title="Schema Analysis", 
                    border_style="green"
                ))
            except Exception as e:
                console.print(f"[yellow]Warning: Could not analyze database schema: {str(e)}[/yellow]")
        
        # Create SQL generator with analyzer
        sql_generator = SQLGenerator(llm_client, db_analyzer)
        
        # Show current database info (if connected)
        db_connection_info = get_current_db_info(config)
        if db_connection_info:
            console.print(Panel.fit(
                f"[bold]Connected to:[/bold] {db_connection_info}", 
                title="Database Connection", 
                border_style="green"
            ))
        
        # Generate SQL from natural language
        console.print(f"\n[bold cyan]Generating SQL for:[/bold cyan] {query_text}")
        with console.status("[bold green]Thinking...[/bold green]", spinner="dots"):
            sql_response = sql_generator.generate_sql(query_text, db_info)
        
        # Display the generated SQL
        console.print(Panel.fit(
            sql_response.sql, 
            title="Generated SQL", 
            border_style="blue"
        ))
        
        # Display explanation
        console.print(Panel.fit(
            sql_response.explanation, 
            title="Explanation", 
            border_style="cyan"
        ))
        
        # Optimize the query if requested
        if optimize and db_info:
            console.print("\n[bold]Optimizing query...[/bold]")
            with console.status("[bold green]Optimizing...[/bold green]", spinner="dots"):
                optimizer = QueryOptimizer(llm_client)
                optimization_result = optimizer.optimize_query(sql_response.sql, db_info)
            
            # Display optimization results
            if optimization_result.get("optimized_sql") != sql_response.sql:
                console.print(Panel.fit(
                    optimization_result["optimized_sql"], 
                    title="Optimized SQL", 
                    border_style="green"
                ))
                
                console.print(Panel.fit(
                    optimization_result["explanation"], 
                    title="Optimization Explanation", 
                    border_style="green"
                ))
                
                # Update the SQL to use optimized version
                sql_response.sql = optimization_result["optimized_sql"]
            else:
                console.print("[yellow]No optimizations needed or possible for this query.[/yellow]")
        
        # Validate SQL if requested
        if validate and db_info:
            console.print("\n[bold]Validating SQL...[/bold]")
            with console.status("[bold green]Validating...[/bold green]", spinner="dots"):
                validation_result = sql_generator.validate_sql(sql_response.sql, db_info)
            
            # Display validation results
            if validation_result.get("valid") is True:
                console.print("[green]✓ SQL is valid against the current schema[/green]")
            elif validation_result.get("valid") is False:
                console.print("[red]✗ SQL validation found issues:[/red]")
                
                if validation_result.get("errors"):
                    console.print("[bold red]Errors:[/bold red]")
                    for error in validation_result["errors"]:
                        console.print(f"  • [red]{error}[/red]")
                
                if validation_result.get("warnings"):
                    console.print("[bold yellow]Warnings:[/bold yellow]")
                    for warning in validation_result["warnings"]:
                        console.print(f"  • [yellow]{warning}[/yellow]")
                
                if validation_result.get("suggestions"):
                    console.print("[bold cyan]Suggestions:[/bold cyan]")
                    for suggestion in validation_result["suggestions"]:
                        console.print(f"  • [cyan]{suggestion}[/cyan]")
            else:
                console.print("[yellow]Could not validate SQL against schema[/yellow]")
        
        # Suggest indexes if requested
        if suggest_indexes and db_info:
            console.print("\n[bold]Suggesting indexes...[/bold]")
            with console.status("[bold green]Analyzing...[/bold green]", spinner="dots"):
                optimizer = QueryOptimizer(llm_client)
                index_suggestions = optimizer.suggest_indexes(sql_response.sql, db_info)
            
            # Display index suggestions
            if index_suggestions:
                console.print(Panel.fit(
                    "\n".join([f"[bold]{i+1}. {suggestion['create_statement']}[/bold]\n   Reason: {suggestion['reason']}\n   Impact: {suggestion['impact']}" 
                             for i, suggestion in enumerate(index_suggestions)]), 
                    title="Index Suggestions", 
                    border_style="magenta"
                ))
            else:
                console.print("[yellow]No index suggestions available for this query.[/yellow]")
        
        # Execute the SQL if needed and user is connected to a database
        if sql_response.execute and db_manager.is_connected():
            execute = False
            
            # Query confirmation
            if db_info and any(metadata.get("query_type") in ["insert", "update", "delete", "create", "drop", "alter"]
                             for metadata in [sql_response.metadata]):
                execute = Confirm.ask(
                    "\n[bold yellow]This query will modify the database. Do you want to execute it?[/bold yellow]"
                )
            else:
                execute = Confirm.ask("\n[bold]Do you want to execute this SQL?[/bold]")
            
            if execute:
                try:
                    with console.status("[bold green]Executing query...[/bold green]", spinner="dots"):
                        result = db_manager.execute_sql(sql_response.sql)
                    
                    # Check if there was an error
                    if not result.get("success", True):
                        console.print(f"[bold red]Error executing SQL:[/bold red] {result.get('error', 'Unknown error')}")
                    else:
                        # Display results based on the format
                        if sql_response.display_format == "table" and result.get("data"):
                            # Create a table for the results
                            table = Table(show_header=True, header_style="bold magenta")
                            
                            # Add columns
                            for column in result["columns"]:
                                table.add_column(column)
                            
                            # Add rows
                            for row in result["data"]:
                                table.add_row(*[str(item) for item in row])
                            
                            console.print("\n[bold green]Query Results:[/bold green]")
                            console.print(table)
                            console.print(f"[dim]Returned {len(result['data'])} rows in {result['execution_time']:.4f} seconds[/dim]")
                        elif sql_response.display_format == "json" and result.get("data"):
                            console.print("\n[bold green]Query Results (JSON):[/bold green]")
                            console.print(json.dumps(result["data"], indent=2))
                        elif result.get("multi_statements", False):
                            console.print(f"\n[bold green]Multiple statements executed:[/bold green]")
                            
                            for i, stmt_result in enumerate(result["results"]):
                                status = "[green]Success[/green]" if stmt_result["success"] else f"[red]Error: {stmt_result['error']}[/red]"
                                console.print(f"Statement {i+1}: {status}")
                                
                                if stmt_result["data"]:
                                    # Create a table for the results
                                    table = Table(show_header=True, header_style="bold magenta")
                                    
                                    # Add columns
                                    for column in stmt_result["columns"]:
                                        table.add_column(column)
                                    
                                    # Add rows
                                    for row in stmt_result["data"]:
                                        table.add_row(*[str(item) for item in row])
                                    
                                    console.print(table)
                                    console.print(f"[dim]Returned {len(stmt_result['data'])} rows[/dim]")
                                elif stmt_result["affected_rows"] is not None:
                                    console.print(f"[green]Affected rows: {stmt_result['affected_rows']}[/green]")
                                    
                            console.print(f"[dim]Total execution time: {result['execution_time']:.4f} seconds[/dim]")
                        else:
                            if result.get("affected_rows") is not None:
                                console.print(f"\n[bold green]Query executed successfully in {result['execution_time']:.4f} seconds[/bold green]")
                                console.print(f"[green]Affected rows: {result['affected_rows']}[/green]")
                            else:
                                console.print(f"\n[bold green]Query executed successfully in {result['execution_time']:.4f} seconds[/bold green]")
                                console.print("[yellow]No data returned[/yellow]")
                except Exception as e:
                    console.print(f"[bold red]Error executing SQL:[/bold red] {str(e)}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

@cli.command()
def config():
    """View or update HyperXQL configuration."""
    print_banner()
    
    try:
        config = Config()
        
        console.print("\n[bold]Current Configuration:[/bold]\n")
        
        # Display current provider
        console.print(f"LLM Provider: [cyan]{config.llm_provider}[/cyan]")
        
        # Display database connection info (without sensitive info)
        db_type = config.db_config.get("db_type", "Not configured")
        db_host = config.db_config.get("host", "Not configured")
        db_name = config.db_config.get("database", "Not configured")
        
        console.print(f"Database Type: [cyan]{db_type}[/cyan]")
        console.print(f"Database Host: [cyan]{db_host}[/cyan]")
        console.print(f"Database Name: [cyan]{db_name}[/cyan]")
        
        # Ask if user wants to update configuration
        if click.confirm("\nDo you want to update your configuration?", default=False):
            initialize_config()
            console.print("[bold green]✓[/bold green] Configuration updated successfully!")
        
    except ConfigurationError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {str(e)}")
        console.print("Run [cyan]hyperxql init[/cyan] to set up your configuration.")
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {str(e)}")
        logger.exception("Unexpected error in config command")

@cli.command()
def status():
    """Display the status of the HyperXQL configuration."""
    from hyperxql.config import load_config
    
    config = load_config()
    console = Console()
    
    # Display header
    console.print(Panel("[bold]HyperXQL Status[/bold]", expand=False))
    
    # Display LLM configuration
    llm_table = Table(title="LLM Configuration")
    llm_table.add_column("Service", style="green")
    llm_table.add_column("Status", style="blue")
    llm_table.add_column("Model", style="blue")
    
    primary_service = config.get("llm_service", "together")
    
    services = [
        ("Together AI", "together_api_key", "together_model"),
        ("OpenAI", "openai_api_key", "openai_model"),
        ("Anthropic", "anthropic_api_key", "anthropic_model")
    ]
    
    for service_name, key_name, model_name in services:
        api_key = config.get(key_name, "")
        model = config.get(model_name, "Not configured")
        status = "Available" if api_key else "Not configured"
        
        if service_name.lower().startswith(primary_service.lower()):
            service_display = f"[bold]{service_name} (PRIMARY)[/bold]"
        else:
            service_display = f"{service_name} (Fallback)"
            
        llm_table.add_row(service_display, status, model)
    
    console.print(llm_table)
    
    # ...existing code to display database status, etc...

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind the server to')
@click.option('--port', default=5000, help='Port to bind the server to')
@click.option('--debug/--no-debug', default=False, help='Run in debug mode')
@click.option('--open-browser/--no-open-browser', default=True, help='Open browser automatically')
def gui(host, port, debug, open_browser):
    """Launch the HyperXQL web interface."""
    print_banner()
    
    console.print("\n[bold green]Starting HyperXQL Web Interface[/bold green]\n")
    
    # Check if configuration exists
    try:
        config = Config()
    except ConfigurationError:
        # If config doesn't exist, create it first
        console.print("[yellow]Configuration not found. Setting up HyperXQL first...[/yellow]")
        config = initialize_config()
        console.print("[bold green]✓[/bold green] Configuration completed successfully!")
    
    # Check if Flask is installed
    if importlib.util.find_spec("flask") is None:
        console.print("[bold red]Error:[/bold red] Flask is not installed. Please install it with 'pip install flask'.")
        return
    
    # Find the path to main.py
    main_script_path = None
    potential_paths = [
        Path(__file__).parent.parent.parent / 'main.py',  # From CLI script location
        Path.cwd() / 'main.py',  # Current working directory
    ]
    
    for path in potential_paths:
        if path.exists():
            main_script_path = path
            break
    
    if main_script_path is None:
        console.print("[bold red]Error:[/bold red] Could not find main.py script to launch the web interface.")
        return
    
    # Start the web server
    try:
        # Show information to the user
        console.print(f"[bold]Server URL:[/bold] http://{host}:{port}")
        console.print("[bold]Press CTRL+C to stop the server[/bold]\n")
        
        # Prepare environment variables
        env = os.environ.copy()
        env["FLASK_APP"] = str(main_script_path)
        if debug:
            env["FLASK_DEBUG"] = "1"
        
        # Command to run the Flask app
        cmd = [sys.executable, str(main_script_path)]
        
        # Configure host and port
        cmd.extend(["--host", host, "--port", str(port)])
        
        # Start the server process
        process = subprocess.Popen(cmd, env=env)
        
        # Open browser after a short delay to allow server to start
        if open_browser:
            def open_browser_tab():
                time.sleep(1.5)  # Wait for the server to start
                webbrowser.open(f"http://{host}:{port}")
            
            browser_thread = threading.Thread(target=open_browser_tab)
            browser_thread.daemon = True
            browser_thread.start()
        
        # Handle Ctrl+C gracefully
        def signal_handler(sig, frame):
            console.print("\n[bold yellow]Shutting down HyperXQL web interface...[/bold yellow]")
            process.terminate()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Wait for the process to finish
        process.wait()
        
    except Exception as e:
        console.print(f"[bold red]Error starting web interface:[/bold red] {str(e)}")
        logger.exception("Error starting web interface")
        sys.exit(1)

# Add the new agent command to the CLI

@cli.command()
@click.argument("task", nargs=-1)
@click.option("--verbose/--quiet", default=True, help="Toggle verbose agent output")
def agent(task, verbose):
    """
    Interact with the database using an AI agent that explains its thought process.
    
    Example: hyperxql agent "Create a users table with name, email, and phone columns"
    """
    print_banner()
    
    if not task:
        console.print("[bold yellow]Please provide a task for the agent.[/bold yellow]")
        console.print("Example: [cyan]hyperxql agent \"Create a users table with name, email, and phone columns\"[/cyan]")
        return
    
    # Join all arguments to form the complete task
    task_text = " ".join(task)
    
    try:
        # Load configuration
        config = Config()
        
        # Import the agent module
        from hyperxql.agent import DatabaseAgent
        
        # Create the agent
        agent = DatabaseAgent(config, verbose=verbose)
        
        # Execute the operation
        result = agent.execute_operation(task_text)
        
        if not result.get("success", False):
            console.print(f"[bold red]Agent could not complete the task: {result.get('error', 'Unknown error')}[/bold red]")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        logger.exception("Error in agent mode")

def main():
    """Main entry point for the CLI."""
    cli()

if __name__ == "__main__":
    main()
