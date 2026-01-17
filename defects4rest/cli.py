#-------------------------------------------------------------------------------
# Copyright (c) 2026 Rahil Piyush Mehta, Kausar Y. Moshood, Huwaida Rahman Yafie and Manish Motwani
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------

"""
Defects4REST Command-Line Interface (CLI) entry point.

This module provides the main CLI interface for the Defects4REST tool,
supporting commands to retrieve bug information and checkout/deploy bug versions.
"""
import argparse
from defects4rest.src.command_scripts import info, checkout

def main():
    """
    Main entry point for the Defects4REST CLI application.

    Parses command-line arguments and dispatches to appropriate subcommands:
    - info: Display detailed bug information
    - checkout: Checkout and deploy specific bug versions
    """
    # Create the main argument parser for the CLI
    parser = argparse.ArgumentParser(
        prog="defects4rest",
        description="Defects4REST CLI Tool"
    )
    # Create subparsers to handle different commands (info, checkout, etc.)
    subparsers = parser.add_subparsers(dest="command")

    # === info command ===
    info_parser = subparsers.add_parser("info", help="Show bug info")
    info_parser.add_argument("-p", "--project", required=True, help="Project name (e.g., awx)")
    info_parser.add_argument("-i", "--issue_id", type=int, required=True, help="Issue ID")

    # === checkout command ===
    checkout_parser = subparsers.add_parser("checkout", help="Checkout bug version and deploy")
    checkout_parser.add_argument("-p", "--project", required=True, help="Project name (e.g., awx)")
    checkout_parser.add_argument("-i", "--issue_id", type=int, required=True, help="Issue ID")
    checkout_parser.add_argument("--buggy", action="store_true", help="Checkout the buggy version")
    checkout_parser.add_argument("--patched", type=int, nargs="?", const=1,help="Checkout the nth patched version (default is 1)")
    checkout_parser.add_argument("--start", action="store_true",help="Run deployment script (default with buggy/patched)")
    checkout_parser.add_argument("--stop", action="store_true", help="Stop running containers only")
    checkout_parser.add_argument("--clean", action="store_true", help="Stop and remove containers/volumes/networks")

    # Parse all command-line arguments
    args = parser.parse_args()

    # === info ===
    # Handle the 'info' command - display bug information
    if args.command == "info":
        info.run(args.project, args.issue_id)

    # === checkout ===
    # Handle the 'checkout' command - checkout/deploy/manage bug versions
    elif args.command == "checkout":
        # Determine which action to perform based on provided flags
        if args.clean:
            # Full cleanup: stop containers and remove volumes/networks
            action = "clean"
        elif args.stop:
            # Stop running containers only, keep volumes/networks
            action = "stop"
        elif args.start or args.buggy or args.patched:
            # Deploy/start the selected version (buggy or patched)
            action = "deploy"
        else:
            # No action specified
            action = "noop"

        # Dispatch to checkout module with all necessary parameters
        checkout.run(
            project_name=args.project,
            issue_id=args.issue_id,
            start=args.start,
            action=action,
            buggy=args.buggy,
            patched=args.patched
        )

    else:
        # No valid command provided - display help information
        parser.print_help()

if __name__ == "__main__":
    # Entry point when script is run directly (not imported)
    main()