"""
 @author Rajkumar Palanikumar (original), Ibn Aleem (modified)
 @date 15/01/2019 (original), 15/01/2019 (modified)
 @description Access token class to store the access token and its expiry time
"""

import time
from typing import Optional

class AccessToken:
    def __init__(self, access_token: str, expires_in: int, token_type: str, environment, refresh_token=None):
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.created_at = time.time()
        self.path = "/v1/oauth2/token"
        self.verb = "POST"
        self.body = {}
        if refresh_token:
            self.body["grant_type"] = "refresh_token"
            self.body["refresh_token"] = refresh_token
        else:
            self.body["grant_type"] = "client_credentials"

        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": environment.authorization_string(),
        }

    def is_expired(self) -> bool:
        return self.created_at + self.expires_in <= time.time()

    def remaining_time(self) -> Optional[int]:
        remaining = self.expires_in - (time.time() - self.created_at)
        return max(int(remaining), 0) if not self.is_expired() else None

    def authorization_string(self) -> str:
        return f"{self.token_type} {self.access_token}"

    def __str__(self) -> str:
        return f"AccessToken(type={self.token_type}, token={self.access_token}, expires_in={self.expires_in})"
