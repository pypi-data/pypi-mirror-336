#!/usr/bin/env python3
"""
Neo4j commands for TPM-CLI.
"""

import os
import sys
import json
from utils import neo4j_utils
from utils.config_utils import get_credential, set_credential

def cmd_neo4j(args):
    """Handle Neo4j commands."""
    if not hasattr(args, 'subcommand') or not args.subcommand:
        print("Error: No subcommand specified for 'neo4j' command")
        print("Available subcommands: cypher, graphql, rag")
        sys.exit(1)
    
    if args.subcommand == 'cypher':
        cmd_neo4j_cypher(args)
    elif args.subcommand == 'graphql':
        cmd_neo4j_graphql(args)
    elif args.subcommand == 'rag':
        cmd_neo4j_rag(args)
    else:
        print(f"Error: Unknown subcommand '{args.subcommand}' for 'neo4j' command")
        sys.exit(1)

def cmd_neo4j_cypher(args):
    """Handle Neo4j Cypher subcommands."""
    if not hasattr(args, 'cypher_action') or not args.cypher_action:
        print("Error: No action specified for 'neo4j cypher' command")
        print("Available actions: query, run")
        sys.exit(1)
    
    if args.cypher_action == 'query':
        cmd_neo4j_cypher_query(args)
    elif args.cypher_action == 'run':
        cmd_neo4j_cypher_run(args)
    else:
        print(f"Error: Unknown action '{args.cypher_action}' for 'neo4j cypher' command")
        sys.exit(1)

def cmd_neo4j_cypher_query(args):
    """Execute a read-only Cypher query and display the results."""
    try:
        # Get credentials
        creds = neo4j_utils.get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            sys.exit(1)
        
        # Execute query
        results = neo4j_utils.execute_cypher_query(
            query=args.query,
            params=json.loads(args.params) if args.params else None
        )
        
        # Format and output results
        formatted_results = neo4j_utils.format_cypher_results(results, args.format)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(formatted_results)
            print(f"Query results saved to {args.output}")
        else:
            print(formatted_results)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_neo4j_cypher_run(args):
    """Execute a Cypher query that can modify the database."""
    try:
        # Get credentials
        creds = neo4j_utils.get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            sys.exit(1)
        
        # Execute query
        results = neo4j_utils.execute_cypher_query(
            query=args.query,
            params=json.loads(args.params) if args.params else None
        )
        
        # Format and output results
        formatted_results = neo4j_utils.format_cypher_results(results, args.format)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(formatted_results)
            print(f"Query results saved to {args.output}")
        else:
            print(formatted_results)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_neo4j_graphql(args):
    """Handle Neo4j GraphQL subcommands."""
    if not hasattr(args, 'graphql_action') or not args.graphql_action:
        print("Error: No action specified for 'neo4j graphql' command")
        print("Available actions: create, list, get, delete, query, auth, cors")
        sys.exit(1)
    
    if args.graphql_action == 'create':
        cmd_neo4j_graphql_create(args)
    elif args.graphql_action == 'list':
        cmd_neo4j_graphql_list(args)
    elif args.graphql_action == 'get':
        cmd_neo4j_graphql_get(args)
    elif args.graphql_action == 'delete':
        cmd_neo4j_graphql_delete(args)
    elif args.graphql_action == 'query':
        cmd_neo4j_graphql_query(args)
    elif args.graphql_action == 'auth':
        cmd_neo4j_graphql_auth(args)
    elif args.graphql_action == 'cors':
        cmd_neo4j_graphql_cors(args)
    else:
        print(f"Error: Unknown action '{args.graphql_action}' for 'neo4j graphql' command")
        sys.exit(1)

