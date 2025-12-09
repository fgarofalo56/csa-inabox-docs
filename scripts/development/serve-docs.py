#!/usr/bin/env python3
"""
Local Development Server for Azure Synapse Analytics Documentation
This script helps to run the documentation site locally for development and
testing.

Usage:
  python serve-docs.py [--port PORT]
"""

import argparse
import subprocess
import sys
import webbrowser
from time import sleep


def run_server(port=8000):
    """Run the MkDocs server on the specified port."""
    print(f"Starting documentation server on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")

    try:
        # Open the browser after a short delay to ensure server has started
        def open_browser():
            sleep(2)
            webbrowser.open(f"http://localhost:{port}")

        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()

        # Start the mkdocs server
        subprocess.run(
            f"mkdocs serve -a localhost:{port}", 
            shell=True, 
            check=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except subprocess.CalledProcessError:
        print("\nError starting MkDocs server. Make sure MkDocs is installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run the documentation site locally for development and testing"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port number (default: 8000)"
    )

    args = parser.parse_args()
    run_server(args.port)


if __name__ == "__main__":
    main()
