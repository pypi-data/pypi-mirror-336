"""
Utility modules for the TPM CLI.

This package contains various utility modules used by the TPM CLI for interacting with
different services and APIs.
"""

from importlib import import_module

# List of all utility modules
__all__ = [
    'aws_utils',
    'config_utils',
    'github_utils',
    'google_utils',
    'jira_utils',
    'neo4j_utils',
    'notion_utils',
    'project_utils',
]

# Import all utilities to make them available when importing the utils package
for module_name in __all__:
    try:
        globals()[module_name] = import_module(f'utils.{module_name}')
    except ImportError:
        pass
