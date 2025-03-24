#!/usr/bin/env python3
"""
Project management commands for TPM-CLI.
"""

import os
import sys
import json
from tabulate import tabulate

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.project_utils import (
    create_project,
    get_project,
    list_projects,
    delete_project,
    set_project_neo4j,
    get_current_project,
    set_current_project,
    add_document_to_project
)
from utils.neo4j_utils import create_neo4j_database, get_neo4j_credentials

def cmd_project_create(args):
    """
    Create a new project.
    """
    # Create the project
    project = create_project(args.name, args.description)
    
    # If --create-db flag is set, create a Neo4j database for this project
    if args.create_db:
        print(f"Creating Neo4j database for project '{args.name}'...")
        
        # Check if Neo4j API key is configured
        neo4j_creds = get_neo4j_credentials()
        if not neo4j_creds or "api_key" not in neo4j_creds:
            print("Neo4j API key not configured. Please run 'tpm config neo4j --api-key YOUR_API_KEY' first.")
            return
        
        # Create database with project name
        db_name = f"tpm-{args.name.lower().replace(' ', '-')}"
        db_info = create_neo4j_database(db_name, region=args.region, tier=args.tier)
        
        if db_info:
            # Update project with Neo4j credentials
            instance_id = db_info.get("id")
            uri = db_info.get("connectionUri")
            username = db_info.get("username", "neo4j")
            password = db_info.get("password", "")
            
            set_project_neo4j(args.name, instance_id, uri, username, password)
            
            print(f"Neo4j database created and linked to project '{args.name}'.")
            print(f"Connection URI: {uri}")
            print(f"Username: {username}")
            print(f"Password: {password}")
    
    # If --set-current flag is set, set this as the current project
    if args.set_current:
        set_current_project(args.name)

def cmd_project_list(args):
    """
    List all projects.
    """
    projects = list_projects()
    
    if not projects:
        print("No projects found.")
        return
    
    # Get current project
    current_project = get_current_project()
    
    # Prepare table data
    table_data = []
    for name, project in projects.items():
        has_neo4j = "Yes" if project.get("neo4j_credentials") else "No"
        is_current = "Yes" if name == current_project else "No"
        
        table_data.append([
            name,
            project.get("description", ""),
            has_neo4j,
            is_current,
            project.get("created_at", "")
        ])
    
    # Print table
    print(tabulate(
        table_data,
        headers=["Name", "Description", "Has Neo4j", "Current", "Created At"],
        tablefmt="grid"
    ))

def cmd_project_info(args):
    """
    Show project information.
    """
    # If no project name provided, use current project
    project_name = args.name or get_current_project()
    
    if not project_name:
        print("No project specified and no current project set.")
        print("Use 'tpm project info PROJECT_NAME' or 'tpm project use PROJECT_NAME' first.")
        return
    
    project = get_project(project_name)
    
    if not project:
        print(f"Project '{project_name}' not found.")
        return
    
    # Print project information
    print(f"Project: {project_name}")
    print(f"Description: {project.get('description', '')}")
    print(f"Created: {project.get('created_at', '')}")
    
    # Neo4j information
    neo4j_creds = project.get("neo4j_credentials")
    if neo4j_creds:
        print("\nNeo4j Database:")
        print(f"  Instance ID: {project.get('neo4j_instance_id', '')}")
        print(f"  URI: {neo4j_creds.get('uri', '')}")
        print(f"  Username: {neo4j_creds.get('client_id', '')}")
        print(f"  Password: {'*' * 10}")
    else:
        print("\nNo Neo4j database configured for this project.")
    
    # Documents
    documents = project.get("documents", [])
    if documents:
        print("\nDocuments:")
        doc_table = []
        for doc in documents:
            doc_table.append([
                doc.get("name", ""),
                doc.get("type", ""),
                doc.get("id", ""),
                doc.get("added_at", "")
            ])
        
        print(tabulate(
            doc_table,
            headers=["Name", "Type", "ID", "Added At"],
            tablefmt="grid"
        ))
    else:
        print("\nNo documents added to this project.")

