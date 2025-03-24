#!/usr/bin/env python3
"""
GitHub commands for TPM-CLI.
"""

import os
import sys
import json
from utils import github_utils
from datetime import datetime
from tabulate import tabulate

def cmd_repo(args):
    """Find repositories or get repository information."""
    try:
        # Add debug information
        print(f"Debug: Command arguments: {args}")
        
        # Get GitHub token
        token = github_utils.get_github_token()
        if not token:
            print("GitHub token not found. Please set up your GitHub token.")
            sys.exit(1)
        
        print(f"Debug: Using token: {token[:5]}...{token[-5:]} (length: {len(token)})")
        
        # Default to 'codeium' org if not specified
        org = args.org if args.org else "codeium"
        print(f"Debug: Using organization: {org}")
        
        # Check if query is None and provide a default
        if not hasattr(args, 'query') or args.query is None:
            print("Error: No repository query specified.")
            print("Usage: ./tpm repo <repository_name> [--org <organization>]")
            sys.exit(1)
        
        print(f"Debug: Using query: {args.query}")
        
        # Search for repositories
        match_type = "exact" if args.query.count("/") == 0 and " " not in args.query else "contains"
        max_pages = args.max_pages if hasattr(args, 'limit_pages') and args.limit_pages else None
        
        print(f"Debug: Searching for repositories with match_type: {match_type}, max_pages: {max_pages}")
        
        try:
            repos = github_utils.search_repos(
                args.query, 
                org=org, 
                token=token, 
                max_pages=max_pages,
                match_type=match_type
            )
        except Exception as e:
            print(f"Error searching for repositories: {str(e)}")
            # Try direct repository access as a fallback
            print(f"Debug: Attempting direct repository access for {org}/{args.query}")
            try:
                # Direct API call to get the repository
                import requests
                headers = {
                    "Authorization": f"token {token}",
                    "Accept": "application/vnd.github.v3+json"
                }
                repo_url = f"https://api.github.com/repos/{org}/{args.query}"
                response = requests.get(repo_url, headers=headers)
                
                if response.status_code == 200:
                    repo_data = response.json()
                    repos = [repo_data]
                    print(f"Debug: Successfully accessed repository directly: {repo_data['full_name']}")
                else:
                    print(f"Error accessing repository directly: {response.status_code} - {response.text}")
                    repos = []
            except Exception as direct_error:
                print(f"Error in direct repository access: {str(direct_error)}")
                repos = []
        
        print(f"Debug: Found {len(repos)} repositories")
        
        if not repos:
            print(f"No repositories found matching '{args.query}' in {org}.")
            sys.exit(0)
        
        # If only one repo is found or details are requested, get additional details
        if len(repos) == 1 or (hasattr(args, 'details') and args.details):
            detailed_results = []
            
            for repo in repos:
                print(f"Debug: Getting details for repository: {repo.get('name', 'unknown')}")
                try:
                    details = github_utils.get_repo_details(repo, org, token)
                    detailed_repo = details["repo"]
                    contributors = details["contributors"]
                    languages = details["languages"]
                    
                    # Calculate language percentages
                    total_bytes = sum(languages.values())
                    language_percentages = {}
                    if total_bytes > 0:
                        for lang, bytes_count in languages.items():
                            language_percentages[lang] = round((bytes_count / total_bytes) * 100, 2)
                    
                    # Format top contributors
                    top_contributors = []
                    for contributor in contributors[:5]:  # Show top 5 contributors
                        top_contributors.append(f"{contributor['login']} ({contributor['contributions']})")
                    
                    detailed_results.append({
                        "name": detailed_repo["name"],
                        "url": detailed_repo["html_url"],
                        "description": detailed_repo["description"] or "No description",
                        "created_at": github_utils.format_date(detailed_repo.get("created_at")),
                        "updated_at": github_utils.format_date(detailed_repo.get("updated_at")),
                        "pushed_at": github_utils.format_date(detailed_repo.get("pushed_at")),
                        "stars": detailed_repo.get("stargazers_count", 0),
                        "forks": detailed_repo.get("forks_count", 0),
                        "open_issues": detailed_repo.get("open_issues_count", 0),
                        "language": detailed_repo.get("language", "None"),
                        "languages": language_percentages,
                        "contributors": top_contributors,
                        "size": detailed_repo.get("size", 0),
                        "default_branch": detailed_repo.get("default_branch", "main"),
                        "license": detailed_repo.get("license", {}).get("name", "None"),
                        "classification": github_utils.classify_repository(detailed_repo)
                    })
                except Exception as detail_error:
                    print(f"Error getting details for repository {repo.get('name', 'unknown')}: {str(detail_error)}")
                    # Create a simplified result with available information
                    detailed_results.append({
                        "name": repo.get("name", "Unknown"),
                        "url": repo.get("html_url", "N/A"),
                        "description": repo.get("description", "No description"),
                        "created_at": github_utils.format_date(repo.get("created_at", "")),
                        "updated_at": github_utils.format_date(repo.get("updated_at", "")),
                        "pushed_at": github_utils.format_date(repo.get("pushed_at", "")),
                        "stars": repo.get("stargazers_count", 0),
                        "forks": repo.get("forks_count", 0),
                        "open_issues": repo.get("open_issues_count", 0),
                        "language": repo.get("language", "None"),
                        "languages": {},
                        "contributors": [],
                        "size": repo.get("size", 0),
                        "default_branch": repo.get("default_branch", "main"),
                        "license": "None",
                        "classification": {
                            "type": "Unknown",
                            "activity": "Unknown",
                            "importance": "Unknown"
                        }
                    })
            
            # Output detailed results
            if hasattr(args, 'output') and args.output:
                with open(args.output, 'w') as f:
                    f.write("# Repository Details\n\n")
                    
                    for result in detailed_results:
                        f.write(f"## {result['name']}\n\n")
                        f.write(f"**URL:** {result['url']}  \n")
                        f.write(f"**Description:** {result['description']}  \n")
                        f.write(f"**Created:** {result['created_at']}  \n")
                        f.write(f"**Last Updated:** {result['updated_at']}  \n")
                        f.write(f"**Last Push:** {result['pushed_at']}  \n")
                        f.write(f"**Stars:** {result['stars']}  \n")
                        f.write(f"**Forks:** {result['forks']}  \n")
                        f.write(f"**Open Issues:** {result['open_issues']}  \n")
                        f.write(f"**Primary Language:** {result['language']}  \n")
                        f.write(f"**Size:** {result['size']} KB  \n")
                        f.write(f"**Default Branch:** {result['default_branch']}  \n")
                        f.write(f"**License:** {result['license']}  \n")
                        f.write(f"**Type:** {result['classification'].get('type', 'Unknown')}  \n")
                        f.write(f"**Activity:** {result['classification'].get('activity', 'Unknown')}  \n")
                        f.write(f"**Importance:** {result['classification'].get('importance', 'Unknown')}  \n\n")
                        
                        # Languages
                        f.write("### Languages\n\n")
                        for lang, percentage in result['languages'].items():
                            f.write(f"- {lang}: {percentage}%  \n")
                        f.write("\n")
                        
                        # Contributors
                        f.write("### Top Contributors\n\n")
                        for contributor in result['contributors']:
                            f.write(f"- {contributor}  \n")
                        f.write("\n")
                
                print(f"Detailed results saved to {args.output}")
            else:
                for result in detailed_results:
                    print(f"\n{'-' * 80}")
                    print(f"Repository: {result['name']}")
                    print(f"URL: {result['url']}")
                    print(f"Description: {result['description']}")
                    print(f"Created: {result['created_at']}")
                    print(f"Last Updated: {result['updated_at']}")
                    print(f"Last Push: {result['pushed_at']}")
                    print(f"Stars: {result['stars']}")
                    print(f"Forks: {result['forks']}")
                    print(f"Open Issues: {result['open_issues']}")
                    print(f"Primary Language: {result['language']}")
                    print(f"Size: {result['size']} KB")
                    print(f"Default Branch: {result['default_branch']}")
                    print(f"License: {result['license']}")
                    print(f"Type: {result['classification'].get('type', 'Unknown')}")
                    print(f"Activity: {result['classification'].get('activity', 'Unknown')}")
                    print(f"Importance: {result['classification'].get('importance', 'Unknown')}")
                    
                    print("\nLanguages:")
                    for lang, percentage in result['languages'].items():
                        print(f"- {lang}: {percentage}%")
                    
                    print("\nTop Contributors:")
                    for contributor in result['contributors']:
                        print(f"- {contributor}")
                    
                    print(f"{'-' * 80}")
        else:
            # Apply filters if specified
            filtered_repos = repos
            
            if hasattr(args, 'type') and args.type:
                filtered_repos = [repo for repo in filtered_repos if github_utils.classify_repository(repo)["type"] == args.type]
            
            if hasattr(args, 'activity') and args.activity:
                filtered_repos = [repo for repo in filtered_repos if github_utils.classify_repository(repo)["activity"] == args.activity]
            
            if hasattr(args, 'importance') and args.importance:
                filtered_repos = [repo for repo in filtered_repos if github_utils.classify_repository(repo)["importance"] == args.importance]
            
            # Prepare table data
            table_data = []
            for repo in filtered_repos:
                try:
                    classification = github_utils.classify_repository(repo)
                    table_data.append([
                        repo["name"],
                        repo.get("description", "")[:50] + ("..." if repo.get("description", "") and len(repo.get("description", "")) > 50 else ""),
                        repo.get("language", ""),
                        repo.get("stargazers_count", 0),
                        repo.get("forks_count", 0),
                        github_utils.format_date(repo.get("pushed_at", "")),
                        classification.get("type", "Unknown"),
                        classification.get("activity", "Unknown"),
                        classification.get("importance", "Unknown")
                    ])
                except Exception as class_error:
                    print(f"Error classifying repository {repo.get('name', 'unknown')}: {str(class_error)}")
                    table_data.append([
                        repo.get("name", "Unknown"),
                        repo.get("description", "")[:50] + ("..." if repo.get("description", "") and len(repo.get("description", "")) > 50 else ""),
                        repo.get("language", ""),
                        repo.get("stargazers_count", 0),
                        repo.get("forks_count", 0),
                        github_utils.format_date(repo.get("pushed_at", "")),
                        "Unknown",
                        "Unknown",
                        "Unknown"
                    ])
            
            # Sort by name
            table_data.sort(key=lambda x: x[0])
            
            # Output table
            headers = ["Name", "Description", "Language", "Stars", "Forks", "Last Push", "Type", "Activity", "Importance"]
            table = tabulate(table_data, headers=headers, tablefmt="grid")
            
            if hasattr(args, 'output') and args.output:
                with open(args.output, 'w') as f:
                    f.write(f"# Repositories matching '{args.query}' in {org}\n\n")
                    f.write("| " + " | ".join(headers) + " |\n")
                    f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
                    
                    for row in table_data:
                        f.write("| " + " | ".join(str(cell) for cell in row) + " |\n")
                
                print(f"Results saved to {args.output}")
            else:
                print(f"\nFound {len(filtered_repos)} repositories matching '{args.query}' in {org}:")
                print(table)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(f"Debug: Full traceback:\n{traceback.format_exc()}")
        sys.exit(1)
