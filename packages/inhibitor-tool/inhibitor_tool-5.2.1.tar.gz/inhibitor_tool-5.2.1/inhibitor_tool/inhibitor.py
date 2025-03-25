"""
Author: mmwei3
Email: mmwei@iflytek.com
Contact: 178555350258
Date: 2025-03-19
Description: A CLI tool for sending and deleting inhibition requests via API.
"""

import requests
import datetime
import sys
import os
import json
from inhibitor_tool.auth import get_token
from inhibitor_tool.utils import validate_content
from inhibitor_tool.constants import MAX_TTL


def inhibit(content: str, ttl: int, remark: str):
    """
    Send an inhibition request with the given content and TTL.
    """
    # Validate inhibition content
    if not validate_content(content):
        print(
            "Error: Inhibition content must be at least 10 characters and cannot contain spaces."
        )
        sys.exit(1)

    # Validate TTL duration
    if ttl > MAX_TTL:
        print(f"Error: TTL cannot exceed {MAX_TTL} hours.")
        sys.exit(1)

    # Read required environment variables
    try:
        username = os.environ["USERNAME"]
        password = os.environ["PASSWORD"]
        login_url = os.environ["LOGIN_URL"]
        inhibit_url = os.environ["INHIBIT_URL"]
    except KeyError as e:
        print(
            f"Error: Missing required environment variable: {e}. Please run `source ~/.auth_token` first."
        )
        sys.exit(1)

    # Get authentication token
    token = get_token(username, password, login_url)
    if not token:
        print("Error: Unable to retrieve authentication token.")
        sys.exit(1)

    # Generate request metadata
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    name = f"cli_{username}_{timestamp}"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "type": 1,
        "state": 0,
        "maskAlarmType": "content",
        "policyStartTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "durationUnit": "h",
        "name": name,
        "maskContent": content,
        "duration": str(ttl),
        "remark": f"Inhibition request via CLI: {remark}",
    }

    # Send API request
    response = requests.post(inhibit_url, headers=headers, json=data, verify=False)

    # Handle response
    if response.status_code == 200:
        print(f"Success: Inhibition request sent. Name: { content }")
    else:
        print(
            f"Error: Failed to send inhibition request. Status: {response.status_code}, Response: {response.text}"
        )


def remove_inhibition(id: str = None, content: str = None):
    """
    Remove an existing inhibition based on `id` or `content`.
    """

    # Validate content
    if content and not validate_content(content):
        print(
            "Error: Inhibition content must be at least 10 characters and cannot contain spaces."
        )
        sys.exit(1)

    if not id and not content:
        print("Error: You must specify either 'id' or 'content'.")
        sys.exit(1)

    # Read required environment variables
    try:
        username = os.environ["USERNAME"]
        password = os.environ["PASSWORD"]
        login_url = os.environ["LOGIN_URL"]
        remove_url = os.environ["REMOVE_URL"]  # 新增删除接口 URL
    except KeyError as e:
        print(
            f"Error: Missing required environment variable: {e}. Please run `source ~/.auth_token` first."
        )
        sys.exit(1)

    # Get authentication token
    token = get_token(username, password, login_url)
    if not token:
        print("Error: Unable to retrieve authentication token.")
        sys.exit(1)

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Prepare the data for the API request based on the provided parameters
    # data = {}
    # Start with the base URL
    if id:
        remove_url += f"?id={id}"
    elif content:
        remove_url += f"?content={content}"

    # Send DELETE request
    response = requests.delete(remove_url, headers=headers, verify=False)

    # Handle response
    if response.status_code == 200:
        print("Success: Inhibition removed.")
    else:
        print(
            f"Error: Failed to remove inhibition. Status: {response.status_code}, Response: {response.text}"
        )


def list_inhibitions(json_output: bool = False):
    """
    Fetch and display the list of active inhibitions from the API.
    If `json_output` is True, output raw JSON data; otherwise, return the inhibition data.
    """
    try:
        username = os.environ["USERNAME"]
        password = os.environ["PASSWORD"]
        login_url = os.environ["LOGIN_URL"]
        list_url = os.environ["LIST_URL"]
    except KeyError as e:
        print(
            f"Error: Missing required environment variable: {e}. Run `source ~/.auth_token` first."
        )
        sys.exit(1)

    # Get authentication token
    token = get_token(username, password, login_url)
    if not token:
        print("Error: Unable to retrieve authentication token.")
        sys.exit(1)

    # Send API request
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(list_url, headers=headers, verify=False)

    # Handle response
    if response.status_code == 200:
        try:
            data = response.json()
            if data and "data" in data and "list" in data["data"]:
                inhibition_list = data["data"]["list"]
                if json_output:
                    # Output the raw JSON data
                    return json.dumps(data, indent=4)  # Return JSON formatted data
                else:
                    # Return the list of inhibitions (data)
                    return inhibition_list
            else:
                print("Error: Invalid response format, 'data' or 'list' not found.")
        except ValueError:
            print("Error: Failed to parse response as JSON.")
    else:
        print(
            f"Error: Failed to fetch inhibitions. Status: {response.status_code}, Response: {response.text}"
        )
    return None  # Return None in case of errors or no data
