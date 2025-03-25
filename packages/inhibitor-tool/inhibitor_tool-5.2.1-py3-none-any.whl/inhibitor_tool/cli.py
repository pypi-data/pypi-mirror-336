"""
Author: mmwei3
Email: mmwei@iflytek.com
Contact: 178555350258
Date: 2025-03-19
Description: A CLI tool for sending and deleting inhibition requests via API.
"""

import argparse
import json
import sys
from inhibitor_tool.inhibitor import inhibit, remove_inhibition, list_inhibitions


# version
VERSION = "5.2.1"


def print_table(data):
    """
    Print inhibition data in a human-readable table format.
    """
    if not data:
        print("No active inhibitions found.")
        return

    header = [
        "ID",
        "Content",
        "Start Time",
        "Duration",
        "durationUnit",
        "Remark",
        "createBy",
    ]
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
    remove_parser.add_argument("--id", type=str, help="ID of the inhibition to remove.")
    remove_parser.add_argument(
        "--content", type=str, help="Content of the inhibition to remove."
    )

    # **list inhibitions**
    list_parser = subparsers.add_parser("list", help="List all active inhibitions.")
    list_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format."
    )

    args = parser.parse_args()

    # If no command is provided, show help
    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # exec
    if args.command == "add":
        inhibit(args.content, args.ttl, args.remark)
    elif args.command == "remove":
        if not (args.id or args.content):
            print("Error: You must specify either --id or --content.")
            sys.exit(1)

        # Construct the URL and print it
        base_url = "http://domp.iflytek.cn/api/v1/alarm/blacklist"
        remove_url = (
            f"{base_url}?id={args.id}"
            if args.id
            else f"{base_url}?content={args.content}"
        )

        # Print the URL for debugging or informational purposes
        print(f"Requesting to remove inhibition with URL: {remove_url}")

        remove_inhibition(args.id, args.content)
    elif args.command == "list":
        data = list_inhibitions(json_output=args.json)

        if args.json:
            if data:
                # print(json.dumps(data, indent=4, ensure_ascii=False))
                print(data)
            else:
                print("Error: Failed to retrieve inhibition data.")
                sys.exit(1)
        else:
            # Assuming data is a list of inhibitions
            if data:
                formatted_data = [
                    [
                        item["id"],
                        item["maskContent"],
                        item["policyStartTime"],
                        item["duration"],
                        item["durationUnit"],
                        item["remark"],
                        item["createBy"],
                    ]
                    for item in data
                ]
                print_table(formatted_data)
            else:
                print("Error: Failed to retrieve or parse inhibition data.")
                sys.exit(1)


if __name__ == "__main__":
    main()