def cmd_project_use(args):
    """
    Set the current project.
    """
    success = set_current_project(args.name)
    
    if success:
        # Show project info
        cmd_project_info(args)

def cmd_project_delete(args):
    """
    Delete a project.
    """
    if not args.confirm:
        print(f"Are you sure you want to delete project '{args.name}'?")
        print("This action cannot be undone.")
        print("Use --confirm to confirm deletion.")
        return
    
    delete_project(args.name)

def cmd_project_add_document(args):
    """
    Add a document to a project.
    """
    # If no project name provided, use current project
    project_name = args.project or get_current_project()
    
    if not project_name:
        print("No project specified and no current project set.")
        print("Use 'tpm project add-document --project PROJECT_NAME' or 'tpm project use PROJECT_NAME' first.")
        return
    
    # Add document to project
    success = add_document_to_project(
        project_name,
        args.id,
        args.type,
        args.name
    )
    
    if success and args.import_to_neo4j:
        print(f"Importing document to Neo4j database for project '{project_name}'...")
        # This would call the appropriate import function based on document type
        # For now, we'll just print a message
        print("Document import to Neo4j not yet implemented.")

def cmd_project_add_neo4j(args):
    """
    Add a Neo4j database to an existing project.
    """
    # Get project name
    project_name = args.name or get_current_project()
    
    if not project_name:
        print("No project specified and no current project set.")
        print("Use 'tpm project add-neo4j PROJECT_NAME' or 'tpm project use PROJECT_NAME' first.")
        return
    
    # Check if project exists
    project = get_project(project_name)
    if not project:
        print(f"Project '{project_name}' not found.")
        return
    
    # Check if project already has a Neo4j database
    if project.get("neo4j_credentials"):
        print(f"Project '{project_name}' already has a Neo4j database.")
        print("To update the database, use 'tpm project update-neo4j' instead.")
        return
    
    # Check if Neo4j API key is configured
    neo4j_creds = get_neo4j_credentials()
    if not neo4j_creds or "api_key" not in neo4j_creds or not neo4j_creds["api_key"]:
        print("Neo4j API key not configured. Please run 'tpm config neo4j --api-key YOUR_API_KEY' first.")
        return
    
    # Create database with project name
    db_name = f"tpm-{project_name.lower().replace(' ', '-')}"
    print(f"Creating Neo4j database '{db_name}' for project '{project_name}'...")
    db_info = create_neo4j_database(db_name, region=args.region, tier=args.tier)
    
    if db_info:
        # Update project with Neo4j credentials
        instance_id = db_info.get("id")
        uri = db_info.get("connectionUri")
        username = db_info.get("username", "neo4j")
        password = db_info.get("password", "")
        
        set_project_neo4j(project_name, instance_id, uri, username, password)
        
        print(f"Neo4j database created and linked to project '{project_name}'.")
        print(f"Connection URI: {uri}")
        print(f"Username: {username}")
        print(f"Password: {password}")

def cmd_project_set_neo4j(args):
    """
    Set Neo4j connection details for a project manually.
    """
    # Get project name
    project_name = args.name or get_current_project()
    
    if not project_name:
        print("No project specified and no current project set.")
        print("Use 'tpm project set-neo4j --name PROJECT_NAME' or 'tpm project use PROJECT_NAME' first.")
        return
    
    # Check if project exists
    project = get_project(project_name)
    if not project:
        print(f"Project '{project_name}' not found.")
        return
    
    # Check if required parameters are provided
    if not (args.uri and args.client_id and args.client_secret):
        print("Please provide all required Neo4j connection details:")
        print("--uri, --client-id, and --client-secret")
        return
    
    # Set Neo4j connection details
    instance_id = "manual-connection"  # Placeholder for manually configured connection
    set_project_neo4j(project_name, instance_id, args.uri, args.client_id, args.client_secret)
    
    print(f"Neo4j credentials for project '{project_name}' updated successfully.")
    print(f"Neo4j connection details for project '{project_name}' set successfully.")
    print(f"Connection URI: {args.uri}")
    print(f"Client ID: {args.client_id}")
    print(f"Client Secret: {'*' * len(args.client_secret)}")
