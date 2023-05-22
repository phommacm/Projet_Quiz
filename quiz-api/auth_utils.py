from flask import request

from jwt_utils import decode_token, JwtError

def authenticate():
    auth_header = request.headers.get('Authorization')

    if auth_header is not None:
        auth_token = auth_header.split(" ")[1]

        try:
            user_id = decode_token(auth_token)
            if user_id != 'quiz-app-admin':
                return "Unauthorized", 401
        except JwtError:
            return "Unauthorized", 401

    else:
        return "Unauthorized", 401
    