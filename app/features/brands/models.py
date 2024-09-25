from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.data.models.models import ModelsModel, ModelsResponseModel
from app.data.model_db.db_cars_hub import Model



class Models(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='Models')
        self.session = self.db_connection.get_session(service='Models')
        self.model_id = request.args.get('model_id')
        self.data = request.data
        self.strategy = ModelsResponseModel(ModelsModel())

    def _request(self):
        if self.model_id:
            return self.session.query(Model).filter(Model.model_id == self.model_id).first()
        else:
            return self.session.query(Model).all()

    def check_id(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if request.args and 'model_id' not in request.args:
                return {'Error': 'Invalid argument provided'}, HTTPStatus.BAD_REQUEST
            if not self.model_id:
                return {'Error': 'model_id is required and must have a value.'}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper

    def get(self):
        valid_args = {'model_id'}

        if any(arg not in valid_args for arg in request.args):
            return {'Error': 'Invalid argument provided'}, HTTPStatus.BAD_REQUEST

        try:
            model = self._request()
            if not model:
                return {'Error': 'model not found'}, HTTPStatus.NOT_FOUND
            models = self.strategy.compose(model)
            return models, HTTPStatus.OK
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
