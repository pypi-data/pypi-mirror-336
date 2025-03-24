# TPM CLI

A command-line tool for Technical Project Managers to interact with GitHub repositories, Google Drive documents, AWS services, and Jira.

## Installation

```bash
pip install tpm-cli
```

## Features

- **GitHub Repository Management**: Search for repositories, get repository information.
- **Google Drive Integration**: List, get, and search Google Drive documents.
- **AWS CLI Integration**: Run AWS CLI commands with assumed role credentials, manage configuration, and view CloudWatch logs.
- **Jira Integration**: Get ticket details, search for tickets, test connectivity, and list accessible projects.

## Usage

### GitHub Repositories

```bash
# Search for repositories
tpm repo "search query" --org "organization"

# Get repository information
tpm repo "exact-repo-name" --org "organization"

# Output to file
tpm repo "search query" --output "output.md"
```

### Google Drive

```bash
# List Google Drive files
tpm google list --query "search query"
tpm google list --folder "folder-id"

# Get a Google Drive document
tpm google get "document-id" --format md
tpm google get "https://docs.google.com/document/d/..." --output "output.md"

# Search within a Google Drive document
tpm google search "document-id" "search query"
```

### AWS

```bash
# Run AWS CLI commands with assumed role credentials
tpm aws run -a 123456789012 s3 ls
tpm aws run -a 123456789012 -r CustomRoleName ec2 describe-instances
tpm aws run s3 ls  # Uses default target account if set during setup

# Configure default settings
tpm aws config
tpm aws config --set-role CustomRoleName
tpm aws config --set-source-profile my-profile

# Show recently used accounts
tpm aws recent

# Quick setup for SaaS and target accounts
tpm aws setup -s 123456789012 -t 987654321098
tpm aws setup -s 123456789012  # Set up with just SaaS account

# Get logs from CloudWatch Logs using sam logs
tpm aws logs "log-group-name" --filter "filter-pattern" --start "5m"
tpm aws logs "log-group-name" --filter "filter-pattern" --start "1h"
tpm aws logs "log-group-name" --filter "filter-pattern" --start "1d"
```

### Jira

```bash
# Get a Jira ticket
tpm jira get PROJ-123
tpm jira get PROJ-123 --output ticket.md

# Search for Jira tickets
tpm jira search "project = PROJ AND status = Open ORDER BY created DESC" --limit 10

# Test Jira connectivity
tpm jira test

# List accessible Jira projects
tpm jira projects

# Configure Jira credentials
tpm config jira --email "your.email@example.com" --token "your-api-token"
```

## AWS Command Details

The `aws` command provides several subcommands for interacting with AWS services:

### run

Run AWS CLI commands with assumed role credentials.

```bash
tpm aws run [options] [AWS CLI command and arguments]
```

Options:
- `-a, --account`: Target AWS account ID (optional if default target is set)
- `-r, --role`: Role name to assume
- `-s, --source-profile`: Source profile for role chaining
- `--saas-account`: SaaS account ID for role chaining
- `--saas-role`: SaaS role name for role chaining
- `--debug`: Enable debug logging

Examples:
```bash
tpm aws run -a 123456789012 s3 ls
tpm aws run -a 123456789012 -r CustomRoleName ec2 describe-instances
tpm aws run s3 ls  # Uses default target account if set during setup
tpm aws run -s my-profile --saas-account 123456789012 s3 ls  # Uses role chaining
```

### config

Configure default settings for AWS.

```bash
tpm aws config [options]
```

Options:
- `-a, --account`: Target AWS account ID
- `-r, --role`: Role name to assume
- `--set-role`: Set default role
- `--set-saas-role`: Set default SaaS role for role chaining
- `--set-source-profile`: Set default source profile for role chaining
- `--source-profile`: Source profile for role chaining
- `--saas-account`: SaaS account ID for role chaining
- `--debug`: Enable debug logging

### recent

Show recently used AWS accounts.

```bash
tpm aws recent [options]
```

Options:
- `-a, --account`: Target AWS account ID
- `-r, --role`: Role name to assume
- `-s, --source-profile`: Source profile for role chaining
- `--saas-account`: SaaS account ID for role chaining
- `--debug`: Enable debug logging

### setup

Quick setup for SaaS and target accounts.

```bash
tpm aws setup [options]
```

Options:
- `-s, --saas-account`: SaaS AWS account ID (required)
- `-t, --target-account`: Target AWS account ID (optional)
- `-r, --role`: Role name to assume
- `--saas-role`: SaaS role name for role chaining
- `--source-profile`: Source profile for role chaining
- `--debug`: Enable debug logging

### logs

Get logs from CloudWatch Logs using sam logs.

```bash
tpm aws logs [log-group] [options]
```

Options:
- `--filter`: Filter pattern
- `--start`: Start time (e.g., 5m, 1h, 1d)
- `--debug`: Enable debug logging

Examples:
```bash
tpm aws logs "log-group-name" --filter "filter-pattern" --start "5m"
tpm aws logs "log-group-name" --filter "filter-pattern" --start "1h"
tpm aws logs "log-group-name" --filter "filter-pattern" --start "1d"
```

## Project Structure

The TPM CLI is organized with a modular structure:

```
tpm-cli/
├── commands/         # Command modules for each service
│   ├── __init__.py
│   ├── aws_commands.py
│   ├── github_commands.py
│   ├── google_commands.py
│   ├── jira_commands.py
│   ├── neo4j_commands.py
│   ├── notion_commands.py
│   └── ...
├── utils/            # Utility functions
│   ├── __init__.py
│   ├── aws_utils.py
│   ├── github_utils.py
│   ├── google_utils.py
│   ├── jira_utils.py
│   ├── neo4j_utils.py
│   ├── notion_utils.py
│   └── ...
├── tests/            # Test modules
│   ├── __init__.py
│   └── ...
├── tpm               # Main CLI entry point
├── setup.py          # Package setup file
└── README.md
```

## Installation Options

You can install the TPM CLI in two ways:

### 1. Global Installation

```bash
pip install .
```

This will install the `tpm` command globally, allowing you to run it from anywhere.

### 2. Virtual Environment Installation

```bash
./install.sh
```

This script will create a virtual environment and install the TPM CLI within it.

## Configuration

The TPM CLI stores credentials in `~/.tpm-cli/credentials.json` for all services except AWS, which uses the standard AWS credential files.

To configure credentials:

```bash
# Configure Google Drive
tpm config google --json-file /path/to/credentials.json

# Configure GitHub
tpm config github --token your-github-token

# Configure Jira
tpm config jira --email your-email --token your-jira-token

# Configure Neo4j
tpm config neo4j --uri your-neo4j-uri --client-id your-client-id --client-secret your-client-secret
```

## Development

To contribute to the TPM CLI, clone the repository and install in development mode:

```bash
git clone https://github.com/yourusername/tpm-cli.git
cd tpm-cli
pip install -e .
```

## License

MIT
