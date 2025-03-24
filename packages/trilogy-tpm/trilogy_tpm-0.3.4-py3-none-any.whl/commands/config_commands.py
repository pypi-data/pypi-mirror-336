#!/usr/bin/env python3
"""
Configuration commands for TPM-CLI.
"""

import os
import sys
import json
from utils.config_utils import (
    get_credential,
    set_credential,
    load_credentials,
    show_config,
    CONFIG_DIR,
    CREDENTIALS_FILE,
)

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def cmd_config_show(args):
    """Show the current configuration."""
    try:
        show_config()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_config_google(args):
    """Configure Google Drive credentials."""
    try:
        if args.json_file:
            configure_service("google", json_file=args.json_file)
        else:
            print("Please provide a Google service account JSON file with --json-file.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_config_github(args):
    """Configure GitHub credentials."""
    try:
        if args.token:
            configure_service("github", token=args.token)
        else:
            print("Please provide a GitHub token with --token.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_config_jira(args):
    """Configure Jira credentials."""
    try:
        if args.email and args.token:
            configure_service("jira", email=args.email, token=args.token, server=args.server)
        else:
            print("Please provide both Jira email and token.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_config_notion(args):
    """Configure Notion credentials."""
    try:
        if args.token:
            configure_service("notion", token=args.token)
        else:
            print("Please provide a Notion API token with --token.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_config_neo4j(args):
    """Configure Neo4j credentials."""
    try:
        # Check for API key
        if args.api_key:
            configure_service("neo4j", api_key=args.api_key)
            print("Neo4j API key configured successfully.")
            
        # Check for connection credentials
        if args.uri and args.client_id and args.client_secret:
            configure_service("neo4j", uri=args.uri, client_id=args.client_id, client_secret=args.client_secret)
            print("Neo4j connection credentials configured successfully.")
            
        # If neither set of credentials provided
        if not (args.api_key or (args.uri and args.client_id and args.client_secret)):
            print("Please provide either:")
            print("1. Neo4j API key (--api-key) for database management")
            print("2. Neo4j URI, client ID, and client secret for connection")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_config_openai(args):
    """Configure OpenAI API key."""
    try:
        if args.api_key:
            configure_service("openai", api_key=args.api_key)
            print("OpenAI API key configured successfully.")
            
            # Also set the environment variable for the current session
            os.environ["OPENAI_API_KEY"] = args.api_key
        else:
            print("Please provide an OpenAI API key with --api-key.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_config(args):
    """Handle config subcommands."""
    if args.config_action == "show":
        cmd_config_show(args)
    elif args.config_action == "google":
        cmd_config_google(args)
    elif args.config_action == "github":
        cmd_config_github(args)
    elif args.config_action == "jira":
        cmd_config_jira(args)
    elif args.config_action == "notion":
        cmd_config_notion(args)
    elif args.config_action == "neo4j":
        cmd_config_neo4j(args)
    elif args.config_action == "openai":
        cmd_config_openai(args)
    else:
        print("Please specify a valid config action.")
        sys.exit(1)
