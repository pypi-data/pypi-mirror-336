"""Core functionality for the MCP Serverless package."""


class MCPContext:
    """Base class for managing Model Context Protocol in serverless environments."""
    
    def __init__(self, model_id=None, context_data=None):
        """Initialize an MCP context.
        
        Args:
            model_id (str, optional): Identifier for the AI model.
            context_data (dict, optional): Initial context data.
        """
        self.model_id = model_id
        self.context_data = context_data or {}
        self.initialized = True
    
    def add_context(self, key, value):
        """Add data to the context.
        
        Args:
            key (str): Context data key.
            value (any): Context data value.
        """
        self.context_data[key] = value
        
    def get_context(self, key=None):
        """Retrieve context data.
        
        Args:
            key (str, optional): Specific context key to retrieve.
                If None, returns the entire context.
                
        Returns:
            The requested context data.
        """
        if key is None:
            return self.context_data
        return self.context_data.get(key)
    
    def clear_context(self):
        """Clear all context data."""
        self.context_data = {}
        
    def __str__(self):
        """String representation of the MCP context."""
        return (f"MCPContext(model_id={self.model_id}, "
                f"data_keys={list(self.context_data.keys())})")


def create_mcp_context(model_id=None, initial_context=None):
    """Factory function to create a new MCP context.
    
    Args:
        model_id (str, optional): Identifier for the AI model.
        initial_context (dict, optional): Initial context data.
        
    Returns:
        MCPContext: A new context instance.
    """
    return MCPContext(model_id=model_id, context_data=initial_context) 