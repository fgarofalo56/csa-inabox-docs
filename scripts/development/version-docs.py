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


import re


# Pattern to validate version/alias strings (prevents shell injection)
SAFE_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9._-]+$')


def _validate_name(value: str, label: str) -> None:
    """Validate that a version/alias name contains only safe characters.

    Args:
        value: The value to validate
        label: Human-readable label for error messages

    Raises:
        ValueError: If the value contains unsafe characters
    """
    if not SAFE_NAME_PATTERN.match(value):
        raise ValueError(
            f"Invalid {label}: '{value}'. "
            f"Only alphanumeric characters, dots, hyphens, and underscores are allowed."
        )


def run_command(command):
    """Run a shell command and return the output.

    Uses list-based subprocess invocation to prevent shell injection.
    """
    try:
        result = subprocess.run(
            command, check=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.stderr}")
        sys.exit(1)


def create_version(version, alias=None, title=None, ignore=False, rebase=False):
    """Create a new documentation version."""
    _validate_name(version, "version")
    cmd = ["mike", "deploy", version]

    if alias:
        _validate_name(alias, "alias")
        cmd.append(alias)

    if title:
        cmd.extend(["--title", title])

    if ignore:
        cmd.append("--ignore")

    if rebase:
        cmd.append("--rebase")
    
    print(f"Creating version {version}...")
    result = run_command(cmd)
    print(result)
    print(f"Version {version} created successfully.")


def add_alias(version, alias):
    """Add an alias to an existing version."""
    _validate_name(version, "version")
    _validate_name(alias, "alias")
    cmd = ["mike", "alias", version, alias]
    
    print(f"Adding alias '{alias}' to version {version}...")
    result = run_command(cmd)
    print(result)
    print(f"Alias '{alias}' added to version {version} successfully.")


def delete_version(version):
    """Delete a documentation version."""
    _validate_name(version, "version")
    cmd = ["mike", "delete", version]
    
    print(f"Deleting version {version}...")
    result = run_command(cmd)
    print(result)
    print(f"Version {version} deleted successfully.")


def list_versions():
    """List all documentation versions."""
    cmd = ["mike", "list"]
    
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
    create_parser.add_argument("--ignore", action="store_true", help="Ignore unrelated histories when deploying")
    create_parser.add_argument("--rebase", action="store_true", help="Rebase onto remote when deploying")
    
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
        create_version(args.version, args.alias, args.title, args.ignore, args.rebase)
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
