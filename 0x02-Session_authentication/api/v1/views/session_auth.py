#!/usr/bin/env python3
""" Session authentication module
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Handles POST requests to /auth_session/login.

    Parameters:
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        - A JSON response with the error message
        and a 400 status code if the email or password is missing.
        - A JSON response with the error message
        and a 404 status code if the user is not found.
        - A JSON response with the error message
        and a 401 status code if the password is incorrect.
        - A JSON response with the user's info
        and a 200 status code if the credentials are correct.
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    if session_id is None:
        return jsonify({"error": "error creating the session"}), 500

    user_json = user.to_json()
    response = jsonify(user_json)
    session_name = getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Logs the user out of the session.

    - Destroys the user's session.
    - Returns a JSON response with an empty dictionary and a 200 status code.
    """
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)

    return jsonify({})
