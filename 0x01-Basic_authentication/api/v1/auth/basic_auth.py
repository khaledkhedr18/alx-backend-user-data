#!/usr/bin/env python3
'''Basic authentication module'''
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    Basic authentication class.
    """

    def __init__(self) -> None:
        super().__init__()

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 encoded authorization
        token from the Authorization header.

        Args:
            authorization_header (str):
            The Authorization header to extract the token from.

        Returns:
            str: The extracted Base64 encoded token,
            or None if the header is invalid.
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 authorization header.

        Args:
            base64_authorization_header (str):
            The Base64 authorization header to decode.

        Returns:
            str: The decoded authorization header,
            or None if decoding fails.
        """
        if type(base64_authorization_header) == str:
            try:
                return base64.b64decode(base64_authorization_header).decode('utf-8')
            except Exception:
                return None
        return None
