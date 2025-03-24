#!/usr/bin/env python3
"""
Configuration utilities for TPM-CLI.
"""

import os
import json
import sys
from pathlib import Path

# Constants
CONFIG_DIR = os.path.expanduser("~/.tpm-cli")
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, "credentials.json")

# Legacy paths for backward compatibility
LEGACY_PATHS = {
    "google": os.path.expanduser("~/.config/google/creds.json"),
    "github": os.path.expanduser("~/.config/github/token"),
    "jira_email": os.path.expanduser("~/.config/jira/email"),
    "jira_token": os.path.expanduser("~/.config/jira/token"),
    "notion_token": os.path.expanduser("~/.config/notion.token")
}

def setup_config_dir():
    """Set up the config directory if it doesn't exist."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)

def load_credentials():
    """Load credentials from the credentials file."""
    setup_config_dir()
    
    # Initialize with empty credentials
    credentials = {
        "google": {},
        "github": {"token": ""},
        "jira": {"email": "", "token": "", "server": ""},
        "notion": {"token": ""},
        "neo4j": {"uri": "", "client_id": "", "client_secret": "", "api_key": ""},
        "openai": {"api_key": ""}
    }
    
    # Try to load from centralized credentials file
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                stored_creds = json.load(f)
                # Update credentials with stored values, preserving structure
                for service in credentials:
                    if service in stored_creds:
                        credentials[service] = stored_creds[service]
        except Exception as e:
            print(f"Error loading credentials: {e}")
    
    # If credentials are missing, try to load from legacy paths
    # Google
    if not credentials["google"] and os.path.exists(LEGACY_PATHS["google"]):
        try:
            with open(LEGACY_PATHS["google"], 'r') as f:
                credentials["google"] = json.load(f)
                save_credentials(credentials)  # Save to centralized file
        except Exception as e:
            print(f"Error loading legacy Google credentials: {e}")
    
    # GitHub
    if not credentials["github"]["token"] and os.path.exists(LEGACY_PATHS["github"]):
        try:
            with open(LEGACY_PATHS["github"], 'r') as f:
                credentials["github"]["token"] = f.read().strip()
                save_credentials(credentials)  # Save to centralized file
        except Exception as e:
            print(f"Error loading legacy GitHub credentials: {e}")
    
    # Jira
    if not credentials["jira"]["email"] and os.path.exists(LEGACY_PATHS["jira_email"]):
        try:
            with open(LEGACY_PATHS["jira_email"], 'r') as f:
                credentials["jira"]["email"] = f.read().strip()
                save_credentials(credentials)  # Save to centralized file
        except Exception as e:
            print(f"Error loading legacy Jira email: {e}")
    
    if not credentials["jira"]["token"] and os.path.exists(LEGACY_PATHS["jira_token"]):
        try:
            with open(LEGACY_PATHS["jira_token"], 'r') as f:
                credentials["jira"]["token"] = f.read().strip()
                save_credentials(credentials)  # Save to centralized file
        except Exception as e:
            print(f"Error loading legacy Jira token: {e}")
    
    # Notion
    if not credentials["notion"]["token"] and os.path.exists(LEGACY_PATHS["notion_token"]):
        try:
            with open(LEGACY_PATHS["notion_token"], 'r') as f:
                credentials["notion"]["token"] = f.read().strip()
                save_credentials(credentials)  # Save to centralized file
        except Exception as e:
            print(f"Error loading legacy Notion token: {e}")
    
    return credentials

def save_credentials(credentials):
    """Save credentials to the credentials file."""
    setup_config_dir()
    
    try:
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(credentials, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving credentials: {e}")
        return False

def get_credential(service, key=None):
    """Get a specific credential."""
    credentials = load_credentials()
    
    if service not in credentials:
        return None
    
    if key is None:
        return credentials[service]
    
    if isinstance(credentials[service], dict) and key in credentials[service]:
        return credentials[service][key]
    
    return None

def set_credential(service, value, key=None):
    """Set a specific credential."""
    credentials = load_credentials()
    
    if service not in credentials:
        credentials[service] = {}
    
    if key is None:
        credentials[service] = value
    else:
        if not isinstance(credentials[service], dict):
            credentials[service] = {}
        credentials[service][key] = value
    
    return save_credentials(credentials)

def show_config():
    """Show the current configuration."""
    credentials = load_credentials()
    
    print("TPM-CLI Configuration")
    print("====================")
    print(f"Configuration directory: {CONFIG_DIR}")
    print()
    
    # Google Drive
    print("Google Drive:")
    if credentials["google"] and "client_email" in credentials["google"]:
        print("  Status: Configured")
        print(f"  Service Account: {credentials['google']['client_email']}")
    else:
        print("  Status: Not configured")
    print()
    
    # GitHub
    print("GitHub:")
    if credentials["github"]["token"]:
        masked_token = mask_token(credentials["github"]["token"])
        print("  Status: Configured")
        print(f"  Token: {masked_token}")
    else:
        print("  Status: Not configured")
    print()
    
    # Jira
    print("Jira:")
    if credentials["jira"]["email"] and credentials["jira"]["token"]:
        masked_token = mask_token(credentials["jira"]["token"])
        print("  Status: Configured")
        print(f"  Email: {credentials['jira']['email']}")
        print(f"  Token: {masked_token}")
        if "server" in credentials["jira"] and credentials["jira"]["server"]:
            print(f"  Server: {credentials['jira']['server']}")
    else:
        print("  Status: Not configured")
    print()
    
    # Notion
    print("Notion:")
    if credentials["notion"]["token"]:
        masked_token = mask_token(credentials["notion"]["token"])
        print("  Status: Configured")
        print(f"  Token: {masked_token}")
    else:
        print("  Status: Not configured")
    print()
    
    # Neo4j
    print("Neo4j:")
    if credentials["neo4j"]["client_id"] and credentials["neo4j"]["client_secret"] and credentials["neo4j"]["uri"]:
        masked_client_id = mask_token(credentials["neo4j"]["client_id"])
        masked_client_secret = mask_token(credentials["neo4j"]["client_secret"])
        print("  Status: Configured")
        print(f"  URI: {credentials['neo4j']['uri']}")
        print(f"  Client ID: {masked_client_id}")
        print(f"  Client Secret: {masked_client_secret}")
        if "api_key" in credentials["neo4j"] and credentials["neo4j"]["api_key"]:
            masked_api_key = mask_token(credentials["neo4j"]["api_key"])
            print(f"  API Key: {masked_api_key}")
    else:
        print("  Status: Not configured")
    print()
    
    # OpenAI
    print("OpenAI:")
    if credentials["openai"]["api_key"]:
        masked_api_key = mask_token(credentials["openai"]["api_key"])
        print("  Status: Configured")
        print(f"  API Key: {masked_api_key}")
    else:
        print("  Status: Not configured")
    print()
    
    # AWS
    print("AWS:")
    aws_creds_path = os.path.expanduser("~/.aws/credentials")
    aws_config_path = os.path.expanduser("~/.aws/config")
    tpm_aws_config = os.path.join(CONFIG_DIR, "aws-config.json")
    
    if os.path.exists(aws_creds_path) or os.path.exists(aws_config_path):
        print("  Status: AWS credentials found")
        if os.path.exists(aws_creds_path):
            print(f"  Credentials: {aws_creds_path}")
        if os.path.exists(aws_config_path):
            print(f"  Config: {aws_config_path}")
        if os.path.exists(tpm_aws_config):
            print(f"  TPM AWS Config: {tpm_aws_config}")
    else:
        print("  Status: Not configured")

def configure_service(service, **kwargs):
    """Configure a specific service."""
    credentials = load_credentials()
    
    if service == "google":
        if "json_file" in kwargs:
            try:
                with open(kwargs["json_file"], 'r') as f:
                    credentials["google"] = json.load(f)
                save_credentials(credentials)
                print("Google Drive credentials saved successfully.")
            except Exception as e:
                raise Exception(f"Error loading Google credentials: {e}")
    
    elif service == "github":
        if "token" in kwargs:
            credentials["github"]["token"] = kwargs["token"]
            save_credentials(credentials)
            print("GitHub token saved successfully.")
    
    elif service == "jira":
        if "email" in kwargs:
            credentials["jira"]["email"] = kwargs["email"]
        if "token" in kwargs:
            credentials["jira"]["token"] = kwargs["token"]
        if "server" in kwargs and kwargs["server"]:
            credentials["jira"]["server"] = kwargs["server"]
        save_credentials(credentials)
        print("Jira credentials saved successfully.")
    
    elif service == "notion":
        if "token" in kwargs:
            credentials["notion"]["token"] = kwargs["token"]
            save_credentials(credentials)
            print("Notion API token saved successfully.")
    
    elif service == "neo4j":
        if "uri" in kwargs:
            credentials["neo4j"]["uri"] = kwargs["uri"]
        if "client_id" in kwargs:
            credentials["neo4j"]["client_id"] = kwargs["client_id"]
        if "client_secret" in kwargs:
            credentials["neo4j"]["client_secret"] = kwargs["client_secret"]
        if "api_key" in kwargs:
            credentials["neo4j"]["api_key"] = kwargs["api_key"]
        save_credentials(credentials)
        print("Neo4j credentials saved successfully.")
    
    elif service == "openai":
        if "api_key" in kwargs:
            credentials["openai"]["api_key"] = kwargs["api_key"]
            save_credentials(credentials)
            print("OpenAI API key saved successfully.")
    
    else:
        raise Exception(f"Unknown service: {service}")

def mask_token(token):
    """Mask a token for display."""
    if not token:
        return ""
    if len(token) <= 8:
        return "*" * len(token)
    return "*" * (len(token) - 4) + token[-4:]
