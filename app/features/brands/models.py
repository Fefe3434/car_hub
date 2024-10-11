from http import HTTPStatus
from flask import request
from flask_restful import Resource
from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.data.models.models import ModelsModel, ModelsResponseModel
from app.data.model_db.db_cars_hub import Model, BrandModelMap


class Models(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='Models')
        self.session = self.db_connection.get_session(service='Models')
        self.model_id = request.args.get('model_id')
        self.brand_id = request.args.get('brand_id')  # New: Retrieve brand_id from query params
        self.data = request.data
        self.strategy = ModelsResponseModel(ModelsModel())

    def _request(self):
        # If model_id is provided, fetch specific model
        if self.model_id:
            return self.session.query(Model).filter(Model.model_id == self.model_id).first()
        # If brand_id is provided, fetch models associated with the brand
        elif self.brand_id:
            return (
                self.session.query(Model)
                .join(BrandModelMap, BrandModelMap.model_id == Model.model_id)
                .filter(BrandModelMap.brand_id == self.brand_id)
                .all()
            )
        else:
            # Otherwise, return all models
            return self.session.query(Model).all()

    def get(self):
        valid_args = {'model_id', 'brand_id'}

        # Validate query parameters
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