def cmd_neo4j_graphql_create(args):
    """Create a new GraphQL API for Neo4j."""
    try:
        # Get credentials
        creds = neo4j_utils.get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            sys.exit(1)
        
        # Create GraphQL API
        result = neo4j_utils.create_graphql_api(
            name=args.name,
            description=args.description,
            database_id=args.database_id
        )
        
        print(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_neo4j_graphql_list(args):
    """List GraphQL APIs for Neo4j."""
    try:
        # Get credentials
        creds = neo4j_utils.get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            sys.exit(1)
        
        # List GraphQL APIs
        result = neo4j_utils.list_graphql_apis()
        
        print(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_neo4j_graphql_get(args):
    """Get details of a GraphQL API for Neo4j."""
    try:
        # Get credentials
        creds = neo4j_utils.get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            sys.exit(1)
        
        # Get GraphQL API details
        result = neo4j_utils.get_graphql_api(args.api_id)
        
        print(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_neo4j_graphql_delete(args):
    """Delete a GraphQL API for Neo4j."""
    try:
        # Get credentials
        creds = neo4j_utils.get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            sys.exit(1)
        
        # Delete GraphQL API
        result = neo4j_utils.delete_graphql_api(args.api_id)
        
        print(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_neo4j_graphql_query(args):
    """Execute a GraphQL query against a Neo4j GraphQL API."""
    try:
        # Get credentials
        creds = neo4j_utils.get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            sys.exit(1)
        
        # Read query from file if provided
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                query = f.read()
        else:
            query = args.query
        
        # Read variables from file if provided
        variables = None
        if args.variables:
            with open(args.variables, 'r', encoding='utf-8') as f:
                variables = json.load(f)
        
        # Execute GraphQL query
        result = neo4j_utils.execute_graphql_query(
            api_id=args.api_id,
            query=query,
            variables=variables
        )
        
        print(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_neo4j_graphql_auth(args):
    """Manage authentication providers for a Neo4j GraphQL API."""
    try:
        # Get credentials
        creds = neo4j_utils.get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            sys.exit(1)
        
        # Parse auth params if provided
        auth_params = {}
        if args.auth_params:
            auth_params = json.loads(args.auth_params)
        
        # Manage GraphQL API auth
        result = neo4j_utils.manage_graphql_auth(
            api_id=args.api_id,
            action=args.auth_action,
            auth_type=args.auth_type,
            auth_params=auth_params
        )
        
        print(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_neo4j_graphql_cors(args):
    """Manage CORS policies for a Neo4j GraphQL API."""
    try:
        # Get credentials
        creds = neo4j_utils.get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            sys.exit(1)
        
        # Manage GraphQL API CORS
        result = neo4j_utils.manage_graphql_cors(
            api_id=args.api_id,
            action=args.cors_action,
            origin=args.origin
        )
        
        print(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def cmd_neo4j_rag(args):
    """Handle Neo4j RAG subcommands."""
    if not hasattr(args, 'rag_action') or not args.rag_action:
        print("Error: No action specified for 'neo4j rag' command")
        print("Available actions: create-index, ingest, query, build-kg")
        sys.exit(1)
    
    if args.rag_action == 'create-index':
        cmd_neo4j_rag_create_index(args)
    elif args.rag_action == 'ingest':
        cmd_neo4j_rag_ingest(args)
    elif args.rag_action == 'query':
        cmd_neo4j_rag_query(args)
    elif args.rag_action == 'build-kg':
        cmd_neo4j_rag_build_kg(args)
    else:
        print(f"Error: Unknown action '{args.rag_action}' for 'neo4j rag' command")
        sys.exit(1)

def cmd_neo4j_rag_create_index(args):
    """Command handler for creating a vector index for RAG."""
    try:
        result = neo4j_utils.create_rag_vector_index(
            args.index_name,
            label=args.label,
            embedding_property=args.embedding_property,
            dimensions=args.dimensions
        )
        print(result)
    except Exception as e:
        print(f"Error creating vector index: {str(e)}")
        sys.exit(1)

def cmd_neo4j_rag_ingest(args):
    """Command handler for ingesting a document into the vector store."""
    # Get text content from either --text or --file
    if args.text:
        text = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            sys.exit(1)
    else:
        print("Error: Either --text or --file must be provided")
        sys.exit(1)
    
    # Parse metadata if provided
    metadata = None
    if args.metadata:
        try:
            metadata = json.loads(args.metadata)
        except json.JSONDecodeError:
            print("Error: Metadata must be a valid JSON string")
            sys.exit(1)
    
    try:
        # Use the enhanced ingest_document function
        result = neo4j_utils.ingest_document(
            args.index_name,
            text,
            metadata=metadata,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap
        )
        print(result)
    except Exception as e:
        print(f"Error ingesting document: {str(e)}")
        sys.exit(1)

def cmd_neo4j_rag_query(args):
    """Command handler for querying the RAG system."""
    try:
        # Use the enhanced rag_query function
        result = neo4j_utils.rag_query(
            args.index_name,
            args.query,
            top_k=args.top_k
        )
        
        # Format output based on user preference
        if args.format == 'json':
            output = json.dumps(result, indent=2)
        else:  # markdown format
            output = f"# Answer\n\n{result['answer']}\n\n# Sources\n\n"
            for i, source in enumerate(result['context']):
                output += f"## Source {i+1} (Score: {source['score']:.4f})\n\n{source['text']}\n\n"
        
        # Write to file or print to console
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Response written to {args.output}")
        else:
            print(output)
    except Exception as e:
        print(f"Error querying RAG system: {str(e)}")
        sys.exit(1)

def cmd_neo4j_rag_build_kg(args):
    """Command handler for building a knowledge graph from text."""
    # Get text content from either --text or --file
    if args.text:
        text = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            sys.exit(1)
    else:
        print("Error: Either --text or --file must be provided")
        sys.exit(1)
    
    # Parse entities and relations if provided
    entities = None
    if args.entities:
        try:
            entities = json.loads(args.entities)
        except json.JSONDecodeError:
            print("Error: Entities must be a valid JSON array")
            sys.exit(1)
    
    relations = None
    if args.relations:
        try:
            relations = json.loads(args.relations)
        except json.JSONDecodeError:
            print("Error: Relations must be a valid JSON array")
            sys.exit(1)
    
    try:
        # Use the enhanced build_knowledge_graph function
        result = neo4j_utils.build_knowledge_graph(
            text,
            entities=entities,
            relations=relations
        )
        
        # Print the result in a formatted way
        print(result["message"])
        print("\nExtracted Entities:")
        for entity in result["entities"]:
            print(f"  - {entity['text']} ({entity['type']})")
        
        print("\nExtracted Relations:")
        for relation in result["relations"]:
            print(f"  - {relation['source']} ({relation['source_type']}) --[{relation['type']}]--> {relation['target']} ({relation['target_type']})")
    except Exception as e:
        print(f"Error building knowledge graph: {str(e)}")
        sys.exit(1)
