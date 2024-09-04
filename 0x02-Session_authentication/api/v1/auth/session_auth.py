#!/usr/bin/env python3
'''Session authentication module'''
from api.v1.auth.auth import Auth
from uuid import uuid4


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
