from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.data.models.brands import BrandsModel, BrandsResponseModel
from app.data.model_db.db_cars_hub import Brand



class Brands(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='Brands')
        self.session = self.db_connection.get_session(service='Brands')
        self.brand_id = request.args.get('brand_id')
        self.data = request.data
        self.strategy = BrandsResponseModel(BrandsModel())

    def _request(self):
        if self.brand_id:
            return self.session.query(Brand).filter(Brand.brand_id == self.brand_id).first()
        else:
            return self.session.query(Brand).all()

    def check_id(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if request.args and 'brand_id' not in request.args:
                return {'Error': 'Invalid argument provided'}, HTTPStatus.BAD_REQUEST
            if not self.brand_id:
                return {'Error': 'brand_id is required and must have a value.'}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper

    def get(self):
        valid_args = {'brand_id'}

        if any(arg not in valid_args for arg in request.args):
            return {'Error': 'Invalid argument provided'}, HTTPStatus.BAD_REQUEST

        try:
            brand = self._request()
            if not brand:
                return {'Error': 'brand not found'}, HTTPStatus.NOT_FOUND
            brands = self.strategy.compose(brand)
            return brands, HTTPStatus.OK
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
