from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.data.model_db.db_cars_hub import Feature
from app.data.models.features import FeaturesModel, FeaturesResponseModel



class Features(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='Features')
        self.session = self.db_connection.get_session(service='Features')
        self.category_id = request.args.get('category_id')
        self.data = request.data
        self.strategy = FeaturesResponseModel(FeaturesModel())

    def _request(self):
        if self.category_id:
            return self.session.query(Feature).filter(Feature.category_id == self.category_id).all()
        else:
            return self.session.query(Feature).all()

    def check_id(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if request.args and 'category_id' not in request.args:
                return {'Error': 'Invalid argument provided'}, HTTPStatus.BAD_REQUEST
            if not self.category_id:
                return {'Error': 'category_id is required and must have a value.'}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper

    def get(self):
        valid_args = {'category_id'}

        if any(arg not in valid_args for arg in request.args):
            return {'Error': 'Invalid argument provided'}, HTTPStatus.BAD_REQUEST

        try:
            feature = self._request()
            if not feature:
                return {'Error': 'feature not found'}, HTTPStatus.NOT_FOUND
            features = self.strategy.compose(feature)
            return features, HTTPStatus.OK
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
