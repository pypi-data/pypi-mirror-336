# HyperXQL

HyperXQL is a Python library that bridges the gap between non-technical users and complex database operations through natural language processing and Large Language Models (LLMs).

![HyperXQL Logo](static/img/hyperxql-logo.png)

## Features

- ✨ Convert natural language to SQL queries with high accuracy
- 🔄 Execute database operations with plain English commands
- 🌐 Interactive web interface for user-friendly interactions
- 📊 Database schema visualization with interactive features
- 🔌 Support for SQLite, PostgreSQL, and MySQL databases
- 🤖 Integration with OpenAI and Together AI models
- 💬 Conversational explanations of SQL operations
- 📑 Detailed query results displayed in tables or text format
- 🔒 Secure API key and database credential management
- 🖥️ CLI interface for quick operations
- 🔄 Version control and migration support
- 📐 Customizable prompts and system instructions

## Installation

```bash
# Install from PyPI
pip install hyperxql

# Optional: Install graphviz for schema visualization
# On Ubuntu/Debian
apt-get install graphviz

# On macOS
brew install graphviz

# On Windows (using Chocolatey)
choco install graphviz
```

## Quick Start

### CLI Usage

```bash
# Initialize HyperXQL configuration
hyperxql init

# Run a natural language query
hyperxql query "Show me all users who joined last month"

# View or update configuration
hyperxql config
```

### Python Library Usage

```python
from hyperxql import Config, LLMClient, DatabaseManager, SQLGenerator

# Initialize configuration
config = Config()

# Create SQL generator
llm_client = LLMClient(config)
sql_generator = SQLGenerator(llm_client)

# Initialize database manager
db_manager = DatabaseManager(config)

# Generate SQL from natural language
nl_query = "Find all products with price greater than $100"
sql_response = sql_generator.generate_sql(nl_query, db_manager.get_database_info())

# Execute the generated SQL
result = db_manager.execute_sql(sql_response.sql)
print(result)
```

### Web Interface

To start the web interface:

```bash
# From the command line
python main.py

# Visit http://localhost:5000 in your browser
```

## Supported LLM Providers

1. **OpenAI**
   - gpt-4o (default)
   - gpt-3.5-turbo

2. **Together AI** 
   - meta-llama/Llama-3.3-70B-Instruct-Turbo-Free (default)
   - meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo-classifier
   - mistralai/Mixtral-8x22B-Instruct-v0.1
   - and other supported Together AI models

## Database Schema Visualization

HyperXQL provides interactive database schema visualization with:

- Entity-relationship diagrams
- Zoom and pan functionality
- Dark/light mode toggle
- Schema download options
- Primary and foreign key indicators
- Table relationship visualization

## Documentation

For detailed documentation, please visit:

- [Getting Started Guide](https://github.com/hyperxql/hyperxql/wiki/Getting-Started)
- [API Reference](https://github.com/hyperxql/hyperxql/wiki/API-Reference)
- [Web Interface Guide](https://github.com/hyperxql/hyperxql/wiki/Web-Interface)
- [Configuration Options](https://github.com/hyperxql/hyperxql/wiki/Configuration)
- [Advanced Usage](https://github.com/hyperxql/hyperxql/wiki/Advanced-Usage)

## Contributing

Contributions are welcome! Please check out our [contributing guidelines](https://github.com/hyperxql/hyperxql/blob/main/CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
