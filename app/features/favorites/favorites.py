from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.data.model_db.db_cars_hub import Car, Favorite
from app.data.models.favorites import FavoritesModel, FavoritesResponseModel
from app.shared.user_info.user_info import UserInfo

class Favorites(Resource):
    REQUIRED_FIELDS = ['car_id']

    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='Favorites')
        self.session = self.db_connection.get_session(service='Favorites')
        self.favorite_id = request.args.get('favorite_id')
        self.data = request.data
        self.strategy = FavoritesResponseModel(FavoritesModel())
        self.current_user = UserInfo(self.session).get_user


    def validate_data(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            missing_fields = [field for field in self.REQUIRED_FIELDS if field not in self.data]
            if missing_fields:
                return {'Error': f'Missing required fields: {", ".join(missing_fields)}'}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper
    
    def get(self):
        try:
            user_id = self.current_user.user_id

            favorites = self.session.query(Favorite).filter(Favorite.user_id == user_id).all()

            if not favorites:
                return {'message': 'No favorites found'}, HTTPStatus.NOT_FOUND

            favorites_list = [self.strategy.compose(fav) for fav in favorites]

            return favorites_list, HTTPStatus.OK

        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @validate_data
    def post(self):
        try:
            car_id = self.data.get('car_id')
            user_id = self.current_user.user_id  

            car = self.session.query(Car).filter(Car.car_id == car_id).first()
            if not car:
                return {'Error': 'Car not found'}, HTTPStatus.NOT_FOUND

            existing_favorite = self.session.query(Favorite).filter_by(user_id=user_id, car_id=car_id).first()
            if existing_favorite:
                return {'Error': 'Car is already in favorites'}, HTTPStatus.CONFLICT

            new_favorite = Favorite(user_id=user_id, car_id=car_id)
            self.session.add(new_favorite)
            self.session.commit()

            return {'Success': 'Car added to favorites'}, HTTPStatus.CREATED

        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    @validate_data
    def delete(self):
        try:
            car_id = self.data.get('car_id')
            user_id = self.current_user.user_id

            favorite = self.session.query(Favorite).filter_by(user_id=user_id, car_id=car_id).first()
            if not favorite:
                return {'Error': 'Favorite not found'}, HTTPStatus.NOT_FOUND

            self.session.delete(favorite)
            self.session.commit()

            return {'Success': 'Car removed from favorites'}, HTTPStatus.OK

        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR