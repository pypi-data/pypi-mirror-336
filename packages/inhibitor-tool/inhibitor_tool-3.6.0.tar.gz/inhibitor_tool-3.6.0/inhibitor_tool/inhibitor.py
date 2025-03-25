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
        print("Success: Inhibition request sent.")
    else:
        print(
            f"Error: Failed to send inhibition request. Status: {response.status_code}, Response: {response.text}"
        )


def remove_inhibition(content: str):
    """
    Remove an existing inhibition based on `maskContent`.
    """

    # Validate content
    if not validate_content(content):
        print(
            "Error: Inhibition content must be at least 10 characters and cannot contain spaces."
        )
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
    data = {"maskContent": content}

    # Send DELETE request
    response = requests.post(remove_url, headers=headers, json=data, verify=False)

    # Handle response
    if response.status_code == 200:
        print("Success: Inhibition removed.")
    else:
        print(
            f"Error: Failed to remove inhibition. Status: {response.status_code}, Response: {response.text}"
        )


def list_inhibitions():
    """
    Fetch and display the list of active inhibitions from the API.
    """
    try:
        #
        username = os.environ["USERNAME"]
        password = os.environ["PASSWORD"]
        login_url = os.environ["LOGIN_URL"]
        list_url = os.environ["LIST_URL"]
    except KeyError as e:
        print(
            f"Error: Missing required environment variable: {e}. Run `source ~/.auth_token` first."
        )
        sys.exit(1)

    # get Token
    token = get_token(username, password, login_url)
    if not token:
        print("Error: Unable to retrieve authentication token.")
        sys.exit(1)

    # send API
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(list_url, headers=headers, verify=False)

    # api
    if response.status_code == 200:
        try:
            data = response.json()
            if data and "data" in data and "list" in data["data"]:
                inhibition_list = data["data"]["list"]
                if inhibition_list:
                    # print
                    for item in inhibition_list:
                        print(
                            f"ID: {item['id']}, Name: {item['name']},maskContent: {item['maskContent']}, Duration: {item['duration']}, durationUnit: {item['durationUnit']},Remark: {item['remark']}"
                        )
                else:
                    print("No active inhibitions found.")
            else:
                print("Error: Invalid response format, 'data' or 'list' not found.")
        except ValueError:
            print("Error: Failed to parse response as JSON.")
    else:
        print(
            f"Error: Failed to fetch inhibitions. Status: {response.status_code}, Response: {response.text}"
        )
