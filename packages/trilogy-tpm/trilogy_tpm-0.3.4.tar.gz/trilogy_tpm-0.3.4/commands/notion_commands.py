#!/usr/bin/env python3
"""
Notion commands for TPM-CLI.
"""

import os
import sys
import argparse
import json
from rich.console import Console
from utils.notion_utils import (
    check_notion_status,
    list_notion_pages,
    add_content,
    create_new_page,
    upload_directory,
    set_notion_token,
)

console = Console()

def setup_notion_parser(subparsers):
    """Set up the Notion command parser."""
    notion_parser = subparsers.add_parser('notion', help='Notion commands')
    notion_subparsers = notion_parser.add_subparsers(dest='notion_action', help='Notion action')
    
    # Status command
    status_parser = notion_subparsers.add_parser('status', help='Check Notion API status')
    
    # List pages command
    list_parser = notion_subparsers.add_parser('list', help='List Notion pages')
    list_parser.add_argument('--limit', type=int, default=10, help='Maximum number of pages to list')
    list_parser.add_argument('--full-ids', action='store_true', help='Show full page IDs')
    
    # Add content command
    add_parser = notion_subparsers.add_parser('add', help='Add content to a Notion page')
    add_parser.add_argument('page', help='Page ID or name to add content to')
    add_parser.add_argument('--markdown', help='Markdown file to add')
    add_parser.add_argument('--sample', action='store_true', help='Use sample markdown content')
    add_parser.add_argument('--debug', action='store_true', help='Show debug information')
    add_parser.add_argument('--mode', choices=['append', 'replace'], default='append', 
                           help='How to add content: append to page or replace page content')
    add_parser.add_argument('--replace-marker', help='Marker to replace in the page (for replace mode)')
    add_parser.add_argument('--format', action='store_true', help='Format markdown for Notion compatibility')
    
    # Create page command
    create_parser = notion_subparsers.add_parser('create', help='Create a new Notion page')
    create_parser.add_argument('title', help='Title of the new page')
    create_parser.add_argument('--markdown', help='Markdown file to use as content')
    create_parser.add_argument('--sample', action='store_true', help='Use sample markdown content')
    create_parser.add_argument('--debug', action='store_true', help='Show debug information')
    create_parser.add_argument('--format', action='store_true', help='Format markdown for Notion compatibility')
    
    # Upload directory command
    upload_parser = notion_subparsers.add_parser('upload', 
                                               help='Upload a directory of markdown files to Notion')
    upload_parser.add_argument('directory', help='Directory containing markdown files')
    upload_parser.add_argument('parent_page', help='Parent page ID or name')
    upload_parser.add_argument('--format', action='store_true', 
                              help='Format markdown for Notion compatibility')
    upload_parser.add_argument('--debug', action='store_true', help='Show debug information')
    upload_parser.add_argument('--mode', choices=['create', 'update'], default='create',
                              help='Create new pages or update existing ones')
    
    return notion_parser

def handle_notion_commands(args):
    """Handle Notion commands."""
    if args.notion_action == 'status':
        try:
            check_notion_status()
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
    
    elif args.notion_action == 'list':
        try:
            list_notion_pages(args.limit, args.full_ids)
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
    
    elif args.notion_action == 'add':
        try:
            add_content(args.page, args.markdown, args.sample, args.debug, 
                       args.mode, getattr(args, 'replace_marker', None), args.format)
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
    
    elif args.notion_action == 'create':
        try:
            create_new_page(args.title, args.markdown, args.sample, args.debug, args.format)
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
    
    elif args.notion_action == 'upload':
        try:
            upload_directory(args.directory, args.parent_page, args.format, args.debug, args.mode)
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
    
    else:
        console.print("[bold red]Please specify a Notion action.[/bold red]")
        console.print("Run 'tpm notion --help' for usage information.")
