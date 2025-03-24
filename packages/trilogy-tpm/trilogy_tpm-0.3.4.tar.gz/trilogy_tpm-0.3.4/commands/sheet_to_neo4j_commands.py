#!/usr/bin/env python3
"""
Commands for importing Google Sheets data into Neo4j.
"""

import os
import sys
import json
from utils.project_utils import (
    get_current_project,
    get_project_neo4j_credentials,
)
from utils.google_utils import get_document, get_credentials, SCOPES
from utils.neo4j_utils import (
    create_neo4j_driver,
    execute_cypher_query,
    format_cypher_results,
)

def cmd_sheet_to_neo4j(args):
    """
    Command handler for the sheet-to-neo4j command.
    
    Args:
        args: Command line arguments
    """
    # Get the current project
    current_project = get_current_project()
    if current_project:
        print(f"Using project: {current_project}")
    
    # Process the sheet
    result = process_sheet_tabs(
        args.sheet_id,
        args.index_name,
        args.model,
        args.dry_run
    )
    
    # If successful and we have a current project, add the sheet to the project
    if result and current_project:
        # Get sheet metadata to use as document name
        try:
            # Build the service
            credentials = get_credentials()
            service = build('sheets', 'v4', credentials=credentials)
            
            # Get spreadsheet metadata
            spreadsheet = service.spreadsheets().get(spreadsheetId=args.sheet_id).execute()
            sheet_title = spreadsheet.get('properties', {}).get('title', f"Sheet {args.sheet_id}")
            
            # Add document to project
            add_document_to_project(
                current_project,
                args.sheet_id,
                'google_sheet',
                sheet_title
            )
            print(f"Added sheet '{sheet_title}' to project: {current_project}")
        except Exception as e:
            print(f"Warning: Could not add sheet to project: {str(e)}")

