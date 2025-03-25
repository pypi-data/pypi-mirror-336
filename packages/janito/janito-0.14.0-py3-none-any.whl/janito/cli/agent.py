"""
Agent initialization and query handling for Janito CLI.

This file is a compatibility layer that imports from the new module structure.
"""

# Import the public API from the new module structure
from janito.cli.agent.query import handle_query
from janito.cli.agent.conversation import load_messages, save_messages

# Export the public API
__all__ = ["handle_query", "load_messages", "save_messages"]