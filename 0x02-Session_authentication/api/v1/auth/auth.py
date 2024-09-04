#!/usr/bin/env python3
'''Authentication Module'''
from flask import request
from typing import List, TypeVar
import re
from os import getenv

User = TypeVar('User')


class Auth:
    """Auth class
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
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the current user's authorization header from the request.

        Args:
            request: The request object containing user information.

        Returns:
            The authorization header as a string.
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user from the request.

        Args:
            request: The request object containing user information.

        Returns:
            The current user object.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the current user's session cookie from the request.

        Args:
            request: The request object containing user information.

        Returns:
            The session cookie as a string.
        """
        if request is None:
            return None
        cookie_name = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(cookie_name)
