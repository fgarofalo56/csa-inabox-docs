#!/usr/bin/env python3
"""
Version Documentation Script for Azure Synapse Analytics Documentation
This script helps to create and manage documentation versions using mike.

Usage:
  python version-docs.py create <version> [--alias <alias>] [--title <title>]
  python version-docs.py alias <version> <alias>
  python version-docs.py delete <version>
  python version-docs.py list
"""

import argparse
import os
import subprocess
import sys


def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(
            command, check=True, shell=True, text=True, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.stderr}")
        sys.exit(1)


def create_version(version, alias=None, title=None):
    """Create a new documentation version."""
    cmd = f"mike deploy {version}"
    
    if alias:
        cmd += f" {alias}"
    
    if title:
        cmd += f" --title \"{title}\""
    
    print(f"Creating version {version}...")
    result = run_command(cmd)
    print(result)
    print(f"Version {version} created successfully.")


def add_alias(version, alias):
    """Add an alias to an existing version."""
    cmd = f"mike alias {version} {alias}"
    
    print(f"Adding alias '{alias}' to version {version}...")
    result = run_command(cmd)
    print(result)
    print(f"Alias '{alias}' added to version {version} successfully.")


def delete_version(version):
    """Delete a documentation version."""
    cmd = f"mike delete {version}"
    
    print(f"Deleting version {version}...")
    result = run_command(cmd)
    print(result)
    print(f"Version {version} deleted successfully.")


def list_versions():
    """List all documentation versions."""
    cmd = "mike list"
    
    print("Listing all documentation versions...")
    result = run_command(cmd)
    
    if not result:
        print("No versions found.")
    else:
        print("\nAvailable versions:")
        print(result)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Manage documentation versions for Azure Synapse Analytics Documentation"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create version command
    create_parser = subparsers.add_parser("create", help="Create a new documentation version")
    create_parser.add_argument("version", help="Version number (e.g., '1.0.0')")
    create_parser.add_argument("--alias", help="Alias for this version (e.g., 'latest')")
    create_parser.add_argument("--title", help="Title for this version")
    
    # Add alias command
    alias_parser = subparsers.add_parser("alias", help="Add an alias to a version")
    alias_parser.add_argument("version", help="Target version number")
    alias_parser.add_argument("alias", help="Alias name to add")
    
    # Delete version command
    delete_parser = subparsers.add_parser("delete", help="Delete a documentation version")
    delete_parser.add_argument("version", help="Version to delete")
    
    # List versions command
    subparsers.add_parser("list", help="List all documentation versions")
    
    args = parser.parse_args()
    
    if args.command == "create":
        create_version(args.version, args.alias, args.title)
    elif args.command == "alias":
        add_alias(args.version, args.alias)
    elif args.command == "delete":
        delete_version(args.version)
    elif args.command == "list":
        list_versions()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
