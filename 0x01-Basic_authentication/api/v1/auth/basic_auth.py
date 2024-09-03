#!/usr/bin/env python3
'''Basic authentication module'''
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic authentication class.
    """

    def __init__(self):
        """
        Initializes a new BasicAuth instance.
        """
        super().__init__()
