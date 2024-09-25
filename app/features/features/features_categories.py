from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.data.model_db.db_cars_hub import EmissionClass, FeatureCategory
from app.data.models.emission_class import EmissionClasseModel, EmissionClasseResponseModel
from app.data.models.features_categories import FeaturesCategoriesModel, FeaturesCategoriesResponseModel



class FeaturesCategories(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='FeaturesCategories')
        self.session = self.db_connection.get_session(service='FeaturesCategories')
        self.category_id = request.args.get('category_id')
        self.data = request.data
        self.strategy = FeaturesCategoriesResponseModel(FeaturesCategoriesModel())

    def _request(self):
        if self.category_id:
            return self.session.query(FeatureCategory).filter(FeatureCategory.category_id == self.category_id).first()
        else:
            return self.session.query(FeatureCategory).all()

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
            category = self._request()
            if not category:
                return {'Error': 'category not found'}, HTTPStatus.NOT_FOUND
            categories = self.strategy.compose(category)
            return categories, HTTPStatus.OK
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
