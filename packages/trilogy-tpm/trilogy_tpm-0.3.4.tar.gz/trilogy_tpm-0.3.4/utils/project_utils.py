#!/usr/bin/env python3
"""
Project utilities for TPM-CLI.
"""

import os
import sys
import json
from utils.config_utils import get_credential, set_credential, CONFIG_DIR
from pathlib import Path
import datetime

# Constants
PROJECTS_FILE = os.path.join(CONFIG_DIR, "projects.json")

def load_projects():
    """
    Load projects from the projects file.
    
    Returns:
        dict: Dictionary of projects
    """
    if not os.path.exists(PROJECTS_FILE):
        return {}
    
    try:
        with open(PROJECTS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading projects: {str(e)}")
        return {}

def save_projects(projects):
    """
    Save projects to the projects file.
    
    Args:
        projects (dict): Dictionary of projects to save
    """
    try:
        with open(PROJECTS_FILE, 'w') as f:
            json.dump(projects, f, indent=2)
    except Exception as e:
        print(f"Error saving projects: {str(e)}")

def create_project(name, description=None, neo4j_instance_id=None):
    """
    Create a new project.
    
    Args:
        name (str): Project name
        description (str, optional): Project description
        neo4j_instance_id (str, optional): ID of the Neo4j instance for this project
    
    Returns:
        dict: Project information
    """
    projects = load_projects()
    
    # Check if project already exists
    if name in projects:
        print(f"Project '{name}' already exists.")
        return projects[name]
    
    # Create new project
    project = {
        "name": name,
        "description": description or "",
        "neo4j_instance_id": neo4j_instance_id,
        "neo4j_credentials": None,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "documents": [],
        "repositories": []
    }
    
    # Save project
    projects[name] = project
    save_projects(projects)
    
    print(f"Project '{name}' created successfully.")
    return project

def get_project(name):
    """
    Get a project by name.
    
    Args:
        name (str): Project name
    
    Returns:
        dict: Project information or None if not found
    """
    projects = load_projects()
    return projects.get(name)

def list_projects():
    """
    List all projects.
    
    Returns:
        dict: Dictionary of projects
    """
    return load_projects()

def delete_project(name):
    """
    Delete a project.
    
    Args:
        name (str): Project name
    
    Returns:
        bool: True if successful, False otherwise
    """
    projects = load_projects()
    
    if name not in projects:
        print(f"Project '{name}' not found.")
        return False
    
    # Remove project
    del projects[name]
    save_projects(projects)
    
    print(f"Project '{name}' deleted successfully.")
    return True

def set_project_neo4j(project_name, instance_id, uri, client_id, client_secret):
    """
    Set Neo4j credentials for a project.
    
    Args:
        project_name (str): Project name
        instance_id (str): Neo4j instance ID
        uri (str): Neo4j URI
        client_id (str): Neo4j client ID
        client_secret (str): Neo4j client secret
    
    Returns:
        bool: True if successful, False otherwise
    """
    projects = load_projects()
    
    if project_name not in projects:
        print(f"Project '{project_name}' not found.")
        return False
    
    # Update project with Neo4j credentials
    projects[project_name]["neo4j_instance_id"] = instance_id
    projects[project_name]["neo4j_credentials"] = {
        "uri": uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    save_projects(projects)
    
    print(f"Neo4j credentials for project '{project_name}' updated successfully.")
    return True

def get_project_neo4j_credentials(project_name):
    """
    Get Neo4j credentials for a project.
    
    Args:
        project_name (str): Project name
    
    Returns:
        dict: Neo4j credentials or None if not found
    """
    project = get_project(project_name)
    
    if not project:
        print(f"Project '{project_name}' not found.")
        return None
    
    return project.get("neo4j_credentials")

def add_document_to_project(project_name, document_id, document_type, document_name):
    """
    Add a document to a project.
    
    Args:
        project_name (str): Project name
        document_id (str): Document ID
        document_type (str): Document type (e.g., google_sheet, github_repo)
        document_name (str): Document name
    
    Returns:
        bool: True if successful, False otherwise
    """
    projects = load_projects()
    
    if project_name not in projects:
        print(f"Project '{project_name}' not found.")
        return False
    
    # Add document to project
    document = {
        "id": document_id,
        "type": document_type,
        "name": document_name,
        "added_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    projects[project_name]["documents"].append(document)
    save_projects(projects)
    
    print(f"Document '{document_name}' added to project '{project_name}'.")
    return True

def get_current_project():
    """
    Get the current project from the environment.
    
    Returns:
        str: Current project name or None if not set
    """
    # First check environment variable
    project_name = os.environ.get("TPM_PROJECT")
    
    # If not in environment, check local .tpm-project file
    if not project_name and os.path.exists(".tpm-project"):
        try:
            with open(".tpm-project", 'r') as f:
                project_name = f.read().strip()
        except:
            pass
    
    return project_name

def set_current_project(project_name):
    """
    Set the current project in the local directory.
    
    Args:
        project_name (str): Project name
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Check if project exists
    if not get_project(project_name):
        print(f"Project '{project_name}' not found.")
        return False
    
    # Create .tpm-project file
    try:
        with open(".tpm-project", 'w') as f:
            f.write(project_name)
        print(f"Current project set to '{project_name}'.")
        return True
    except Exception as e:
        print(f"Error setting current project: {str(e)}")
        return False
