"""
 @author Rajkumar Palanikumar (original), Ibn Aleem (modified)
 @date 15/01/2019 (original), 15/01/2019 (modified)
 @description Access token class to store the access token and its expiry time
"""

import time
from typing import Optional

class AccessToken:
    def __init__(self, access_token: str, expires_in: int, token_type: str):
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.created_at = time.time()

    def is_expired(self) -> bool:
        return self.created_at + self.expires_in <= time.time()

    def remaining_time(self) -> Optional[int]:
        remaining = self.expires_in - (time.time() - self.created_at)
        return max(int(remaining), 0) if not self.is_expired() else None

    def refresh(self, new_token: str, new_expires_in: int) -> None:
        self.access_token = new_token
        self.expires_in = new_expires_in
        self.created_at = time.time()

    def authorization_string(self) -> str:
        return f"{self.token_type} {self.access_token}"

    def __str__(self) -> str:
        return f"AccessToken(type={self.token_type}, token={self.access_token}, expires_in={self.expires_in})"