from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.data.model_db.db_cars_hub import FuelType
from app.data.models.fuel_type import FuelTypeModel, FuelTypeResponseModel



class FuelTypes(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='FuelTypes')
        self.session = self.db_connection.get_session(service='FuelTypes')
        self.fuel_type_id = request.args.get('fuel_type_id')
        self.data = request.data
        self.strategy = FuelTypeResponseModel(FuelTypeModel())

    def _request(self):
        if self.fuel_type_id:
            return self.session.query(FuelType).filter(FuelType.fuel_type_id == self.fuel_type_id).first()
        else:
            return self.session.query(FuelType).all()

    def check_id(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if request.args and 'fuel_type_id' not in request.args:
                return {'Error': 'Invalid argument provided'}, HTTPStatus.BAD_REQUEST
            if not self.fuel_type_id:
                return {'Error': 'fuel_type_id is required and must have a value.'}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper

    def get(self):
        valid_args = {'fuel_type_id'}

        if any(arg not in valid_args for arg in request.args):
            return {'Error': 'Invalid argument provided'}, HTTPStatus.BAD_REQUEST

        try:
            fuel_type = self._request()
            if not fuel_type:
                return {'Error': 'fuel_type not found'}, HTTPStatus.NOT_FOUND
            fuel_types = self.strategy.compose(fuel_type)
            return fuel_types, HTTPStatus.OK
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
