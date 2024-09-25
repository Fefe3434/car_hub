from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.data.model_db.db_cars_hub import EmissionClass
from app.data.models.emission_class import EmissionClasseModel, EmissionClasseResponseModel



class EmissionClasses(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='EmissionClasses')
        self.session = self.db_connection.get_session(service='EmissionClasses')
        self.emission_class_id = request.args.get('emission_class_id')
        self.data = request.data
        self.strategy = EmissionClasseResponseModel(EmissionClasseModel())

    def _request(self):
        if self.emission_class_id:
            return self.session.query(EmissionClass).filter(EmissionClass.emission_class_id == self.emission_class_id).first()
        else:
            return self.session.query(EmissionClass).all()

    def check_id(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if request.args and 'emission_class_id' not in request.args:
                return {'Error': 'Invalid argument provided'}, HTTPStatus.BAD_REQUEST
            if not self.emission_class_id:
                return {'Error': 'emission_class_id is required and must have a value.'}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper

    def get(self):
        valid_args = {'emission_class_id'}

        if any(arg not in valid_args for arg in request.args):
            return {'Error': 'Invalid argument provided'}, HTTPStatus.BAD_REQUEST

        try:
            emission_class = self._request()
            if not emission_class:
                return {'Error': 'emission_class not found'}, HTTPStatus.NOT_FOUND
            emission_class = self.strategy.compose(emission_class)
            return emission_class, HTTPStatus.OK
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
