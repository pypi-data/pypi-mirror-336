#!/usr/bin/env python3
"""
Setup script for HyperXQL package.
"""

from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Get version from hyperxql/__init__.py
with open(os.path.join("hyperxql", "__init__.py"), encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

setup(
    name="hyperxql",
    version=version,
    description="A Python library that bridges the gap between non-technical users and complex database operations through natural language processing and LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="HyperXQL Team",
    author_email="info@hyperxql.com",
    url="https://github.com/hyperxql/hyperxql",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.0",
        "python-dotenv>=1.0.0",
        "flask>=3.0.0",
        "flask-sqlalchemy>=3.0.0",
        "graphviz>=0.20.0",
        "gunicorn>=21.0.0",
        "openai>=1.0.0",
        "psycopg2-binary>=2.9.0",
        "pydot>=1.4.0",
        "requests>=2.31.0",
        "rich>=13.0.0",
        "sqlalchemy>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "hyperxql=hyperxql.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.11",
    keywords="database, natural language processing, sql, llm, ai",
)