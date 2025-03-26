"""
AI Agent for HyperXQL that provides conversational database operations.
The agent analyzes, thinks aloud, and explains its actions while manipulating the database.
"""

import time
import random
import sqlite3
import logging
import textwrap
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union, Set
import sqlparse

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich import box
from rich.table import Table
from rich.syntax import Syntax

from .config import Config
from .llm_client import LLMClient
from .db_manager import DatabaseManager
from .sql_generator import SQLGenerator
from .exceptions import DatabaseError, SQLGenerationError

logger = logging.getLogger(__name__)
console = Console()

class DatabaseAgent:
    """Interactive AI agent for database operations."""
    
    def __init__(self, config: Config, verbose: bool = True):
        """Initialize the database agent."""
        self.config = config
        self.db_manager = DatabaseManager(config)
        self.llm_client = LLMClient(config)
        self.sql_generator = SQLGenerator(self.llm_client)
        self.console = Console()
        self.verbose = verbose
        self.thinking_phrases = [
            "Analyzing database structure...",
            "Thinking about the best approach...",
            "Checking existing tables...",
            "Planning the database changes...",
            "Formulating SQL statements...",
            "Considering edge cases...",
            "Looking for potential issues...",
            "Optimizing query structure...",
            "Checking for existing data...",
            "Ensuring data integrity...",
        ]
        
        # New properties for error tracking and smart retries
        self.error_patterns = {
            "unique_constraint": [
                r"UNIQUE constraint failed", 
                r"duplicate key value violates unique constraint",
                r"Duplicate entry"
            ],
            "foreign_key_constraint": [
                r"FOREIGN KEY constraint failed",
                r"foreign key constraint fails",
                r"violates foreign key constraint"
            ],
            "syntax_error": [
                r"syntax error",
                r"SQL syntax error",
                r"You have an error in your SQL syntax"
            ],
            "table_not_exists": [
                r"no such table",
                r"Table .* doesn't exist",
                r"relation .* does not exist"
            ],
            "column_not_exists": [
                r"no such column",
                r"Unknown column",
                r"column .* does not exist"
            ],
            "permission_error": [
                r"permission denied",
                r"access denied",
                r"not authorized"
            ]
        }
        self.executed_statements = []
        self.execution_errors = []
        self.recovery_attempts = {}
        
    def _think(self, message: str = None, duration: float = 1.0):
        """Display a thinking message with optional delay."""
        if not self.verbose:
            return
            
        if message is None:
            message = random.choice(self.thinking_phrases)
            
        with self.console.status(f"[bold blue]{message}[/bold blue]", spinner="dots"):
            time.sleep(duration)
    
    def _speak(self, message: str, style: str = "info"):
        """Display a message from the agent."""
        if not self.verbose:
            return
            
        styles = {
            "info": "blue",
            "success": "green",
            "warning": "yellow",
            "error": "red",
            "thinking": "cyan",
        }
        
        # Wrap long lines for better readability
        wrapped_message = textwrap.fill(message, width=80)
        
        # Display message with appropriate style
        color = styles.get(style, "white")
        self.console.print(f"[bold {color}]Agent:[/bold {color}] {wrapped_message}")
    
    def analyze_database(self) -> Dict[str, Any]:
        """Analyze the current database structure."""
        self._speak("Let me analyze your database structure first...", "thinking")
        self._think("Examining tables and relationships")
        
        try:
            # Get database information
            db_info = self.db_manager.get_database_info()
            
            # Display database summary
            num_tables = len(db_info.get("tables", []))
            if num_tables == 0:
                self._speak("I don't see any tables in your database yet. It looks like we're starting fresh!", "info")
            else:
                table_names = [table["name"] for table in db_info.get("tables", [])]
                self._speak(f"I found {num_tables} tables in your database: {', '.join(table_names)}", "info")
                
                # Display more detailed information about each table
                for table in db_info.get("tables", []):
                    self._think(f"Analyzing table: {table['name']}")
                    columns = table.get("columns", [])
                    column_info = [f"{c['name']} ({c['type']})" for c in columns]
                    self._speak(f"Table '{table['name']}' has {len(columns)} columns: {', '.join(column_info)}", "info")
            
            return db_info
            
        except Exception as e:
            self._speak(f"I had trouble analyzing your database: {str(e)}", "error")
            logger.error(f"Error analyzing database: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_error(self, error_message: str) -> Tuple[str, Dict[str, Any]]:
        """
        Analyze an error message to identify the type and details of the error.
        
        Args:
            error_message: The error message to analyze
            
        Returns:
            Tuple of (error_type, error_details)
        """
        error_message = str(error_message).lower()
        error_type = "unknown"
        error_details = {}
        
        # Check for each error pattern
        for err_type, patterns in self.error_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, error_message, re.IGNORECASE)
                if match:
                    error_type = err_type
                    
                    # Extract table name if present
                    table_match = re.search(r'table[s\s]*([\'\"\w]+)', error_message)
                    if table_match:
                        error_details["table"] = table_match.group(1)
                        
                    # Extract column name if present
                    column_match = re.search(r'column[s\s]*([\'\"\w]+)', error_message)
                    if column_match:
                        error_details["column"] = column_match.group(1)
                        
                    # For unique constraint errors, try to extract the column
                    if err_type == "unique_constraint":
                        # Pattern like: "UNIQUE constraint failed: table.column"
                        constraint_match = re.search(r'constraint failed:[\s]*([\w\.]+)', error_message)
                        if constraint_match:
                            parts = constraint_match.group(1).split('.')
                            if len(parts) == 2:
                                error_details["table"] = parts[0]
                                error_details["column"] = parts[1]
                    
                    return error_type, error_details
        
        return error_type, error_details
    
    def _suggest_error_fix(self, error_type: str, error_details: Dict[str, Any], sql: str) -> str:
        """
        Suggest a fix for a SQL error.
        
        Args:
            error_type: Type of error
            error_details: Error details
            sql: Original SQL that caused the error
            
        Returns:
            Human-readable suggestion for fixing the error
        """
        if error_type == "unique_constraint":
            table = error_details.get("table", "the table")
            column = error_details.get("column", "a column")
            return (f"The SQL statement is trying to insert duplicate values in {table}.{column}, "
                   f"which has a unique constraint. Try using different values, or use "
                   f"INSERT OR IGNORE/REPLACE to handle duplicates.")
        
        elif error_type == "foreign_key_constraint":
            return ("The SQL statement is trying to insert a row with a foreign key that doesn't exist in the referenced table. "
                   "Make sure the referenced values exist in the parent table first.")
        
        elif error_type == "syntax_error":
            return "There's a syntax error in the SQL statement. Check for typos or missing parentheses/quotes."
        
        elif error_type == "table_not_exists":
            table = error_details.get("table", "the specified table")
            return f"The table '{table}' doesn't exist. You need to create it first or check the spelling."
        
        elif error_type == "column_not_exists":
            column = error_details.get("column", "the specified column")
            table = error_details.get("table", "a table")
            return f"The column '{column}' doesn't exist in table '{table}'. Check the column name or add it first."
        
        elif error_type == "permission_error":
            return "You don't have permission to perform this operation. Check your database user privileges."
        
        return "An unexpected error occurred. You may need to modify your SQL approach."
    
    def _fix_unique_constraint_error(self, sql: str, table: str, column: str) -> str:
        """
        Fix a unique constraint error by modifying the SQL statement.
        
        Args:
            sql: Original SQL statement
            table: Table with the constraint
            column: Column with the constraint
            
        Returns:
            Modified SQL statement
        """
        # For SQLite, use INSERT OR REPLACE to handle unique constraint errors
        if sql.strip().upper().startswith("INSERT INTO"):
            fixed_sql = sql.replace("INSERT INTO", "INSERT OR REPLACE INTO")
            return fixed_sql
        
        return sql
    
    def _get_existing_ids(self, table: str) -> Set[int]:
        """Get existing ID values from a table to avoid conflicts."""
        try:
            result = self.db_manager.execute_sql(f"SELECT id FROM {table}")
            if result.get("success", False) and result.get("data"):
                return {row[0] for row in result["data"]}
            return set()
        except Exception:
            return set()
    
    def _fix_insert_with_id_conflict(self, sql: str, table: str) -> str:
        """
        Fix an INSERT statement that has ID conflicts by using new IDs.
        
        Args:
            sql: Original SQL statement
            table: Table name
            
        Returns:
            Modified SQL with new IDs that don't conflict
        """
        # Get existing IDs
        existing_ids = self._get_existing_ids(table)
        if not existing_ids:
            return sql
            
        # Find the max ID
        max_id = max(existing_ids) if existing_ids else 0
        next_id = max_id + 1
        
        # Parse the SQL to extract values
        # Handle multiple value sets in INSERT statements
        sql_lower = sql.lower()
        if "values" not in sql_lower:
            return sql
        
        # Split into parts before and after VALUES
        parts = sql_lower.split("values", 1)
        values_part = parts[1].strip()
        
        # Extract each value tuple
        values_tuples = []
        open_pos = 0
        in_tuple = False
        current_tuple = ""
        
        # Parse the values carefully
        for i, char in enumerate(values_part):
            if char == '(' and not in_tuple:
                in_tuple = True
                open_pos = i
            elif char == ')' and in_tuple:
                in_tuple = False
                current_tuple = values_part[open_pos:i+1]
                values_tuples.append(current_tuple)
                current_tuple = ""
        
        if not values_tuples:
            return sql
        
        # Extract the column definition part
        columns_part = parts[0].strip()
        
        # Create new VALUES part with non-conflicting IDs
        new_values = []
        for value_tuple in values_tuples:
            # Extract the ID from the tuple
            id_match = re.search(r'\(\s*(\d+)', value_tuple)
            if id_match:
                old_id = int(id_match.group(1))
                # Replace with new ID
                new_tuple = value_tuple.replace(f"({old_id}", f"({next_id}")
                new_values.append(new_tuple)
                next_id += 1
            else:
                new_values.append(value_tuple)
        
        # Reassemble the SQL
        new_sql = f"{columns_part} VALUES {', '.join(new_values)}"
        
        return new_sql
    
    def _retry_with_modified_sql(self, stmt: str, error_type: str, error_details: Dict[str, Any]) -> Optional[str]:
        """
        Generate a modified SQL statement to retry after an error.
        
        Args:
            stmt: Original SQL statement
            error_type: Type of error
            error_details: Error details
            
        Returns:
            Modified SQL statement or None if no fix is available
        """
        if error_type == "unique_constraint":
            table = error_details.get("table")
            column = error_details.get("column")
            
            if table and column == "id":
                # Special handling for INSERT with multiple rows causing ID conflicts
                if "VALUES" in stmt and stmt.count("(") > 1:
                    fixed_sql = self._fix_insert_with_id_conflict(stmt, table)
                    return fixed_sql
                    
                # For single-row inserts, try a different approach
                existing_ids = self._get_existing_ids(table)
                if existing_ids:
                    max_id = max(existing_ids)
                    next_id = max_id + 1
                    
                    # Use a regex to replace the ID in the VALUES clause
                    return re.sub(r'VALUES\s*\(\s*\d+', f'VALUES ({next_id}', stmt)
                    
            elif table and column:
                # General unique constraint fix with OR REPLACE
                return self._fix_unique_constraint_error(stmt, table, column)
        
        # For other errors, we may need more complex fixes or manual intervention
        return None

    def execute_operation(self, operation_nl: str) -> Dict[str, Any]:
        """Execute a database operation described in natural language."""
        self._speak(f"I'll help you {operation_nl}. Let me think about how to approach this...", "info")
        
        # Clear execution tracking for new operation
        self.executed_statements = []
        self.execution_errors = []
        self.recovery_attempts = {}
        
        # First, analyze the database
        db_info = self.analyze_database()
        
        # Think about the request
        self._think("Formulating approach")
        self._speak("Now I'm planning the steps needed to perform this operation.", "thinking")
        
        # Generate SQL from natural language
        self._think("Generating SQL")
        try:
            sql_response = self.sql_generator.generate_sql(operation_nl, db_info)
            proposed_sql = sql_response.sql
            explanation = sql_response.explanation
            
            # Parse and display individual SQL statements
            statements = sqlparse.split(proposed_sql)
            formatted_statements = [sqlparse.format(stmt, reindent=True, keyword_case='upper') 
                                    for stmt in statements if stmt.strip()]
            
            # Display proposed SQL
            self._speak("Here's what I'm planning to do:", "info")
            for i, stmt in enumerate(formatted_statements):
                self.console.print(Panel(stmt, title=f"Step {i+1}", border_style="blue"))
            
            # Explain the approach
            self._speak("My approach:", "info")
            self.console.print(Panel(explanation, title="Explanation", border_style="cyan"))
            
            # Ask for confirmation before proceeding
            proceed = self.console.input("[bold yellow]Should I proceed with these changes? (yes/no): [/bold yellow]")
            if proceed.lower() not in ("y", "yes"):
                self._speak("Operation cancelled. No changes were made to your database.", "warning")
                return {"success": False, "message": "Operation cancelled by user"}
            
            # Execute the SQL
            self._speak("Executing the SQL statements. I'll report on each step...", "info")
            
            results = {}
            # Flag to track if we're showing data or executing a data modification query
            is_data_retrieval_operation = any(keyword in operation_nl.lower() for keyword in ["show", "display", "list", "get", "view", "select", "query", "all data", "all tables", "all records"])
            
            for i, stmt in enumerate(statements):
                if not stmt.strip():
                    continue
                
                stmt_key = f"statement_{i+1}"
                self._think(f"Executing statement {i+1}")
                
                # Track this statement
                self.executed_statements.append(stmt)
                
                try:
                    # Execute the statement
                    result = self.db_manager.execute_sql(stmt)
                    
                    if result.get("success", False):
                        # Handle successful execution
                        # For data retrieval operations, always show the results regardless of row count
                        if is_data_retrieval_operation and "select" in stmt.lower():
                            # Get table name from the query for better display
                            table_name = self._extract_table_name(stmt)
                            
                            if result.get("data") and result.get("columns"):
                                rows_count = len(result.get("data", []))
                                self._speak(f"Step {i+1} completed: Query returned {rows_count} rows", "success")
                                self._display_table_data(
                                    result["columns"], 
                                    result["data"], 
                                    f"Data from '{table_name}'" if table_name else f"Results from step {i+1}"
                                )
                            else:
                                self._speak(f"Step {i+1} completed: No data found in {table_name}", "info")
                                # Create an empty table to show structure
                                if result.get("columns"):
                                    self._display_empty_table(result["columns"], f"Table structure for '{table_name}' (no data)")
                        # For non-SELECT queries or non-data retrieval operations
                        elif result.get("affected_rows") is not None:
                            self._speak(f"Step {i+1} completed: {result.get('affected_rows')} rows affected", "success")
                        else:
                            # Handle case where there are results but it's not a data retrieval operation
                            rows_count = len(result.get("data", [])) if result.get("data") else 0
                            if rows_count > 0:
                                self._speak(f"Step {i+1} completed: Query returned {rows_count} rows", "success")
                                if "select" in stmt.lower():
                                    self._display_table_data(
                                        result["columns"], 
                                        result["data"], 
                                        f"Results from step {i+1}"
                                    )
                            else:
                                self._speak(f"Step {i+1} completed successfully", "success")
                    else:
                        # Handle errors
                        error_message = result.get("error", "Unknown error")
                        self._speak(f"Step {i+1} failed: {error_message}", "error")
                        
                        # Track the error
                        self.execution_errors.append({
                            "step": i+1,
                            "sql": stmt,
                            "error": error_message
                        })
                        
                        # Analyze the error
                        error_type, error_details = self._analyze_error(error_message)
                        
                        # Display error analysis and suggestions
                        if error_type != "unknown":
                            suggestion = self._suggest_error_fix(error_type, error_details, stmt)
                            self._speak(f"Error analysis: {suggestion}", "info")
                            
                            # Try to fix and retry if possible
                            modified_sql = self._retry_with_modified_sql(stmt, error_type, error_details)
                            if modified_sql and modified_sql != stmt:
                                self._speak("I'll try to fix this issue and retry with a modified SQL statement...", "thinking")
                                self.console.print(Panel(modified_sql, title=f"Modified SQL for Step {i+1}", border_style="yellow"))
                                
                                # Record retry attempt
                                self.recovery_attempts[stmt_key] = {
                                    "original_sql": stmt,
                                    "modified_sql": modified_sql,
                                    "error_type": error_type
                                }
                                
                                # Execute the modified SQL
                                retry_result = self.db_manager.execute_sql(modified_sql)
                                
                                if retry_result.get("success", False):
                                    self._speak(f"Retry successful! Modified SQL fixed the issue.", "success")
                                    
                                    # Update the result with the successful retry
                                    result = retry_result
                                    result["retry_succeeded"] = True
                                    result["original_error"] = error_message
                                    
                                    # If it's a data retrieval operation, show the results
                                    if result.get("data") and result.get("columns") and "select" in modified_sql.lower():
                                        self._display_table_data(
                                            result["columns"], 
                                            result["data"], 
                                            f"Results from retried step {i+1}"
                                        )
                                else:
                                    # Second retry attempt with a completely different approach for INSERT statements
                                    if "INSERT INTO" in stmt.upper() and error_type == "unique_constraint":
                                        self._speak("First retry failed. Trying a different approach...", "thinking")
                                        
                                        # For insert statements, try an approach that completely avoids IDs
                                        table_match = re.search(r'INSERT\s+INTO\s+([^\s\(]+)', stmt, re.IGNORECASE)
                                        if table_match:
                                            table_name = table_match.group(1)
                                            
                                            # Get table structure to know column names
                                            table_info = next((t for t in db_info.get("tables", []) if t["name"] == table_name), None)
                                            
                                            if table_info and table_info.get("columns"):
                                                # Get all columns except ID
                                                columns = [c["name"] for c in table_info["columns"] if c["name"].lower() != "id"]
                                                
                                                if columns:
                                                    # Extract values without the ID from the original statement
                                                    values_match = re.search(r'VALUES\s*(\(.*\))', stmt, re.IGNORECASE | re.DOTALL)
                                                    if values_match:
                                                        values_part = values_match.group(1)
                                                        
                                                        # Try to extract values without the ID
                                                        values_list = []
                                                        for value_set in re.findall(r'\(([^)]+)\)', values_part):
                                                            parts = [p.strip() for p in value_set.split(',')]
                                                            if len(parts) > 1:  # Skip the ID (first column)
                                                                values_list.append(f"({', '.join(parts[1:])})")
                                                        
                                                        if values_list:
                                                            # Create new INSERT without specifying ID
                                                            second_retry_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES {', '.join(values_list)}"
                                                            
                                                            self.console.print(Panel(second_retry_sql, title=f"Second retry SQL for Step {i+1}", border_style="yellow"))
                                                            
                                                            # Execute the new SQL
                                                            second_retry_result = self.db_manager.execute_sql(second_retry_sql)
                                                            
                                                            if second_retry_result.get("success", False):
                                                                self._speak(f"Second retry successful! I worked around the ID issue by letting the database auto-generate IDs.", "success")
                                                                result = second_retry_result
                                                                result["retry_succeeded"] = True
                                                                result["original_error"] = error_message
                                                            else:
                                                                self._speak(f"All retry attempts failed. There might be a fundamental issue with the data or table structure.", "error")
                                                                result["retry_failed"] = True
                                    else:
                                        self._speak(f"Retry also failed: {retry_result.get('error', 'Unknown error')}", "error")
                                        result["retry_failed"] = True
                            else:
                                self._speak("I can't automatically fix this error. You may need to manually modify the SQL.", "warning")
                        
                    results[stmt_key] = result
                except Exception as e:
                    self._speak(f"Error executing step {i+1}: {str(e)}", "error")
                    results[stmt_key] = {"success": False, "error": str(e)}
                    
                    # Track the error
                    self.execution_errors.append({
                        "step": i+1,
                        "sql": stmt,
                        "error": str(e)
                    })

            # Verify the operation
            self._speak("Let me verify that everything worked as expected...", "thinking")
            self._think("Verifying changes")
            
            # Re-analyze the database to see the changes
            new_db_info = self.db_manager.get_database_info()
            
            # Check if tables were created/modified as expected
            new_tables = set(table["name"] for table in new_db_info.get("tables", []))
            old_tables = set(table["name"] for table in db_info.get("tables", []))
            
            added_tables = new_tables - old_tables
            if added_tables:
                self._speak(f"I successfully created these new tables: {', '.join(added_tables)}", "success")
                
                # Display sample data for new tables if applicable
                for table_name in added_tables:
                    self._think(f"Checking table structure: {table_name}")
                    try:
                        # Get column info for the new table
                        table_info = next((t for t in new_db_info.get("tables", []) if t["name"] == table_name), None)
                        if table_info:
                            cols = [c["name"] for c in table_info.get("columns", [])]
                            self._speak(f"Table '{table_name}' has these columns: {', '.join(cols)}", "info")
                            
                            # Try to get a sample row to verify
                            sample_result = self.db_manager.execute_sql(f"SELECT * FROM {table_name} LIMIT 1")
                            if sample_result.get("success", False) and sample_result.get("data"):
                                self._speak(f"I've confirmed the table structure is correct by retrieving a sample row.", "success")
                                # Display the sample row
                                self._display_table_data(sample_result["columns"], sample_result["data"], f"Sample data from {table_name}")
                            else:
                                self._speak(f"The table was created, but it appears to be empty.", "info")
                    except Exception as e:
                        self._speak(f"Note: I couldn't verify the structure of table '{table_name}': {str(e)}", "warning")
            
            # Check for mock data in existing tables
            if "mock" in operation_nl.lower() or "sample" in operation_nl.lower() or "test" in operation_nl.lower() or "data" in operation_nl.lower():
                self._speak("Let me check if the sample data was inserted correctly...", "thinking")
                
                # For each relevant table, try to count rows and show sample data
                for table in new_db_info.get("tables", []):
                    table_name = table["name"]
                    try:
                        count_result = self.db_manager.execute_sql(f"SELECT COUNT(*) FROM {table_name}")
                        if count_result.get("success", False) and count_result.get("data"):
                            count = count_result["data"][0][0]
                            if count > 0:
                                self._speak(f"Table '{table_name}' contains {count} rows of data.", "success")
                                # Show sample data (up to 5 rows)
                                sample_data = self.db_manager.execute_sql(f"SELECT * FROM {table_name} LIMIT 5")
                                if sample_data.get("success", False) and sample_data.get("data"):
                                    self._display_table_data(sample_data["columns"], sample_data["data"], f"Sample data from {table_name}")
                            else:
                                self._speak(f"Table '{table_name}' exists but has no data yet.", "info")
                    except Exception:
                        pass
            
            # For "show data" type operations, ensure we display the results
            if any(keyword in operation_nl.lower() for keyword in ["show", "display", "list", "get", "view", "all data", "all tables", "all records"]):
                for result_key, result_value in results.items():
                    if result_value.get("success", False) and result_value.get("data") and result_value.get("columns"):
                        table_name = ""
                        # Extract table name from the SQL statement
                        stmt_idx = int(result_key.split('_')[1]) - 1
                        if stmt_idx < len(statements):
                            stmt_lower = statements[stmt_idx].lower()
                            table_name = self._extract_table_name(stmt_lower)
                        
                        # Display the result data in a formatted table
                        self._display_table_data(
                            result_value["columns"], 
                            result_value["data"], 
                            f"Data from '{table_name}'" if table_name else f"Results for {result_key}"
                        )
            
            # Summarize any errors or retry attempts
            if self.execution_errors:
                self._speak("Summary of issues encountered during execution:", "warning")
                for error in self.execution_errors:
                    self.console.print(f"[yellow]• Step {error['step']}: {error['error']}[/yellow]")
                
                if self.recovery_attempts:
                    self._speak("I attempted to recover from some errors by modifying the SQL:", "info")
                    for stmt_key, attempt in self.recovery_attempts.items():
                        step_num = stmt_key.split('_')[1]
                        if results.get(stmt_key, {}).get("retry_succeeded", False):
                            self.console.print(f"[green]• Step {step_num}: Successfully recovered from {attempt['error_type']} error[/green]")
                        else:
                            self.console.print(f"[yellow]• Step {step_num}: Attempted recovery from {attempt['error_type']} error but failed[/yellow]")
            
            # If this was a query operation, give a better success message
            if is_data_retrieval_operation:
                self._speak("Query execution completed. Data has been retrieved and displayed.", "success")
            else:
                # Check if we had any successful modifications
                had_success = any(
                    result.get("success", False) and result.get("affected_rows", 0) > 0 
                    for result in results.values()
                )
                
                if had_success:
                    self._speak("Database has been successfully updated with the new data.", "success")
                else:
                    if self.execution_errors:
                        self._speak("Operation completed with some errors. Some changes may not have been applied.", "warning")
                    else:
                        self._speak("Operation completed, but no data appears to have been modified.", "info")
            
            return {
                "success": len(self.execution_errors) == 0, 
                "message": "Operation completed successfully" if len(self.execution_errors) == 0 else "Operation completed with some errors",
                "details": results,
                "errors": self.execution_errors,
                "recovery_attempts": self.recovery_attempts
            }
            
        except SQLGenerationError as e:
            self._speak(f"I couldn't figure out how to perform this operation: {str(e)}", "error")
            return {"success": False, "error": str(e)}
        except Exception as e:
            self._speak(f"Something unexpected happened: {str(e)}", "error")
            logger.error(f"Unexpected error in execute_operation: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _extract_table_name(self, sql_statement: str) -> str:
        """Extract table name from a SQL SELECT statement."""
        sql_lower = sql_statement.lower()
        if "from" in sql_lower:
            # Split on FROM and take the next part
            parts = sql_lower.split("from")[1].strip().split()
            if parts:
                # Remove any trailing semicolons, commas, etc.
                return parts[0].rstrip(';,')
        return ""

    def _display_empty_table(self, columns: List[str], title: str = "Empty Table"):
        """Display an empty table with column structure."""
        if not self.verbose:
            return
            
        # Create a table to show structure
        table = Table(title=title, box=box.SIMPLE)
        
        # Add columns to the table
        for column in columns:
            table.add_column(str(column), style="cyan")
        
        # Add an empty row with placeholders
        table.add_row(*["(empty)" for _ in columns])
        
        # Print the table
        self.console.print()
        self.console.print(table)
        self.console.print()

    def _display_table_data(self, columns: List[str], data: List[List[Any]], title: str = "Query Results"):
        """Display query results in a formatted table."""
        if not self.verbose:
            return
        
        # Handle empty data case
        if not data:
            return self._display_empty_table(columns, f"{title} (No Data)")
            
        # Create a table for displaying results
        table = Table(title=title, box=box.SIMPLE)
        
        # Add columns to the table
        for column in columns:
            table.add_column(str(column), style="cyan")
        
        # Add rows to the table
        for row in data:
            table.add_row(*[str(item) for item in row])
        
        # Print the table
        self.console.print()  # Add some space
        self.console.print(table)
        self.console.print()  # Add some space after the table
    
    def check_table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        try:
            # Try to get table information
            result = self.db_manager.execute_sql(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            return bool(result.get("data"))
        except Exception as e:
            logger.error(f"Error checking if table exists: {str(e)}")
            return False

    def get_table_column_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get column information for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column information dictionaries
        """
        try:
            # Use PRAGMA table_info for SQLite
            result = self.db_manager.execute_sql(f"PRAGMA table_info({table_name})")
            
            if not result.get("success", False) or not result.get("data"):
                return []
                
            # Convert SQLite PRAGMA results to column info
            # Format: cid, name, type, notnull, dflt_value, pk
            columns = []
            for row in result.get("data", []):
                if len(row) >= 6:
                    columns.append({
                        "name": row[1],
                        "type": row[2],
                        "is_nullable": not bool(row[3]),
                        "is_primary_key": bool(row[5])
                    })
                    
            return columns
        except Exception as e:
            logger.error(f"Error getting column info for table {table_name}: {str(e)}")
            return []

    def count_table_rows(self, table_name: str) -> int:
        """
        Count the number of rows in a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Number of rows in the table
        """
        try:
            result = self.db_manager.execute_sql(f"SELECT COUNT(*) FROM {table_name}")
            if result.get("success", False) and result.get("data") and result["data"][0]:
                return result["data"][0][0]
            return 0
        except Exception as e:
            logger.error(f"Error counting rows in table {table_name}: {str(e)}")
            return 0
