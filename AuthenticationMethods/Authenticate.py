import datetime
from flask import request, abort
import jwt
from functools import wraps


# Wrapper decorator method for below method
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if has_user_authenticated() != 200:
            return abort(401, "Unauthorized, please log in first.")
        return func(*args, **kwargs)

    return wrapper


# Method to check for user log in authentication
def has_user_authenticated():
    # Get the JWT token from the request cookie
    token = request.cookies.get('Authorization')
    if token is None:
        return abort(401, description="Unauthorized, please log in first.")
    # Verify the JWT token
    try:
        payload = jwt.decode(token, "secret-key", "HS256")
    except jwt.DecodeError as e:
        return abort(401, description=f"{e}")
    if datetime.datetime.fromtimestamp(payload['exp']) <= datetime.datetime.utcnow():
        return abort(401, description="Your log in session has expired. Please log in again.")

    # The token is valid, proceed with the request
    return 200
