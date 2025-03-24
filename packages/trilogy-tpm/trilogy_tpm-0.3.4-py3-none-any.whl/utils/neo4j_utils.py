#!/usr/bin/env python3
"""
Neo4j utilities for TPM-CLI.
"""

import os
import sys
import json
import requests
import subprocess
import tempfile
from neo4j import GraphDatabase
from tabulate import tabulate
from utils.config_utils import get_credential, set_credential
from utils.project_utils import get_current_project, get_project_neo4j_credentials

# Constants
CREDENTIALS_DIR = os.path.expanduser("~/.tpm-cli")
LOCAL_CREDENTIALS_FILE = os.path.expanduser("~/.tpm-cli/credentials.json")

def get_neo4j_credentials():
    """Load Neo4j credentials from the centralized config."""
    # First, check if there's a current project with Neo4j credentials
    current_project = get_current_project()
    if current_project:
        project_creds = get_project_neo4j_credentials(current_project)
        if project_creds:
            print(f"Using Neo4j credentials from project: {current_project}")
            return project_creds
    
    # If no project credentials, try to get credentials from centralized config
    neo4j_creds = get_credential("neo4j")
    if neo4j_creds:
        return neo4j_creds
    
    # If not found, return None - will need to be configured
    return None

def get_openai_api_key():
    """Load OpenAI API key from the centralized config."""
    # Try to get credentials from centralized config
    openai_creds = get_credential("openai")
    if openai_creds and "api_key" in openai_creds:
        return openai_creds["api_key"]
    
    # If not found in config, try environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    # If not found, return None
    return None

def create_neo4j_driver(uri=None, client_id=None, client_secret=None):
    """Create a Neo4j driver using the provided or stored credentials."""
    # If credentials not provided, try to get from config
    if not (client_id and client_secret and uri):
        creds = get_neo4j_credentials()
        if creds:
            uri = creds.get("uri")
            client_id = creds.get("client_id")
            client_secret = creds.get("client_secret")
        else:
            raise ValueError("Neo4j credentials not found. Please configure using 'tpm config neo4j'")
    
    # Create driver
    try:
        driver = GraphDatabase.driver(uri, auth=(client_id, client_secret))
        # Test connection
        with driver.session() as session:
            session.run("RETURN 1")
        return driver
    except Exception as e:
        raise ConnectionError(f"Failed to connect to Neo4j: {str(e)}")

def execute_cypher_query(query, params=None, uri=None, client_id=None, client_secret=None):
    """Execute a Cypher query and return the results."""
    driver = create_neo4j_driver(uri, client_id, client_secret)
    
    try:
        with driver.session() as session:
            result = session.run(query, params or {})
            # Convert result to a list of dictionaries
            records = [dict(record) for record in result]
            return records
    except Exception as e:
        raise Exception(f"Error executing Cypher query: {str(e)}")
    finally:
        driver.close()

def format_cypher_results(results, format='table'):
    """Format Cypher query results in the specified format."""
    if not results:
        return "No results returned."
    
    if format == 'json':
        return json.dumps(results, indent=2)
    
    elif format == 'md':
        # Create markdown table
        if not results:
            return "No results returned."
        
        # Extract headers
        headers = list(results[0].keys())
        
        # Create table rows
        rows = []
        for record in results:
            row = []
            for header in headers:
                value = record.get(header, "")
                # Format value for markdown
                if isinstance(value, (dict, list)):
                    value = json.dumps(value)
                row.append(str(value))
            rows.append(row)
        
        # Create markdown table
        md_table = "| " + " | ".join(headers) + " |\n"
        md_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        
        for row in rows:
            md_table += "| " + " | ".join(row) + " |\n"
        
        return md_table
    
    else:  # Default to table format
        # Extract headers and rows for tabulate
        if not results:
            return "No results returned."
        
        headers = list(results[0].keys())
        rows = []
        
        for record in results:
            row = []
            for header in headers:
                value = record.get(header, "")
                # Format complex values
                if isinstance(value, (dict, list)):
                    value = json.dumps(value)
                row.append(value)
            rows.append(row)
        
        return tabulate(rows, headers=headers, tablefmt="grid")

# GraphQL utilities

