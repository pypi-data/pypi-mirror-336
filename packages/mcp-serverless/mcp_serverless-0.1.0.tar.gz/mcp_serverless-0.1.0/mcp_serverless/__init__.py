"""
MCP Serverless - Python package for Model Context Protocol

This package provides tools and utilities for working with the Model Context 
Protocol in serverless environments.
"""

__version__ = "0.1.0"
__author__ = "MCP Team"


def get_version():
    """Return the current version of the package."""
    return __version__


def about():
    """Return information about the Model Context Protocol."""
    return """
    The Model Context Protocol (MCP) is a standardized way for AI models 
    to interact with their context, including:
    
    - Structured communication between models and their runtime environments
    - Standardized interfaces for data exchange
    - Context management for AI inference in serverless environments
    - Tools for efficient model deployment and scaling
    
    This package provides utilities to implement MCP in serverless 
    architectures.
    """ 