from app.utils.token.token import Token
import jwt
from flask import request, g

from app.core.authentification.const import routes_without_token
from config import SECRET_KEY


def create_token(user_id='Seven'):
    return Token().create_token(user_id)


# def requires_auth():
#     if request.method == 'GET' and request.path in routes_without_token:
#         return
    
#     token = get_auth_header_token()
#     if not token:
#         return {'message': 'Token required'}, 401
    
#     try:
#         g.token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#     except jwt.ExpiredSignatureError:
#         return {'message': 'Token has expired'}, 401
#     except jwt.InvalidTokenError:
#         return {'message': 'Invalid token'}, 401


def requires_auth():
    if request.method == 'GET':
        # Check for base routes in `routes_without_token`
        for route in routes_without_token:
            if request.path.startswith(route):
                return  # Allow access without a token

    token = get_auth_header_token()
    if not token:
        return {'message': 'Token required'}, 401

    try:
        g.token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return {'message': 'Token has expired'}, 401
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token'}, 401

def get_auth_header_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    try: 
        token = request.authorization.token
        return token
    except IndexError:
        return None