def execute_graphql_command(command, args=None):
    """Execute an Aura CLI GraphQL command."""
    # Check if Aura CLI is installed
    try:
        subprocess.run(["aura", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError("Aura CLI not found. Please install it using 'npm install -g @neo4j/aura-cli'")
    
    # Build command
    cmd = ["aura", "graphql", command]
    if args:
        cmd.extend(args)
    
    # Execute command
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error executing Aura CLI command: {e.stderr}")

def create_graphql_api(name, description=None, database_id=None):
    """Create a new GraphQL API for Neo4j."""
    args = ["--name", name]
    if description:
        args.extend(["--description", description])
    if database_id:
        args.extend(["--database-id", database_id])
    
    return execute_graphql_command("create", args)

def list_graphql_apis():
    """List all GraphQL APIs."""
    return execute_graphql_command("list")

def get_graphql_api(api_id):
    """Get details of a specific GraphQL API."""
    return execute_graphql_command("get", [api_id])

def delete_graphql_api(api_id):
    """Delete a GraphQL API."""
    return execute_graphql_command("delete", [api_id])

def execute_graphql_query(api_id, query, variables=None):
    """Execute a GraphQL query against a Neo4j GraphQL API."""
    # Create temporary file for query
    with tempfile.NamedTemporaryFile(mode='w', suffix='.graphql', delete=False) as query_file:
        query_file.write(query)
        query_file_path = query_file.name
    
    try:
        args = [api_id, "--file", query_file_path]
        if variables:
            # Create temporary file for variables
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as vars_file:
                json.dump(variables, vars_file)
                vars_file_path = vars_file.name
            args.extend(["--variables", vars_file_path])
            
            try:
                return execute_graphql_command("query", args)
            finally:
                os.unlink(vars_file_path)
        else:
            return execute_graphql_command("query", args)
    finally:
        os.unlink(query_file_path)

def manage_graphql_auth(api_id, action, auth_type=None, auth_params=None):
    """Manage authentication providers for a GraphQL API."""
    if action not in ["add", "list", "remove"]:
        raise ValueError("Action must be one of: add, list, remove")
    
    args = [api_id, action]
    
    if action == "add" and auth_type:
        args.append(auth_type)
        if auth_params:
            for key, value in auth_params.items():
                args.extend([f"--{key}", value])
    
    elif action == "remove" and auth_type:
        args.append(auth_type)
    
    return execute_graphql_command("auth", args)

def manage_graphql_cors(api_id, action, origin=None):
    """Manage CORS policies for a GraphQL API."""
    if action not in ["add", "list", "remove"]:
        raise ValueError("Action must be one of: add, list, remove")
    
    args = [api_id, action]
    
    if action in ["add", "remove"] and origin:
        args.append(origin)
    
    return execute_graphql_command("cors", args)

# Database management utilities

def create_neo4j_database(name, region="us-east-1", tier="free"):
    """
    Create a new Neo4j Aura database instance.
    
    Args:
        name (str): Name for the new database
        region (str): AWS region for the database (default: us-east-1)
        tier (str): Database tier (free, professional, enterprise)
    
    Returns:
        dict: Database information including connection details
    """
    try:
        import requests
        
        # Get Neo4j credentials
        creds = get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            return None
        
        # Prepare API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {creds.get('api_key', '')}"
        }
        
        # Validate tier
        valid_tiers = ["free", "professional", "enterprise"]
        if tier not in valid_tiers:
            print(f"Invalid tier: {tier}. Must be one of {valid_tiers}")
            return None
            
        # Prepare request data
        data = {
            "name": name,
            "region": region,
            "tier": tier
        }
        
        # Make API request to create database
        response = requests.post(
            "https://api.neo4j.io/v1/instances",
            headers=headers,
            json=data
        )
        
        # Check response
        if response.status_code in [200, 201]:
            db_info = response.json()
            print(f"Database '{name}' created successfully!")
            
            # Update credentials with new database info
            new_uri = db_info.get("connectionUri")
            if new_uri:
                # Update credentials
                creds["uri"] = new_uri
                set_credential("neo4j", creds)
                print(f"Neo4j connection URI updated to: {new_uri}")
            
            return db_info
        else:
            print(f"Failed to create database. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error creating Neo4j database: {str(e)}")
        return None

def list_neo4j_databases():
    """
    List all Neo4j Aura database instances.
    
    Returns:
        list: List of database instances
    """
    try:
        import requests
        
        # Get Neo4j credentials
        creds = get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            return None
        
        # Prepare API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {creds.get('api_key', '')}"
        }
        
        # Make API request to list databases
        response = requests.get(
            "https://api.neo4j.io/v1/instances",
            headers=headers
        )
        
        # Check response
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to list databases. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error listing Neo4j databases: {str(e)}")
        return None

