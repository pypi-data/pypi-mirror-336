"""
Command-line interface for PromptFlow.
"""

import argparse
import sys
from typing import List, Optional

from promptflow.ui import create_app


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        args: List of arguments to parse. If None, uses sys.argv[1:].

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="PromptFlow CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # UI command
    subparsers.add_parser("ui", help="Start the web UI for managing prompts")

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> None:
    """Main entry point for the CLI.

    Args:
        args: List of arguments to parse. If None, uses sys.argv[1:].
    """
    parsed_args = parse_args(args)

    if parsed_args.command == "ui":
        app = create_app()
        app.run()


if __name__ == "__main__":
    main()
