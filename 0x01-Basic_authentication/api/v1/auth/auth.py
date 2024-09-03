#!/usr/bin/env python3
from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    """
    Auth class
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the Auth class.

        Returns:
            None
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths
            that do not require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the current user's authorization header from the request.

        Args:
            request: The request object containing user information.

        Returns:
            The authorization header as a string.
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user from the request.

        Args:
            request: The request object containing user information.

        Returns:
            The current user object.
        """
        return None
