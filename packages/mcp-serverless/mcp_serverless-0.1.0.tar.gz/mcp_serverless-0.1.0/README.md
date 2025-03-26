# MCP-Serverless

A Python package for implementing the Model Context Protocol in serverless environments.

## About Model Context Protocol

The Model Context Protocol (MCP) is a standardized way for AI models to interact with their context, including:

- Structured communication between models and their runtime environments
- Standardized interfaces for data exchange
- Context management for AI inference in serverless environments
- Tools for efficient model deployment and scaling

## Installation

```bash
pip install mcp-serverless
```

## Quick Start

```python
from mcp_serverless import about
from mcp_serverless.core import create_mcp_context

# Print information about MCP
print(about())

# Create a context for your model
context = create_mcp_context(model_id="my-model")

# Add data to the context
context.add_context("input", "Some user input")
context.add_context("parameters", {"temperature": 0.7, "max_tokens": 100})

# Get context data
print(context.get_context())
```

## Features

- Simple API for managing model context
- Lightweight with minimal dependencies
- Designed for serverless environments

## License

MIT 