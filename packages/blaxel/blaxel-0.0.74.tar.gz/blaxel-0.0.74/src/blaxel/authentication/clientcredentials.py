"""
This module provides the ClientCredentials class, which handles client credentials-based
authentication for Blaxel. It manages token refreshing and authentication flows using
client credentials and refresh tokens.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator, Optional

import requests
from httpx import Auth, Request, Response

from blaxel.common.settings import get_settings


@dataclass
class DeviceLoginFinalizeResponse:
    access_token: str
    expires_in: int
    refresh_token: str
    token_type: str


class ClientCredentials(Auth):
    """
    A provider that authenticates requests using client credentials.
    """

    def __init__(self, credentials, workspace_name: str, base_url: str):
        """
        Initializes the ClientCredentials provider with the given credentials, workspace name, and base URL.

        Parameters:
            credentials: Credentials containing access and refresh tokens.
            workspace_name (str): The name of the workspace.
            base_url (str): The base URL for authentication.
        """
        self.credentials = credentials
        self.expires_at = None
        self.workspace_name = workspace_name
        self.base_url = base_url

    def get_headers(self):
        """
        Retrieves the authentication headers after ensuring tokens are valid.

        Returns:
            dict: A dictionary of headers with Bearer token and workspace.

        Raises:
            Exception: If token refresh fails.
        """
        err = self.get_token()
        if err:
            raise err
        return {
            "X-Blaxel-Authorization": f"Bearer {self.credentials.access_token}",
            "X-Blaxel-Workspace": self.workspace_name,
        }

    def get_token(self) -> Optional[Exception]:
        """
        Checks if the access token needs to be refreshed and performs the refresh if necessary.

        Returns:
            Optional[Exception]: An exception if refreshing fails, otherwise None.
        """
        settings = get_settings()
        if self.need_token():
            headers = {"Authorization": f"Basic {self.credentials.client_credentials}", "Content-Type": "application/json"}
            body = {"grant_type": "client_credentials"}
            response = requests.post(f"{settings.base_url}/oauth/token", headers=headers, json=body)
            response.raise_for_status()
            creds = response.json()
            self.credentials.access_token = creds["access_token"]
            self.credentials.refresh_token = creds["refresh_token"]
            self.credentials.expires_in = creds["expires_in"]
            self.expires_at = datetime.now() + timedelta(seconds=self.credentials.expires_in)
        return None

    def need_token(self):
        if not self.expires_at:
            return True
        return datetime.now() > self.expires_at - timedelta(minutes=10)

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        """
        Processes the authentication flow by ensuring tokens are valid and adding necessary headers.

        Parameters:
            request (Request): The HTTP request to authenticate.

        Yields:
            Request: The authenticated request.

        Raises:
            Exception: If token refresh fails.
        """
        self.get_token()
        request.headers["X-Blaxel-Authorization"] = f"Bearer {self.credentials.access_token}"
        request.headers["X-Blaxel-Workspace"] = self.workspace_name
        yield request
