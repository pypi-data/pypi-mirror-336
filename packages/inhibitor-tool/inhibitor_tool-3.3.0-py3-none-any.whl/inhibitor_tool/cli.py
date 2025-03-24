"""
Author: mmwei3
Email: mmwei@iflytek.com
Contact: 178555350258
Date: 2025-03-19
Description: CLI entry point for sending, removing, and listing inhibition requests.
"""

import argparse
import json
from inhibitor_tool.inhibitor import inhibit, remove_inhibition, list_inhibitions


# version
VERSION = "3.3.0"


def print_table(data):
    """
    Print inhibition data in a human-readable table format.
    """
    if not data:
        print("No active inhibitions found.")
        return

    header = ["ID", "Content", "Start Time", "Duration (h)", "Remark"]
    col_widths = [
        max(len(str(row[i])) for row in data + [header]) for i in range(len(header))
    ]

    # Print header
    print(" | ".join(f"{header[i]:<{col_widths[i]}}" for i in range(len(header))))
    print("-" * (sum(col_widths) + 3 * (len(header) - 1)))

    # Print rows
    for row in data:
        print(" | ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(row))))


def main():
    """
    Parse command-line arguments and process inhibition requests.
    """

    parser = argparse.ArgumentParser(description="CLI tool for inhibition requests.")

    # version
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"inhibitor_tool {VERSION}",
        help="Show program's version number and exit.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # **add inhibition**
    inhibit_parser = subparsers.add_parser("add", help="Send an inhibition request.")
    inhibit_parser.add_argument(
        "--content",
        type=str,
        required=True,
        help="Content to inhibit (at least 10 characters, no spaces).",
    )
    inhibit_parser.add_argument(
        "--ttl", type=int, default=3, help="TTL in hours (default: 3, max: 720)."
    )
    inhibit_parser.add_argument(
        "--remark",
        type=str,
        default="tmp_inhibitor",
        help="Optional remark (default: 'tmp_inhibitor').",
    )

    # **remove inhibition**
    remove_parser = subparsers.add_parser(
        "remove", help="Remove an inhibition request."
    )
    remove_parser.add_argument(
        "--content", type=str, required=True, help="Content to remove from inhibition."
    )

    # **list inhibitions**
    list_parser = subparsers.add_parser("list", help="List all active inhibitions.")
    list_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format."
    )

    args = parser.parse_args()

    # exec
    if args.command == "add":
        inhibit(args.content, args.ttl, args.remark)
    elif args.command == "remove":
        remove_inhibition(args.content)
    elif args.command == "list":
        data = list_inhibitions()

        if args.json:
            print(json.dumps(data, indent=4))
        else:
            formatted_data = [
                [
                    item["id"],
                    item["maskContent"],
                    item["policyStartTime"],
                    item["duration"],
                    item["remark"],
                ]
                for item in data
            ]
            print_table(formatted_data)


if __name__ == "__main__":
    main()