def get_neo4j_database(instance_id):
    """
    Get details of a specific Neo4j Aura database instance.
    
    Args:
        instance_id (str): ID of the database instance
    
    Returns:
        dict: Database information
    """
    try:
        import requests
        
        # Get Neo4j credentials
        creds = get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            return None
        
        # Prepare API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {creds.get('api_key', '')}"
        }
        
        # Make API request to get database details
        response = requests.get(
            f"https://api.neo4j.io/v1/instances/{instance_id}",
            headers=headers
        )
        
        # Check response
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get database details. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error getting Neo4j database details: {str(e)}")
        return None

def delete_neo4j_database(instance_id):
    """
    Delete a Neo4j Aura database instance.
    
    Args:
        instance_id (str): ID of the database instance to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import requests
        
        # Get Neo4j credentials
        creds = get_neo4j_credentials()
        if not creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            return False
        
        # Prepare API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {creds.get('api_key', '')}"
        }
        
        # Make API request to delete database
        response = requests.delete(
            f"https://api.neo4j.io/v1/instances/{instance_id}",
            headers=headers
        )
        
        # Check response
        if response.status_code in [200, 202, 204]:
            print(f"Database with ID '{instance_id}' deleted successfully!")
            return True
        else:
            print(f"Failed to delete database. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error deleting Neo4j database: {str(e)}")
        return False

# RAG (Retrieval Augmented Generation) utilities

def initialize_rag_components(embedder_type="openai", llm_type="openai"):
    """Initialize RAG components based on the specified types."""
    try:
        # Import core components
        from neo4j_graphrag.embeddings import OpenAIEmbeddings, OllamaEmbeddings
        from neo4j_graphrag.llm import OpenAILLM, OllamaLLM
        from neo4j_graphrag.indexes import create_vector_index, upsert_vectors
        
        # Import retrievers
        from neo4j_graphrag.retrievers import (
            VectorRetriever, 
            VectorCypherRetriever, 
            HybridRetriever, 
            HybridCypherRetriever,
            Text2CypherRetriever
        )
        
        # Import experimental components
        from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter
        from neo4j_graphrag.experimental.components.text_splitters.langchain import LangChainTextSplitterAdapter
        from neo4j_graphrag.experimental.components.embedder import TextChunkEmbedder
        from neo4j_graphrag.experimental.components.lexical_graph import LexicalGraphBuilder
        from neo4j_graphrag.experimental.components.schema import SchemaBuilder, SchemaEntity, SchemaRelation
        from neo4j_graphrag.experimental.components.entity_relation_extractor import LLMEntityRelationExtractor
        from neo4j_graphrag.experimental.components.kg_writer import Neo4jWriter
        from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
        from neo4j_graphrag.experimental.pipeline import Pipeline
        
        # Import types
        from neo4j_graphrag.types import EntityType
    except ImportError:
        raise ImportError("neo4j-graphrag package not found. Please install it using 'pip install neo4j-graphrag'")
    
    # Get credentials
    creds = get_neo4j_credentials()
    if not creds:
        raise ValueError("Neo4j credentials not found. Please run 'tpm config neo4j' first.")
    
    # Create driver
    driver = create_neo4j_driver()
    
    # Initialize embedder
    if embedder_type == "openai":
        # Get OpenAI API key from config
        openai_api_key = get_openai_api_key()
        if not openai_api_key:
            raise ValueError("OpenAI API key not found. Please run 'tpm config openai --api-key YOUR_KEY' first.")
        
        # Set the API key in the environment
        os.environ["OPENAI_API_KEY"] = openai_api_key
        
        embedder = OpenAIEmbeddings(model="text-embedding-3-large")
    elif embedder_type == "ollama":
        embedder = OllamaEmbeddings(model="llama2")
    else:
        raise ValueError(f"Unsupported embedder type: {embedder_type}")
    
    # Initialize LLM
    if llm_type == "openai":
        # Get OpenAI API key from config (already set in environment above)
        openai_api_key = get_openai_api_key()
        if not openai_api_key:
            raise ValueError("OpenAI API key not found. Please run 'tpm config openai --api-key YOUR_KEY' first.")
        
        llm = OpenAILLM(model_name="gpt-4o", model_params={"temperature": 0})
    elif llm_type == "ollama":
        llm = OllamaLLM(model_name="llama2")
    else:
        raise ValueError(f"Unsupported LLM type: {llm_type}")
    
    # Create text splitter
    text_splitter = FixedSizeSplitter(chunk_size=1000, chunk_overlap=200)
    
    # Create embedder for text chunks
    chunk_embedder = TextChunkEmbedder(embedder)
    
    # Create lexical graph builder
    lexical_graph_builder = LexicalGraphBuilder()
    
    # Create Neo4j writer
    kg_writer = Neo4jWriter(driver)
    
    return {
        "driver": driver,
        "embedder": embedder,
        "llm": llm,
        "create_vector_index": create_vector_index,
        "upsert_vectors": upsert_vectors,
        "VectorRetriever": VectorRetriever,
        "VectorCypherRetriever": VectorCypherRetriever,
        "HybridRetriever": HybridRetriever,
        "HybridCypherRetriever": HybridCypherRetriever,
        "Text2CypherRetriever": Text2CypherRetriever,
        "EntityType": EntityType,
        "text_splitter": text_splitter,
        "chunk_embedder": chunk_embedder,
        "lexical_graph_builder": lexical_graph_builder,
        "kg_writer": kg_writer,
        "SchemaEntity": SchemaEntity,
        "SchemaRelation": SchemaRelation,
        "SchemaBuilder": SchemaBuilder,
        "LLMEntityRelationExtractor": LLMEntityRelationExtractor,
        "SimpleKGPipeline": SimpleKGPipeline,
        "Pipeline": Pipeline
    }

def create_rag_vector_index(index_name, label="Document", embedding_property="embedding", dimensions=1536):
    """Create a vector index for RAG."""
    components = initialize_rag_components()
    
    try:
        components["create_vector_index"](
            components["driver"],
            index_name,
            label=label,
            embedding_property=embedding_property,
            dimensions=dimensions,
            similarity_fn="cosine"
        )
        return f"Vector index '{index_name}' created successfully"
    except Exception as e:
        raise Exception(f"Error creating vector index: {str(e)}")

def ingest_document(index_name, text, metadata=None, chunk_size=1000, chunk_overlap=200):
    """Ingest a document into the vector store.
    
    This function uses the Neo4j GraphRAG API to:
    1. Split the text into chunks
    2. Generate embeddings for each chunk
    3. Store the chunks and embeddings in Neo4j
    4. Create a lexical graph structure connecting the chunks
    
    Args:
        index_name (str): Name of the vector index to use
        text (str): Text content to ingest
        metadata (dict, optional): Metadata to attach to the document
        chunk_size (int, optional): Size of text chunks. Defaults to 1000.
        chunk_overlap (int, optional): Overlap between chunks. Defaults to 200.
        
    Returns:
        str: Success message with number of chunks ingested
    """
    # Initialize components
    components = initialize_rag_components()
    driver = components["driver"]
    embedder = components["embedder"]
    
    try:
        # Create a pipeline for document ingestion
        pipeline = components["Pipeline"]()
        
        # Configure text splitter
        text_splitter = components["text_splitter"]
        pipeline.add_component(text_splitter, "text_splitter")
        
        # Configure chunk embedder
        chunk_embedder = components["chunk_embedder"]
        pipeline.add_component(chunk_embedder, "chunk_embedder")
        
        # Configure lexical graph builder
        lexical_graph_builder = components["lexical_graph_builder"]
        pipeline.add_component(lexical_graph_builder, "lexical_graph_builder")
        
        # Configure Neo4j writer
        kg_writer = components["kg_writer"]
        pipeline.add_component(kg_writer, "kg_writer")
        
        # Connect the components
        pipeline.connect("text_splitter", "chunk_embedder")
        pipeline.connect("chunk_embedder", "lexical_graph_builder")
        pipeline.connect("lexical_graph_builder", "kg_writer")
        
        # Prepare document info
        import uuid
        doc_id = str(uuid.uuid4())
        doc_metadata = metadata or {}
        doc_metadata["id"] = doc_id
        doc_metadata["index_name"] = index_name
        
        # Create document info
        from neo4j_graphrag.experimental.types import DocumentInfo
        document_info = DocumentInfo(id=doc_id, metadata=doc_metadata)
        
        # Run the pipeline
        import asyncio
        result = asyncio.run(pipeline.run({
            "text_splitter": text,
            "lexical_graph_builder": {"document_info": document_info}
        }))
        
        # Get the number of chunks created
        graph_result = result.get("lexical_graph_builder")
        num_chunks = len([node for node in graph_result.nodes if "Chunk" in node.labels])
        
        # Create vector index if it doesn't exist
        try:
            components["create_vector_index"](
                driver,
                index_name,
                label="Chunk",
                embedding_property="embedding",
                dimensions=len(result.get("chunk_embedder")[0].embedding) if result.get("chunk_embedder") else 1536,
                similarity_fn="cosine"
            )
        except Exception as e:
            # Index might already exist, which is fine
            print(f"Note: {str(e)}")
        
        return f"Document ingested successfully with {num_chunks} chunks"
    except Exception as e:
        raise Exception(f"Error ingesting document: {str(e)}")

def rag_query(index_name, query_text, top_k=5):
    """Query the RAG system with a question.
    
    This function uses the Neo4j GraphRAG API to:
    1. Generate an embedding for the query
    2. Retrieve relevant chunks from the vector index
    3. Generate a response using the LLM
    
    Args:
        index_name (str): Name of the vector index to query
        query_text (str): Question to ask
        top_k (int, optional): Number of results to retrieve. Defaults to 5.
        
    Returns:
        dict: Dictionary containing the answer and retrieved context
    """
    # Initialize components
    components = initialize_rag_components()
    driver = components["driver"]
    embedder = components["embedder"]
    llm = components["llm"]
    
    try:
        # Create a hybrid retriever (combines vector search with lexical graph traversal)
        retriever = components["HybridRetriever"](
            driver=driver,
            embedder=embedder,
            index_name=index_name,
            node_label="Chunk",  # Use Chunk nodes from our enhanced ingest pipeline
            embedding_property="embedding",
            text_property="text",
            top_k=top_k
        )
        
        # Retrieve relevant chunks
        results = retriever.retrieve(query_text)
        
        if not results:
            return {
                "answer": "I couldn't find any relevant information to answer your question.",
                "context": []
            }
        
        # Extract text from results
        context_texts = [result.text for result in results]
        
        # Format context for the LLM
        formatted_context = "\n\n".join([f"Context {i+1}:\n{text}" for i, text in enumerate(context_texts)])
        
        # Create prompt for the LLM
        prompt = f"""
