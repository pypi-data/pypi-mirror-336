#!/usr/bin/env python3
"""
Test GitHub API access directly using the token.
"""

import requests
import json
import sys

# Use the token directly
TOKEN = "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"
ORG = "trilogy-group"
REPO = "central-product-tpm"

def test_repo_access():
    """Test access to the repository."""
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Test 1: Access the repository
    print("1. Accessing the repository:")
    url = f"https://api.github.com/repos/{ORG}/{REPO}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repo_data = response.json()
        print(f"  ✅ Successfully accessed repository: {repo_data['full_name']}")
        print(f"  Description: {repo_data['description']}")
        print(f"  Private: {repo_data['private']}")
        print(f"  Language: {repo_data['language']}")
    else:
        print(f"  ❌ Failed to access repository: {response.status_code} - {response.text}")
        return False
    
    # Test 2: Access the tech-interview-automation directory
    print("\n2. Accessing the tech-interview-automation directory:")
    url = f"https://api.github.com/repos/{ORG}/{REPO}/contents/POC/tech-interview-automation"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        contents = response.json()
        print(f"  ✅ Successfully accessed directory with {len(contents)} items:")
        for item in contents:
            print(f"  - {item['name']} ({item['type']})")
    else:
        print(f"  ❌ Failed to access directory: {response.status_code} - {response.text}")
        return False
    
    # Test 3: Access the README.md file
    print("\n3. Accessing the README.md file:")
    url = f"https://api.github.com/repos/{ORG}/{REPO}/contents/POC/tech-interview-automation/README.md"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_data = response.json()
        print(f"  ✅ Successfully accessed file: {file_data['name']}")
        print(f"  Size: {file_data['size']} bytes")
        print(f"  URL: {file_data['html_url']}")
    else:
        print(f"  ❌ Failed to access file: {response.status_code} - {response.text}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing GitHub API access using the token\n")
    success = test_repo_access()
    
    if success:
        print("\n✅ All tests passed! You have the correct permissions to access the repository.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the token permissions.")
        sys.exit(1)
