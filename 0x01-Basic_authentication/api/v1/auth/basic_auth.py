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

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        if authorization_header is None or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
