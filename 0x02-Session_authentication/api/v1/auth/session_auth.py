#!/usr/bin/env python3
'''Session authentication module'''
from api.v1.auth.auth import Auth
from uuid import uuid4
from api.v1.views.users import User


class SessionAuth(Auth):
    '''Session authentication class'''
    user_id_by_session_id = {}

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user.

        Args:
            user_id (str): The user ID of the user to create a session for.

        Returns:
            str: The newly created session ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        self.session_id = str(uuid4())
        self.user_id_by_session_id[self.session_id] = user_id
        return self.session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Return the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID to retrieve a user ID for.

        Returns:
            str: The user ID associated with the given session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user from the request.

        Args:
            request: The request object containing user information.

        Returns:
            User: The current user object.
        """
        cookie = self.session_cookie(request)
        if cookie is None:
            return None
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the session user_id_by_session_id mapping for the session ID
        stored in the request cookie.

        Args:
            request: The request object containing the session ID cookie.

        Returns:
            bool: True if the session was deleted, False otherwise.
        """
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        session_id = self.user_id_for_session_id(cookie)
        if session_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
