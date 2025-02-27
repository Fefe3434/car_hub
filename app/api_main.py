from flask import Flask, make_response, request
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
from app.features.brands.brands import Brands
from app.features.brands.models import Models
from app.features.fuel.fuel_type import FuelTypes
from app.features.emission.emission_classe import EmissionClasses
from app.features.features.features_categories import FeaturesCategories
from app.features.features.features import Features
from app.shared.enum.enum import EnumResource
from app.features.favorites.favorites import Favorites
from app.features.reviews.reviews import Reviews
from app.features.messages.messages import Messages
from app.features.cars_images.car_images import CarImages
from app.features.cars_images.car_primary_image import CarPrimaryImage

def get_api_name():
    global api
    api = Flask(__name__)
    return api


api = get_api_name()
api.config.from_object(Config)
api.config['CORS_HEADERS'] = 'Content-Type'
# Configure CORS
# CORS(api, resources={r"/*": {"origins": "*",
#                              "methods": ["GET", "POST", "PATCH", "DELETE", "PUT", "OPTIONS"],
#                              "allow_headers": ["Content-Type",]}})

CORS(api, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PATCH", "DELETE", "PUT", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "expose_headers": ["Authorization"],
    }
})

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
def handle_preflight():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, DELETE, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
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
api_routes.add_resource(CarsListing,"/cars", "/cars/<int:id>")
api_routes.add_resource(Brands,"/brands")
api_routes.add_resource(Models,"/models")
api_routes.add_resource(FuelTypes,"/fuel_types")
api_routes.add_resource(EmissionClasses,"/emission_classes")
api_routes.add_resource(FeaturesCategories,"/features_categories")
api_routes.add_resource(Features,"/features")
api_routes.add_resource(EnumResource, '/enums/<string:enum_name>')
api_routes.add_resource(Favorites, '/favorites')
api_routes.add_resource(Reviews, '/reviews')
api_routes.add_resource(Messages, '/messages')
api_routes.add_resource(CarImages, "/cars/images/<int:car_id>")  
api_routes.add_resource(CarPrimaryImage, "/cars/primary_image/<int:car_id>")




if __name__ == '__main__':

    api.run(host='0.0.0.0', port=5000)