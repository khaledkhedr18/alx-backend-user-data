#!/usr/bin/env python3
'''Basic authentication module'''
from models.user import User
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
        split_header = decoded_base64_authorization_header.split(":", 1)
        if len(split_header) != 2:
            return (None, None)
        return tuple(split_header)

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
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> myUser:
        """Retrieves the user from a request.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
