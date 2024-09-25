from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
import json

# from app.api_gateway.utils.route_adder import add_routes
# from app.api_gateway.routes.routes import car_hub_routes
from app.core.authentification.auth import requires_auth
from config import Config
from app.features.login.login import Login
from app.features.login.register import Register
from app.features.users.users import Users
from app.features.cars.cars_listing import CarsListing

def get_api_name():
    global api
    api = Flask(__name__)
    return api


api = get_api_name()
api.config.from_object(Config)
api.config['CORS_HEADERS'] = 'Content-Type'
# Configure CORS
CORS(api, resources={r"/*": {"origins": "*",
                             "methods": ["GET", "POST", "PATCH", "DELETE", "PUT"],
                             "allow_headers": ["Content-Type",]}})

api_routes = Api(api)


def get_global_api():
    global api
    return api

@api.after_request
def add_custom_headers(response):
    return response


@api.after_request
def replace_none_to_null_value(response):
    try:
        data = response.data
        if isinstance(data, bytes):
            data = data.decode('latin-1')
        data = data.replace('"None"', 'null')
        response.data = data
        return response
    except Exception:
        return response


@api.before_request
def check_auth():
    message_error_auth = requires_auth()
    if message_error_auth:
        return message_error_auth


@api.before_request
def decode_body():
    try:
        if request.data is not None and request.data != b'':
            data = request.data.decode('latin-1')
            data = json.loads(data)
            request.data = data
    except Exception:
        pass


api_routes.add_resource(Login, '/login')
api_routes.add_resource(Register,"/register")
api_routes.add_resource(Users,"/users")
api_routes.add_resource(CarsListing,"/cars")


if __name__ == '__main__':

    api.run(host='0.0.0.0', port=5000)