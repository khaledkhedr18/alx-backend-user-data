#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


@app.before_request
def before_request():
    """
    Handles the before_request event in Flask.

    This function is called before each request to the API. It checks if the
    authentication object is None. If it is not None, it checks if the current
    path is in the excluded paths. If it isnt, it checks for the authorization
    header and the current user. If either of these checks fail, it aborts the
    request with a 401 or 403 status code respectively.

    Parameters:
        None

    Returns:
        None
    """
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    '''
    This function handles the unauthorized error
    '''
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handles the HTTP 403 Forbidden error.

    Parameters:
        error (str): The error message.

    Returns:
        str: A JSON response with the error message.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    auth_type = getenv('AUTH_TYPE')
    if auth_type:
        auth = Auth()
    app.run(host=host, port=port)
