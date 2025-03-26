# HyperXQL

**Natural Language to SQL Database Operations**

HyperXQL is a powerful tool that enables users to interact with databases using natural language. It leverages large language models to generate and execute SQL queries based on your instructions, without requiring you to write SQL code directly.

![HyperXQL Logo](static/img/hyperxql-logo.png)

## Features

- 🔄 Convert natural language to SQL
- 🗄️ Support for SQLite, PostgreSQL, and MySQL
- 🤖 Intelligent AI agent for database operations
- 🔍 Database schema analysis and visualization
- 📊 Interactive command-line interface
- 🌐 Web interface for query execution
- 🛠️ Automatic error detection and recovery

## Installation

```bash
pip install hyperxql
```

## Quick Start

1. Initialize HyperXQL:

```bash
hyperxql init
```

This will guide you through setting up your configuration and database connection.

2. Use the agent to perform database operations:

```bash
hyperxql agent "create a users table with columns for id, name, email and phone number"
```

3. Query your database:

```bash
hyperxql query "show me all users who signed up in the last month"
```

## Database Agent

The intelligent database agent can help you:

- Create tables and schema
- Insert, update, and delete data
- Generate sample data
- Query and analyze your database
- Fix errors and handle edge cases

The agent thinks aloud, explains its reasoning, and shows you exactly what it's doing.

## Web Interface

Start the web interface with:

```bash
hyperxql web
```

Then open your browser to http://localhost:5000

## Requirements

- Python 3.8+
- SQLAlchemy-supported database (SQLite, PostgreSQL, MySQL)
- API key for OpenAI or Together AI (configurable)

## License

MIT License