You are an AI assistant that answers questions based on the provided context.
If you don't know the answer based on the context, say "I don't have enough information to answer this question."
Do not make up information that is not in the context.

Context:
{formatted_context}

Question: {query_text}

Answer:
"""
        
        # Generate answer using the LLM
        answer = llm.generate(prompt)
        
        # Return answer and context
        return {
            "answer": answer,
            "context": [{"text": result.text, "score": result.score} for result in results]
        }
    except Exception as e:
        raise Exception(f"Error querying RAG system: {str(e)}")

def build_knowledge_graph(text, entities=None, relations=None):
    """Build a knowledge graph from text using the Neo4j GraphRAG pipeline.
    
    This function uses the Neo4j GraphRAG API to:
    1. Extract entities and relations from text using LLM
    2. Create a schema for the knowledge graph
    3. Build and persist the knowledge graph in Neo4j
    
    Args:
        text (str): Text content to process
        entities (list, optional): List of entity types to extract. Defaults to None.
        relations (list, optional): List of relation types to extract. Defaults to None.
        
    Returns:
        dict: Dictionary containing the extracted entities and relations
    """
    # Initialize components
    components = initialize_rag_components()
    driver = components["driver"]
    llm = components["llm"]
    
    try:
        # Set default entity and relation types if not provided
        if not entities:
            entities = ["Person", "Organization", "Location", "Date", "Technology", "Product"]
        
        if not relations:
            relations = ["WORKS_FOR", "LOCATED_IN", "CREATED_BY", "USES", "RELATED_TO"]
        
        # Create schema entities and relations
        schema_entities = [components["SchemaEntity"](name=entity) for entity in entities]
        schema_relations = [components["SchemaRelation"](name=relation) for relation in relations]
        
        # Create schema builder
        schema_builder = components["SchemaBuilder"](entities=schema_entities, relations=schema_relations)
        
        # Create entity relation extractor
        extractor = components["LLMEntityRelationExtractor"](llm=llm, schema_builder=schema_builder)
        
        # Create Neo4j writer
        kg_writer = components["kg_writer"]
        
        # Create knowledge graph pipeline
        kg_pipeline = components["SimpleKGPipeline"](
            entity_relation_extractor=extractor,
            kg_writer=kg_writer
        )
        
        # Run the pipeline
        import asyncio
        result = asyncio.run(kg_pipeline.run(text))
        
        # Extract entities and relations from result
        extracted_entities = []
        for entity in result.entities:
            extracted_entities.append({
                "type": entity.type,
                "text": entity.text,
                "id": entity.id
            })
        
        extracted_relations = []
        for relation in result.relations:
            extracted_relations.append({
                "type": relation.type,
                "source": relation.source.text,
                "source_type": relation.source.type,
                "target": relation.target.text,
                "target_type": relation.target.type
            })
        
        return {
            "entities": extracted_entities,
            "relations": extracted_relations,
            "message": f"Knowledge graph created with {len(extracted_entities)} entities and {len(extracted_relations)} relations"
        }
    except Exception as e:
        raise Exception(f"Error building knowledge graph: {str(e)}")
