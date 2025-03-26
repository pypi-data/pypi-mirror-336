"""Tests for the core module of mcp-serverless package."""
import unittest
from mcp_serverless.core import MCPContext, create_mcp_context


class TestMCPContext(unittest.TestCase):
    """Test cases for MCPContext class."""

    def test_initialization(self):
        """Test context initialization."""
        context = MCPContext(model_id="test-model")
        self.assertEqual(context.model_id, "test-model")
        self.assertEqual(context.context_data, {})
        self.assertTrue(context.initialized)

    def test_add_get_context(self):
        """Test adding and retrieving context data."""
        context = MCPContext()
        context.add_context("key1", "value1")
        context.add_context("key2", {"nested": "data"})
        
        self.assertEqual(context.get_context("key1"), "value1")
        self.assertEqual(context.get_context("key2"), {"nested": "data"})
        self.assertEqual(
            context.get_context(),
            {"key1": "value1", "key2": {"nested": "data"}}
        )

    def test_clear_context(self):
        """Test clearing context data."""
        context = MCPContext()
        context.add_context("key1", "value1")
        self.assertEqual(context.get_context("key1"), "value1")
        
        context.clear_context()
        self.assertEqual(context.get_context(), {})

    def test_factory_function(self):
        """Test the context factory function."""
        initial_data = {"setting": "value"}
        context = create_mcp_context("model-x", initial_data)
        
        self.assertEqual(context.model_id, "model-x")
        self.assertEqual(context.context_data, initial_data)


if __name__ == "__main__":
    unittest.main() 