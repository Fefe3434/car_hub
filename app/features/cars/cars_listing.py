from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource
from app.data.model_db.db_cars_hub import Car
from app.utils.database.db_connexion import DbConnexion as DBConnection
from dotenv import load_dotenv

from app.data.models.cars import CarsModel, CarsResponseModel
from app.features.cars.cars_filters import CarsFilter

load_dotenv()

class CarsListing(Resource):
    REQUIRED_FIELDS = ['user_id', 'brand_id', 'model_id', 'price', 'mileage', 'transmission',
                       'location', 'first_immatriculation', 'fuel_type_id', 'power', 'description',
                       'engine_type', 'image_url', 'emission_class_id', 'announcement_title','latitude','longitude','first_immatriculation']


    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='CarsListing')
        self.session = self.db_connection.get_session(service='CarsListing')
        self.id = request.args.get('id')
        self.query_params = request.args
        self.data = request.data

    def check_args(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.id:
                return {'Error': 'Id is required.'}, HTTPStatus.BAD_REQUEST
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
                if not any(field in self.data for field in self.REQUIRED_FIELDS):
                    return {'Error': 'At least one field must be provided for patch'}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper


    def _filters(self):
        filters = []
        if self.id:
            filters.append((Car.car_id == self.id))
        return filters

    def _request(self):
        # If an ID is provided, look for a single car by ID
        if self.id:
            return self.session.query(Car).filter(Car.car_id == self.id).first()

        # Otherwise, apply filters using the CarsFilter class
        filter_service = CarsFilter(self.session, self.query_params)
        return filter_service.apply_filters()
            
    def get(self):
        try:
            strategy = CarsResponseModel(CarsModel())
            cars = self._request()

            if cars is None:
                return {'Error': 'Car not found'}, HTTPStatus.NOT_FOUND

            if isinstance(cars, Car):
                car_data = strategy.compose(cars)
                return car_data, HTTPStatus.OK

            car_list = [strategy.compose(car) for car in cars]
            return car_list, HTTPStatus.OK

        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @validate_data
    @validate_required_fields
    def post(self):
        try:
            validated_data = self.validate_fields(self.data, self.REQUIRED_FIELDS)
            car = Car(**validated_data)
            self.session.add(car)
            self.session.flush()
            car_id = car.car_id
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
            return self._decompose_patch(car)
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def _decompose_patch(self, car):
        for key, value in self.data.items():
            if key != 'id':
                setattr(car, key, value)
        self.session.commit()
        return {'Success': "car updated", 'id': self.id}, HTTPStatus.OK

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
