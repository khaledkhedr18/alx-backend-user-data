#!/usr/bin/env python3
'''Basic authentication module'''
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
myUser = TypeVar('User')


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
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts user credentials
        from a decoded Base64 authorization header.

        Args:
            decoded_base64_authorization_header (str):
                The decoded Base64 authorization header
                to extract credentials from.

        Returns:
            Tuple[str, str]: A tuple containing the extracted user credentials
            (username, password) or (None, None) if extraction fails.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> myUser:
        """
        Returns the User object based on the email and password.

        Args:
            user_email (str): The email to search for.
            user_pwd (str): The password to verify.

        Returns:
            myUser: The User object if it exists and
            the password is correct, None otherwise.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = myUser.search({"email": user_email})
        if len(users) == 0:
            return None
        if not users[0].is_valid_password(user_pwd):
            return None
        return users[0]
