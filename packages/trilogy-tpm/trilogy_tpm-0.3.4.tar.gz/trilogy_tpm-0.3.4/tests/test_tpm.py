#!/usr/bin/env python3
import unittest
import os
import sys
import subprocess
from unittest.mock import patch, MagicMock
import json
import tempfile

class TestTPMCLI(unittest.TestCase):
    
    def test_command_line_help(self):
        # Test that the CLI can be executed without errors
        try:
            result = subprocess.run(['python', 'tpm', '--help'], 
                                   check=True, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
            self.assertEqual(result.returncode, 0)
            output = result.stdout.decode('utf-8')
            self.assertIn('repo', output)  # Check that 'repo' command is mentioned
            
            # Check repo command help specifically
            result = subprocess.run(['python', 'tpm', 'repo', '--help'], 
                                   check=True, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
            self.assertEqual(result.returncode, 0)
            output = result.stdout.decode('utf-8')
            self.assertIn('--limit-pages', output)  # Check that pagination option is mentioned
            self.assertIn('--max-pages', output)  # Check that max pages option is mentioned
            self.assertIn('--details', output)  # Check that details option is mentioned
        except subprocess.CalledProcessError as e:
            self.fail(f"CLI execution failed: {e.stderr.decode('utf-8')}")
    
    def test_repo_command(self):
        # Test the repo command with a known repository
        try:
            result = subprocess.run(['python', 'tpm', 'repo', 'cloudfix-aws', '--org', 'trilogy-group'], 
                                   check=True, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
            self.assertEqual(result.returncode, 0)
            output = result.stdout.decode('utf-8')
            # Just check that the command ran without errors
            self.assertNotIn('Error:', output)
        except subprocess.CalledProcessError as e:
            self.fail(f"CLI execution failed: {e.stderr.decode('utf-8')}")
    
    def test_repo_pagination(self):
        # Test pagination with a limited number of pages
        try:
            result = subprocess.run(['python', 'tpm', 'repo', 'cloud', '--org', 'trilogy-group', '--limit-pages', '--max-pages', '1'], 
                                   check=True, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
            self.assertEqual(result.returncode, 0)
            output = result.stdout.decode('utf-8')
            # Just check that the command ran without errors
            self.assertNotIn('Error:', output)
        except subprocess.CalledProcessError as e:
            self.fail(f"CLI execution failed: {e.stderr.decode('utf-8')}")
    
    def test_jira_command(self):
        # Test the Jira command with a known issue
        try:
            result = subprocess.run(['python', 'tpm', 'jira', 'get', 'SAASOPS-31347'], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
            # We don't check the return code here because it might fail if credentials aren't set up
            output = result.stdout.decode('utf-8')
            error = result.stderr.decode('utf-8')
            # If we get an authentication error, that's expected without credentials
            # If we get the actual issue, that's also good
            self.assertTrue('SAASOPS-31347' in output or 'authentication' in error.lower() or 'credentials' in error.lower())
        except subprocess.CalledProcessError as e:
            # This is acceptable if credentials aren't set up
            pass
    
    def test_google_command(self):
        # Test the Google command with a known spreadsheet
        try:
            result = subprocess.run(['python', 'tpm', 'google', 'list', '--query', 'hPp8sXcwMJNeQcbc54k'], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
            # We don't check the return code here because it might fail if credentials aren't set up
            output = result.stdout.decode('utf-8')
            error = result.stderr.decode('utf-8')
            # If we get an authentication error, that's expected without credentials
            self.assertTrue('hPp8sXcwMJNeQcbc54k' in output or 'authentication' in error.lower() or 'credentials' in error.lower())
        except subprocess.CalledProcessError as e:
            # This is acceptable if credentials aren't set up
            pass
    
    def test_notion_command(self):
        # Test the Notion command
        try:
            result = subprocess.run(['python', 'tpm', 'notion', 'status'], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
            # We don't check the return code here because it might fail if credentials aren't set up
            output = result.stdout.decode('utf-8')
            error = result.stderr.decode('utf-8')
            
            # Print the output and error for debugging
            print(f"Notion test output: {output}")
            print(f"Notion test error: {error}")
            
            # Check for various expected outputs or errors
            self.assertTrue(
                'status' in output.lower() or 
                'token' in output.lower() or 
                'notion' in output.lower() or 
                'api' in output.lower() or
                'credentials' in output.lower() or
                'authentication' in output.lower() or
                'permissions' in output.lower()
            )
        except subprocess.CalledProcessError as e:
            # This is acceptable if credentials aren't set up
            pass

if __name__ == '__main__':
    unittest.main()
