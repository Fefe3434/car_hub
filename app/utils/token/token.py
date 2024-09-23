import logging
import jwt
import datetime
from config import SECRET_KEY


# Configure logging to output to the console
logging.basicConfig(level=logging.DEBUG)

class Token:
    def __init__(self) -> None:
        self.KEY = SECRET_KEY
        self.TOKEN_TIME_OUT = 60 * 3  # 3 minutes (corrected to 3 minutes)
        self.TOKEN_ALMOST_EXPIRED = 60 * 2  # 2 minutes
        self.user = ''
        self.time_expire = datetime.datetime.utcnow()
        self.time_almost_expire = datetime.datetime.utcnow()
        self.is_expired = True
        self.error = ''
        logging.debug("Token object initialized.")

    def create_token(self, user_id):
        logging.debug(f"Creating token for user: {user_id}")
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.TOKEN_TIME_OUT),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            token = jwt.encode(payload, self.KEY, algorithm='HS256')
            logging.debug(f"Token created successfully: {token}")
            return token
        except Exception as e:
            logging.error(f"Error creating token: {e}")
            return str(e)

    def decode_token(self, auth_token):
        logging.debug(f"Decoding token: {auth_token}")
        try:
            payload = jwt.decode(jwt=auth_token, key=self.KEY, algorithms=['HS256'])
            logging.debug(f"Decoded payload: {payload}")
            self.user = payload['sub']
            self.expire = payload['exp']
            self.time_almost_expire = payload['iat']
            self.is_expired = False
            return self.is_expired, self.error
        except jwt.ExpiredSignatureError:
            logging.error("Token expired.")
            self.error = {'message': 'Session Expired'}, 401
            self.is_expired = True
            return self.is_expired, self.error
        except jwt.InvalidTokenError:
            logging.error("Invalid token.")
            self.error = {'message': 'Session Invalid'}, 405
            self.is_expired = True
            return self.is_expired, self.error

    def is_token_expired(self, auth_token):
        logging.debug(f"Checking if token is expired: {auth_token}")
        self.decode_token(auth_token)
        try:
            if (datetime.datetime.now() - datetime.datetime.utcfromtimestamp(self.expire)).seconds > self.TOKEN_TIME_OUT:
                logging.debug("Token is expired.")
                return True
            return False
        except Exception as e:
            logging.error(f"Error checking token expiration: {e}")
            return False

    def is_token_almost_expired(self, auth_token):
        logging.debug(f"Checking if token is almost expired: {auth_token}")
        self.decode_token(auth_token)
        try:
            if (datetime.datetime.now() - datetime.datetime.utcfromtimestamp(self.time_almost_expire)).seconds > self.TOKEN_ALMOST_EXPIRED:
                logging.debug("Token is almost expired.")
                return True
            return False
        except Exception as e:
            logging.error(f"Error checking token almost expiration: {e}")
            return False


if __name__ == '__main__':
    token = Token()
    _jwt = token.create_token("ro-1658841642497")
    logging.debug(f"Generated JWT: {_jwt}")
    decoded_token = token.decode_token(_jwt)
    logging.debug(f"Decoded JWT: {decoded_token}")