def process_sheet_tabs(sheet_id, index_name=None, model=None, dry_run=False):
    """
    Process each tab in the Google Sheet and load into Neo4j.
    
    Args:
        sheet_id (str): Google Sheet ID
        index_name (str, optional): Neo4j index name
        model (str, optional): Neo4j model name
        dry_run (bool, optional): If True, process without connecting to Neo4j
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get credentials and build the Drive API client
        credentials = get_credentials()
        
        if not credentials:
            print("Google credentials not configured. Please run 'tpm config google' first.")
            return False
        
        # Build the service
        service = build('sheets', 'v4', credentials=credentials)
        
        # Get spreadsheet metadata
        print(f"Fetching Google Sheet: {sheet_id}")
        spreadsheet = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        title = spreadsheet.get('properties', {}).get('title', 'Untitled')
        sheets = spreadsheet.get('sheets', [])
        
        print(f"Processing Google Sheet: {title}")
        print(f"Found {len(sheets)} tabs")
        
        # Check if we need to connect to Neo4j
        driver = None
        if not dry_run:
            try:
                # Try to create Neo4j driver
                print("Using Neo4j credentials from project:", get_current_project())
                driver = create_neo4j_driver()
                if not driver:
                    print("Failed to connect to Neo4j. Check your credentials.")
                    print("Switching to dry-run mode.")
                    dry_run = True
            except Exception as e:
                print(f"Neo4j connection error: {str(e)}")
                print("Switching to dry-run mode.")
                dry_run = True
        
        # Process each tab
        for sheet in sheets:
            sheet_props = sheet.get('properties', {})
            sheet_name = sheet_props.get('title', '')
            sheet_id_in_doc = sheet_props.get('sheetId', '')
            
            # Check if we should process this tab
            if sheet_name != "Class Data":
                print(f"Skipping tab: {sheet_name} (not Class Data)")
                continue
            
            print(f"\nProcessing tab: {sheet_name}")
            
            # Get the data for this tab
            result = service.spreadsheets().values().get(
                spreadsheetId=sheet_id,
                range=sheet_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                print(f"No data found in tab: {sheet_name}")
                continue
            
            # Create a DataFrame from the rows
            try:
                # Get headers from the first row
                headers = values[0]
                
                # Check if we have data rows
                if len(values) < 2:
                    print(f"No data rows found in tab: {sheet_name}")
                    continue
                
                # Create DataFrame with flexible column handling
                data_rows = []
                for row in values[1:]:  # Skip header row
                    # Pad row if it's shorter than headers
                    if len(row) < len(headers):
                        row = row + [''] * (len(headers) - len(row))
                    # Truncate row if it's longer than headers
                    elif len(row) > len(headers):
                        row = row[:len(headers)]
                    data_rows.append(row)
                
                df = pd.DataFrame(data_rows, columns=headers)
                
                # Display DataFrame info
                print(f"DataFrame shape: {df.shape}")
                print(f"Columns: {', '.join(df.columns.tolist())}")
                
                # Display sample data
                print("\nSample data:")
                print(df.head(5).to_string())
                
                # Process data based on the tab name
                if not dry_run and driver:
                    # Use a generic processing function for any tab
                    process_generic_tab(driver, df, f"{index_name or 'kayako'}_{sheet_name.lower().replace(' ', '_')}")
                
            except Exception as e:
                print(f"Error processing tab {sheet_name}: {str(e)}")
        
        # Close Neo4j driver if created
        if driver:
            driver.close()
        
        print("\nProcessing completed successfully.")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def process_generic_tab(driver, df, index_name):
    """
    Process a generic tab from the Google Sheet and load into Neo4j.
    
    Args:
        driver: Neo4j driver
        df: DataFrame with the tab data
        index_name: Name for the Neo4j index
    """
    print(f"Processing generic tab data into Neo4j index: {index_name}")
    
    # Create constraints if they don't exist
    try:
        with driver.session() as session:
            # Create constraint on Document nodes
            session.run("""
                CREATE CONSTRAINT document_id IF NOT EXISTS
                FOR (d:Document) REQUIRE d.id IS UNIQUE
            """)
            print("Created constraint for Document nodes")
            
            # Create constraint on Row nodes
            session.run(f"""
                CREATE CONSTRAINT {index_name}_row_id IF NOT EXISTS
                FOR (r:{index_name}) REQUIRE r.id IS UNIQUE
            """)
            print(f"Created constraint for {index_name} nodes")
    except Exception as e:
        print(f"Warning: Could not create constraints: {str(e)}")
    
    # Process each row as a node
    with driver.session() as session:
        # First, create the Document node for the tab
        doc_query = """
        MERGE (d:Document {id: $id})
        SET d.title = $title,
            d.type = $type,
            d.updated = timestamp()
        RETURN d
        """
        session.run(doc_query, {
            'id': index_name,
            'title': index_name,
            'type': 'sheet_tab'
        })
        print(f"Created Document node for {index_name}")
        
        # Process each row
        for i, row in df.iterrows():
            # Create a unique ID for this row
            row_id = f"{index_name}_row_{i}"
            
            # Create properties from all columns
            properties = {'id': row_id}
            for col in df.columns:
                # Clean column name for Neo4j
                clean_col = col.lower().replace(' ', '_').replace('-', '_')
                val = row[col]
                
                # Skip empty values
                if pd.isna(val) or val == '':
                    continue
                
                # Convert to appropriate type
                if isinstance(val, (int, float)):
                    properties[clean_col] = val
                else:
                    properties[clean_col] = str(val)
            
            # Create the row node
            row_query = f"""
            MERGE (r:{index_name} {{id: $id}})
            SET r += $properties
            WITH r
            MATCH (d:Document {{id: $doc_id}})
            MERGE (d)-[:CONTAINS]->(r)
            RETURN r
            """
            
            session.run(row_query, {
                'id': row_id,
                'properties': properties,
                'doc_id': index_name
            })
            
        print(f"Imported {len(df)} rows into Neo4j")

def process_sheet_for_rag(sheet_content, index_name):
    """
    Process the sheet content for RAG.
    """
    try:
        # Check if Neo4j is configured
        neo4j_creds = get_project_neo4j_credentials()
        if not neo4j_creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            sys.exit(1)
        
        # Create Neo4j driver
        driver = create_neo4j_driver()
        
        # Create RAG vector index if it doesn't exist
        execute_cypher_query(driver, f"CALL gds.graph.create('{index_name}', ['Document'], ['CONTAINS'])")
        
        # Ingest the document
        execute_cypher_query(driver, f"MATCH (d:Document {{id: '{index_name}'}}) SET d.rag_vector = apoc.convert.fromJsonMap({sheet_content})")
        
        print(f"Sheet content ingested into RAG index: {index_name}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def process_sheet_for_graph(sheet_content, model=None):
    """
    Process the sheet content for graph database.
    """
    try:
        # Check if Neo4j is configured
        neo4j_creds = get_project_neo4j_credentials()
        if not neo4j_creds:
            print("Neo4j credentials not configured. Please run 'tpm config neo4j' first.")
            sys.exit(1)
        
        # Create Neo4j driver
        driver = create_neo4j_driver()
        
        # Convert markdown to DataFrame
        df = pd.read_csv(io.StringIO(sheet_content), sep='|')
        
        # Process the data based on the model
        if model:
            process_sheet_data(model, df)
        else:
            # Try to infer the model from the data
            if 'customer' in df.columns or 'customer_id' in df.columns:
                process_sheet_data('customer', df)
            elif 'organization' in df.columns or 'org_id' in df.columns:
                process_sheet_data('organization', df)
            elif 'product' in df.columns:
                process_sheet_data('product', df)
            elif 'user' in df.columns or 'user_id' in df.columns:
                process_sheet_data('user', df)
            else:
                print("Could not infer model from data. Please specify a model.")
                sys.exit(1)
        
        print("Sheet content processed for graph database")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def process_sheet_data(model, df, index_name=None, dry_run=False):
    """
    Process the sheet data based on the model.
    """
    # Create Neo4j driver
    if not dry_run:
        driver = create_neo4j_driver()
    
    # Convert model to lowercase
    model = model.lower()
    
    print(f"Processing data as model: {model}")
    
    # Process based on model type
    if model == 'customer':
        process_customers_tab(driver, df) if not dry_run else print("Dry run: Skipping customer data processing")
    elif model == 'organization' or model == 'organizations':
        process_organizations_tab(driver, df) if not dry_run else print("Dry run: Skipping organization data processing")
    elif model == 'product' or model == 'products':
        process_products_tab(driver, df) if not dry_run else print("Dry run: Skipping product data processing")
    elif model == 'slot' or model == 'slots':
        process_slots_tab(driver, df) if not dry_run else print("Dry run: Skipping slot data processing")
    elif model == 'user' or model == 'users':
        process_users_tab(driver, df) if not dry_run else print("Dry run: Skipping user data processing")
    else:
        # Generic processing
        process_generic_tab(driver, model, df) if not dry_run else print(f"Dry run: Skipping generic {model} data processing")

def process_customers_tab(driver, df):
    """
    Process Customers tab data.
    """
    print("Processing customers data...")
    
    # Clean column names
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    
    # Create Customer nodes
    with driver.session() as session:
        for _, row in df.iterrows():
            # Extract customer data
            customer_id = str(row.get('id', row.get('customer_id', '')))
            customer_name = str(row.get('name', row.get('customer_name', '')))
            
            if not customer_id or not customer_name:
                continue
            
            # Prepare properties
            properties = {'id': customer_id, 'name': customer_name}
            for col in df.columns:
                if pd.notna(row.get(col)) and row.get(col) != '':
                    properties[col] = str(row.get(col))
            
            # Create Customer node
            query = """
            MERGE (c:Customer {id: $id})
            SET c.name = $name
            """
            
            # Add dynamic properties
            for prop, value in properties.items():
                if prop not in ['id', 'name']:
                    query += f"SET c.{prop} = ${prop}\n"
            
            execute_cypher_query(driver, query, **properties)
            
            print(f"Created/Updated Customer: {customer_name} (ID: {customer_id})")

def process_organizations_tab(driver, df):
    """
    Process Organizations tab data.
    """
    print("Processing organizations data...")
    
    # Clean column names
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    
    # Create Organization nodes and link to Customers
    with driver.session() as session:
        for _, row in df.iterrows():
            # Extract organization data
            org_id = str(row.get('id', row.get('org_id', ''))) or str(row.get('organization_id', ''))
            org_name = str(row.get('name', row.get('org_name', ''))) or str(row.get('organization_name', ''))
            customer_id = str(row.get('customer_id', ''))
            
            if not org_id or not org_name:
                continue
            
            # Prepare properties
            properties = {'id': org_id, 'name': org_name}
            for col in df.columns:
                if pd.notna(row.get(col)) and row.get(col) != '':
                    properties[col] = str(row.get(col))
            
            # Create Organization node
            query = """
            MERGE (o:Organization {id: $id})
            SET o.name = $name
            """
            
            # Add dynamic properties
            for prop, value in properties.items():
                if prop not in ['id', 'name', 'customer_id']:
                    query += f"SET o.{prop} = ${prop}\n"
            
            # Link to Customer if customer_id is provided
            if customer_id:
                query += """
                WITH o
                MATCH (c:Customer {id: $customer_id})
                MERGE (c)-[:HAS_ORGANIZATION]->(o)
                """
                properties['customer_id'] = customer_id
            
            execute_cypher_query(driver, query, **properties)
            
            print(f"Created/Updated Organization: {org_name} (ID: {org_id})")

def process_products_tab(driver, df):
    """
    Process Products tab data.
    """
    print("Processing products data...")
    
    # Clean column names
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    
    # Create Product nodes
    with driver.session() as session:
        for _, row in df.iterrows():
            # Extract product data
            product_id = str(row.get('id', row.get('product_id', '')))
            product_name = str(row.get('name', row.get('product_name', '')))
            
            if not product_id and not product_name:
                continue
            
            # If no ID but has name, use name as ID
            if not product_id:
                product_id = product_name.lower().replace(' ', '_')
            
            # Prepare properties
            properties = {'id': product_id, 'name': product_name}
            for col in df.columns:
                if pd.notna(row.get(col)) and row.get(col) != '':
                    properties[col] = str(row.get(col))
            
            # Create Product node
            query = """
            MERGE (p:Product {id: $id})
            SET p.name = $name
            """
            
            # Add dynamic properties
            for prop, value in properties.items():
                if prop not in ['id', 'name']:
                    query += f"SET p.{prop} = ${prop}\n"
            
            execute_cypher_query(driver, query, **properties)
            
            print(f"Created/Updated Product: {product_name} (ID: {product_id})")

def process_slots_tab(driver, df):
    """
    Process Slots tab data.
    """
    print("Processing slots data...")
    
    # Clean column names
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    
    # Create Slot nodes
    with driver.session() as session:
        for _, row in df.iterrows():
            # Extract slot data
            slot_id = str(row.get('id', row.get('slot_id', ''))) or str(row.get('slot', ''))
            if not slot_id:
                slot_id = f"slot_{_}"  # Use row index if no ID
            slot_name = str(row.get('name', row.get('slot_name', '')))
            product = str(row.get('product', ''))
            objective = str(row.get('objective', ''))
            status = str(row.get('status', ''))
            
            # Prepare properties
            properties = {
                'id': slot_id,
                'name': slot_name if slot_name else slot_id
            }
            
            if objective:
                properties['objective'] = objective
            
            if status:
                properties['status'] = status
            
            # Add other properties
            for col in df.columns:
                if col not in ['id', 'name', 'product', 'objective', 'status'] and pd.notna(row.get(col)) and row.get(col) != '':
                    properties[col] = str(row.get(col))
            
            # Create Slot node
            query = """
            MERGE (s:Slot {id: $id})
            SET s.name = $name
            """
            
            # Add dynamic properties
            for prop, value in properties.items():
                if prop not in ['id', 'name']:
                    query += f"SET s.{prop} = ${prop}\n"
            
            # Link to Product if product is provided
            if product:
                query += """
                WITH s
                MERGE (p:Product {name: $product})
                MERGE (p)-[:HAS_SLOT]->(s)
                """
                properties['product'] = product
            
            execute_cypher_query(driver, query, **properties)
            
            print(f"Created/Updated Slot: {slot_name if slot_name else slot_id}")

def process_users_tab(driver, df):
    """
    Process Users tab data.
    """
    print("Processing users data...")
    
    # Clean column names
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    
    # Create User nodes and link to Organizations
    with driver.session() as session:
        for _, row in df.iterrows():
            # Extract user data
            user_id = str(row.get('id', row.get('user_id', ''))) or str(row.get('email', ''))
            user_name = str(row.get('name', row.get('user_name', '')))
            email = str(row.get('email', ''))
            org_id = str(row.get('org_id', row.get('organization_id', '')))
            
            if not user_id:
                continue
            
            # Prepare properties
            properties = {'id': user_id}
            
            if user_name:
                properties['name'] = user_name
            
            if email:
                properties['email'] = email
            
            # Add other properties
            for col in df.columns:
                if col not in ['id', 'name', 'email', 'org_id', 'organization_id'] and pd.notna(row.get(col)) and row.get(col) != '':
                    properties[col] = str(row.get(col))
            
            # Create User node
            query = """
            MERGE (u:User {id: $id})
            """
            
            # Add dynamic properties
            for prop, value in properties.items():
                if prop != 'id':
                    query += f"SET u.{prop} = ${prop}\n"
            
            # Link to Organization if org_id is provided
            if org_id:
                query += """
                WITH u
                MATCH (o:Organization {id: $org_id})
                MERGE (o)-[:HAS_USER]->(u)
                """
                properties['org_id'] = org_id
            
            execute_cypher_query(driver, query, **properties)
            
            print(f"Created/Updated User: {user_name if user_name else user_id}")

def process_generic_tab(driver, model, df):
    """
    Process a generic tab data.
    """
    print(f"Processing generic {model} data...")
    
    # Clean column names
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    
    # Create nodes for the model
    with driver.session() as session:
        for _, row in df.iterrows():
            # Extract ID and name
            node_id = str(row.get('id', ''))
            node_name = str(row.get('name', ''))
            
            # If no ID but has name, use name as ID
            if not node_id and node_name:
                node_id = node_name.lower().replace(' ', '_')
            
            # If still no ID, use row index
            if not node_id:
                node_id = f"{model}_{_}"
            
            # Prepare properties
            properties = {'id': node_id}
            
            if node_name:
                properties['name'] = node_name
            
            # Add other properties
            for col in df.columns:
                if col not in ['id', 'name'] and pd.notna(row.get(col)) and row.get(col) != '':
                    properties[col] = str(row.get(col))
            
            # Create node
            query = f"""
            MERGE (n:{model.capitalize()} {{id: $id}})
            """
            
            # Add dynamic properties
            for prop, value in properties.items():
                if prop != 'id':
                    query += f"SET n.{prop} = ${prop}\n"
            
            execute_cypher_query(driver, query, **properties)
            
            print(f"Created/Updated {model.capitalize()}: {node_name if node_name else node_id}")
