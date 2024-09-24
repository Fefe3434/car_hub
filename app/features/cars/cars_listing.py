from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource
from app.data.model_db.db_cars_hub import Car, User
from app.data.models.user import UserModel, UserResponseModel
from app.shared.user_info.user_info import UserInfo
from app.utils.database.db_connexion import DbConnexion as DBConnection
from dotenv import load_dotenv

from app.shared.password.password import Password
from app.utils.decorator.try_catch_decorator import try_catch_decorator
from app.data.models.cars import CarsModel, CarsResponseModel

load_dotenv()

class CarsListing(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='CarsListing')
        self.session = self.db_connection.get_session(service='CarsListing')
        self.id = request.args.get('id')
        self.data = request.data

    def check_args(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.id:
                return {'Error': 'Id is required.'}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper

    def _filters(self):
        filters = []
        if self.id:
            filters.append((Car.car_id == self.id))
        return filters

    def _request(self):
            filters = self._filters()
            if filters:
                return self.session.query(Car).filter(*filters).first()
            else:
                return self.session.query(Car).all()
            
    def get(self):
        valid_args = {'id'}

        if any(arg not in valid_args for arg in request.args):
            return {'Error': 'Invalid argument(s) provided'}, HTTPStatus.BAD_REQUEST

        try:
            strategy = CarsResponseModel(CarsModel())
            car = self._request()
            if car is None:
                return {'Error': 'Car not found'}, HTTPStatus.NOT_FOUND
            
            cars = strategy.compose(car)
            return cars, HTTPStatus.OK
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR




