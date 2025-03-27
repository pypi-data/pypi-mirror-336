"""This module contains utility functions for the ThoughtHub project."""

import requests
import time

# Global variables to store token and timestamp
_cached_token = None
_token_timestamp = None


def get_stytch_token(client_id: str, client_secret: str, project_id: str) -> str:
    """Get a Stytch access token for the ThoughtHub project.

    Args:
        client_id (str): The Stytch client ID.
        client_secret (str): The Stytch client secret.
        project_id (str): The Stytch project ID.

    Returns:
        str: The Stytch access token.
    """
    global _cached_token, _token_timestamp

    # Check if token exists and is valid (less than 30 minutes old)
    current_time = time.time()
    if _cached_token and _token_timestamp and (current_time - _token_timestamp < 3600):
        print("Using cached token...")
        return _cached_token

    print("No valid token in memory, requesting new token...")

    # Validate required environment variables
    missing_vars = []
    if not client_id:
        missing_vars.append("STYTCH_CLIENT_ID")
    if not client_secret:
        missing_vars.append("STYTCH_CLIENT_SECRET")
    if not project_id:
        missing_vars.append("STYTCH_PROJECT_ID")

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    # API endpoint
    url = f"https://api.stytch.com/v1/public/{project_id}/oauth2/token"

    # Request headers
    headers = {"Content-Type": "application/json"}

    # Request payload
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Get the access token
        access_token = response.json()["access_token"]

        # Update global variables
        _cached_token = access_token
        _token_timestamp = time.time()

        return access_token

    except requests.exceptions.RequestException as e:
        error_message = f"Error making request: {e}"
        if hasattr(e, "response") and hasattr(e.response, "text"):
            error_message += f"\nResponse text: {e.response.text}"
        raise RuntimeError(error_message)
