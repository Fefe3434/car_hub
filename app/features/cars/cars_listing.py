from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource
from app.data.model_db.db_cars_hub import Car, CarFeatureMap, CarImage, Feature
from app.utils.database.db_connexion import DbConnexion as DBConnection
from dotenv import load_dotenv

from app.data.models.cars import CarsModel, CarsResponseModel
from app.features.cars.cars_filters import CarsFilter
from app.shared.user_info.user_info import UserInfo

load_dotenv()

ALLOWED_FILTERS = {'id', 'min_power', 'emission_class_ids', 'max_power', 'brand_id', 
                   'model_id', 'min_price', 'max_price', 'min_mileage', 'max_mileage', 
                   'fuel_type_id', 'transmission', 'location', 
                   'features', 'min_year', 'max_year'}


class CarsListing(Resource):
    REQUIRED_FIELDS = ['brand_id', 'model_id', 'price', 'mileage', 'transmission',
                       'location', 'first_immatriculation', 'fuel_type_id', 'power', 'description',
                       'engine_type', 'image_url', 'emission_class_id', 'announcement_title','latitude','longitude','first_immatriculation']


    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='CarsListing')
        self.session = self.db_connection.get_session(service='CarsListing')
        self.id = request.args.get('id')
        self.query_params = request.args
        self.data = request.data
        self.current_user = UserInfo(self.session).get_user

    def check_args(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.id:
                return {'Error': 'Id is required.'}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper
    
    def check_args_get(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not request.args:
                return func(self, *args, **kwargs)

            invalid_filters = [arg for arg in request.args if arg not in ALLOWED_FILTERS]
            if invalid_filters:
                return {'Error': f"Invalid filter(s) provided: {', '.join(invalid_filters)}"}, HTTPStatus.BAD_REQUEST

            return func(self, *args, **kwargs)
        return wrapper
    
    def validate_data(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.data:
                return {'Error': 'No data provided'}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper
    
    def validate_required_fields(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if isinstance(self.data, dict):
                missing_fields = [field for field in self.REQUIRED_FIELDS if field not in self.data]
                if missing_fields:
                    return {'Error': 'Missing required fields: ' + ', '.join(missing_fields)}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper
    
    def validate_fields(self, data, required_fields):
        validated_data = {}
        for field in required_fields:
            if field in data:
                validated_data[field] = data[field]
        return validated_data
    
    def validate_partial_fields(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if isinstance(self.data, dict):
                if not any(field in self.data for field in self.REQUIRED_FIELDS) and 'features' not in self.data:
                    return {'Error': 'At least one field must be provided for patch'}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper

    def _filters(self):
        filters = []
        if self.id:
            filters.append((Car.car_id == self.id))
        return filters

    def _request(self):
        if self.id:
            return self.session.query(Car).filter(Car.car_id == self.id).first()
        
        # if not self.query_params:
        #     return self.session.query(Car).all()

        filter_service = CarsFilter(self.session, self.query_params)
        return filter_service.apply_filters()
            

    @check_args_get        
    def get(self, id=None):
        """
        Fetch a specific car if 'id' is provided; otherwise, fetch all cars.
        """
        try:
            # If 'id' is provided by the route, assign it to self.id
            if id is not None:
                self.id = id

            strategy = CarsResponseModel(CarsModel())
            cars = self._request()

            if cars is None:
                return {'Error': 'Car not found'}, HTTPStatus.NOT_FOUND

            if isinstance(cars, Car):  # Single car
                features = self._get_features(cars.car_id)
                car_data = strategy.compose(cars, features)
                car_data["primary_image_url"] = self._get_primary_image(cars.car_id)  
                return car_data, HTTPStatus.OK

            # Multiple cars
            car_list = []
            for car in cars:
                features = self._get_features(car.car_id)
                car_data = strategy.compose(car, features)
                car_data["primary_image_url"] = self._get_primary_image(car.car_id)  
                car_list.append(car_data)
            
            return car_list, HTTPStatus.OK

        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    def _get_features(self, car_id):
        features_query = (
            self.session.query(Feature.feature_name)
            .join(CarFeatureMap, Feature.feature_id == CarFeatureMap.feature_id)
            .filter(CarFeatureMap.car_id == car_id)
        )
        return [feature.feature_name for feature in features_query]
    
    def _get_primary_image(self, car_id):
        """
        Fetch the primary image URL for a car.
        """
        primary_image = (
            self.session.query(CarImage)
            .filter(CarImage.car_id == car_id, CarImage.image_id == Car.primary_image_id)
            .first()
        )
        return primary_image.image_url if primary_image else None


    @validate_data
    @validate_required_fields
    def post(self):
        try:
            if not self.current_user or not self.current_user.user_id:
                return {'Error': 'User not authenticated or invalid token'}, HTTPStatus.UNAUTHORIZED
            
            self.data['user_id'] = self.current_user.user_id
            
            validated_data = self.validate_fields(self.data, self.REQUIRED_FIELDS + ['user_id'])

            car = Car(**validated_data)
            self.session.add(car)
            self.session.flush()

            car_id = car.car_id
            
            if 'features' in self.data:
                feature_ids = self.data['features']
                for feature_id in feature_ids:
                    car_feature_map = CarFeatureMap(car_id=car_id, feature_id=feature_id)
                    self.session.add(car_feature_map)

            self.session.commit()
            
            return {'Success': 'Car created', 'id': car_id}, HTTPStatus.CREATED        
        except Exception as e:
            print(e)
            return {'Error': 'Data error'}, HTTPStatus.INTERNAL_SERVER_ERROR


    @check_args
    @validate_data
    @validate_partial_fields
    def patch(self):
        try:
            car = self._request()
            if not car:
                return {'Error': 'Car not found'}, HTTPStatus.NOT_FOUND

            for key, value in self.data.items():
                if key != 'features': 
                    setattr(car, key, value)

            if 'features' in self.data:
                self._update_car_features(car.car_id, self.data['features'])

            self.session.commit()
            return {'Success': "Car updated", 'id': self.id}, HTTPStatus.OK
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def _update_car_features(self, car_id, new_features):
        self.session.query(CarFeatureMap).filter(CarFeatureMap.car_id == car_id).delete()

        for feature_id in new_features:
            car_feature_map = CarFeatureMap(car_id=car_id, feature_id=feature_id)
            self.session.add(car_feature_map)

        self.session.flush()

    @check_args
    @validate_data
    @validate_required_fields
    def put(self):
        try:
            car = self._request()
            if not car:
                return {'Error': 'car not found'}, HTTPStatus.NOT_FOUND

            validated_data = self.validate_fields(self.data, self.REQUIRED_FIELDS)
            for key, value in validated_data.items():
                setattr(car, key, value)
            self.session.commit()
            return {'Success': 'car updated', 'id': self.id}, HTTPStatus.OK
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @check_args
    def delete(self):
        try:
            car = self._request()
            if not car:
                return {'Error': 'car not found'}, HTTPStatus.NOT_FOUND
            self.session.delete(car)
            self.session.commit()
            return {'Success': "car deleted", 'id': self.id}, HTTPStatus.OK
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
