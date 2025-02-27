from flask import request
import jwt

from app.data.model_db.db_cars_hub import User
from config import SECRET_KEY
from app.core.authentification.auth import get_auth_header_token



class UserInfo:
    def __init__(self, session):
        self.KEY = SECRET_KEY
        self.session = session

    @property
    def is_admin(self):
        token = get_auth_header_token()
        if not token:
            return False
        
        user = self._decode_token(request.authorization.token)
        user_info = self.session.query(User).filter(User.email == user).first()
        if user_info and user_info.is_admin:
            print(user_info.is_admin)
            return True
        return False

    @property
    def get_user(self):
        token = get_auth_header_token()
        if not token:
            return None 
        
        user = self._decode_token(request.authorization.token)
        user_info = self.session.query(User).filter(User.email == user).first()        
        return user_info

    def _decode_token(self, auth_token):
        try:
            payload = jwt.decode(jwt=auth_token, key=self.KEY, algorithms='HS256')
            user = payload['sub']
            # print(f"Decoded user from token: {user}")
            return user
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
