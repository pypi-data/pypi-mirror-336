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

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("hyperxql")

# Initialize rich console for pretty output
console = Console()

def print_banner():
    """Print HyperXQL banner."""
    banner = """
    ╔═══════════════════════════════════════════════════╗
    ║                   HyperXQL                        ║
    ║ Natural Language to SQL - Powered by LLM          ║
    ╚═══════════════════════════════════════════════════╝
    """
    console.print(Panel.fit(banner, box=box.ROUNDED))

@click.group()
@click.version_option()
def cli():
    """
    HyperXQL - Natural Language to SQL Database Operations
    
    This CLI tool allows non-technical users to perform database operations
    using natural language, powered by LLMs.
    """
    pass

@cli.command()
def init():
    """Initialize HyperXQL configuration."""
    print_banner()
    console.print("\n[bold green]Welcome to HyperXQL setup![/bold green]\n")
    
    try:
        config = initialize_config()
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
def query(query):
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
        
        # Create SQL generator
        sql_generator = SQLGenerator(llm_client)
        
        # Show current database info (if connected)
        db_info = get_current_db_info(config)
        if db_info:
            console.print(Panel.fit(
                f"[bold]Connected to:[/bold] {db_info}", 
                title="Database Connection", 
                border_style="green"
            ))
        
        # Process the query
        console.print(f"\n[bold]Your query:[/bold] {query_text}")
        console.print("\n[bold cyan]Generating SQL...[/bold cyan]")
        
        sql_response = sql_generator.generate_sql(query_text, db_info)
        
        # Display the generated SQL
        if sql_response.sql:
            console.print("\n[bold green]Generated SQL:[/bold green]")
            console.print(Panel(sql_response.sql, border_style="green"))
        
        # Execute SQL if requested
        if sql_response.execute and sql_response.sql:
            console.print("\n[bold cyan]Executing SQL...[/bold cyan]")
            result = db_manager.execute_sql(sql_response.sql)
            
            # Display results
            console.print("\n[bold green]Result:[/bold green]")
            if sql_response.display_format == "table" and result.get("rows"):
                from rich.table import Table
                table = Table(show_header=True, header_style="bold")
                
                # Add columns
                if result.get("columns"):
                    for column in result["columns"]:
                        table.add_column(column)
                
                # Add rows
                for row in result["rows"]:
                    table.add_row(*[str(item) for item in row])
                
                console.print(table)
            else:
                console.print(Panel(str(result.get("message", "Operation completed successfully.")), 
                                   border_style="green"))
            
            if "db_update" in sql_response.metadata and sql_response.metadata["db_update"]:
                # Update the cached DB info
                db_info = get_current_db_info(config, force_refresh=True)
        
        # Show explanation if available
        if sql_response.explanation:
            console.print("\n[bold]Explanation:[/bold]")
            console.print(Panel(Markdown(sql_response.explanation), border_style="blue"))
        
    except ConfigurationError as e:
        console.print(f"\n[bold red]Configuration Error:[/bold red] {str(e)}")
        console.print("Run [cyan]hyperxql init[/cyan] to set up your configuration.")
    except LLMAPIError as e:
        console.print(f"\n[bold red]LLM API Error:[/bold red] {str(e)}")
    except DatabaseError as e:
        console.print(f"\n[bold red]Database Error:[/bold red] {str(e)}")
    except SQLGenerationError as e:
        console.print(f"\n[bold red]SQL Generation Error:[/bold red] {str(e)}")
    except Exception as e:
        console.print(f"\n[bold red]Unexpected Error:[/bold red] {str(e)}")
        logger.exception("Unexpected error processing query")

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

def main():
    """Main entry point for the CLI."""
    cli()

if __name__ == "__main__":
    main()
