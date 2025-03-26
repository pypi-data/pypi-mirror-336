#!/usr/bin/env python3
"""
Setup script for HyperXQL package
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Get the long description from the README file
readme_path = Path(__file__).parent / "README.md"
if (readme_path.exists()):
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = """# HyperXQL - Natural Language to SQL Database Operations

HyperXQL is an advanced natural language to SQL conversion tool that allows users to interact with databases using plain English. 

## Key Features in v2.0.0

- **Advanced AI Agent**: Interact with your database through an intelligent agent that understands complex queries
- **Multi-LLM Support**: Integration with OpenAI and Together AI models
- **Enhanced CLI**: Improved command-line interface with interactive mode and advanced query capabilities
- **Schema Visualization**: Dynamic visualization of database schema with relationship inference
- **Query Optimization**: Intelligent optimization of generated SQL queries
- **Multi-database Support**: Compatible with SQLite, PostgreSQL, and MySQL
- **Web Interface**: Interactive web UI for database management and querying
- **Detailed Explanations**: Get step-by-step reasoning for every generated query

For more details, visit [GitHub](https://github.com/skandanv/hyperxql).
"""

# Import version from package if available
try:
    from hyperxql import __version__
    version = __version__
except ImportError:
    version = "2.0.1"  # Fallback version

# Get requirements from requirements.txt
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
else:
    # Fallback requirements
    requirements = [
        "click>=8.0.0",
        "flask>=2.0.0",
        "sqlalchemy>=2.0.0",
        "rich>=10.0.0",
        "together>=0.1.5",
        "openai>=1.0.0",
        "sqlparse>=0.4.4",
        "pillow>=9.0.0",
        "python-dotenv>=0.20.0",
    ]

setup(
    name="hyperxql",
    version="2.0.1",  # Ensure this is correct
    description="Natural Language to SQL Database Operations with Advanced AI Agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="HyperXQL Team",
    author_email="hyperxql@skandan.com",
    url="https://github.com/skandanv/hyperxql",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "hyperxql=hyperxql.cli:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Database :: Front-Ends",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    keywords="database sql natural-language ai llm agent sqlite postgresql mysql query-generator ai-assistant database-tool",
    project_urls={
        "Documentation": "https://github.com/skandanv/hyperxql/wiki",
        "Bug Reports": "https://github.com/skandanv/hyperxql/issues",
        "Source": "https://github.com/skandanv/hyperxql",
    },
)