from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.data.model_db.db_cars_hub import Car, CarImage


class CarPrimaryImage(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service="CarPrimaryImage")
        self.session = self.db_connection.get_session(service="CarPrimaryImage")
        self.car_id = request.view_args.get("car_id")  # Fetch `car_id` from the URL

    def _get_car(self):
        """Fetch the car object based on car_id."""
        return self.session.query(Car).filter_by(car_id=self.car_id).first()

    def _get_image(self, image_id):
        """Fetch the image object based on image_id."""
        return self.session.query(CarImage).filter_by(image_id=image_id, car_id=self.car_id).first()

    def check_car_id(func):
        """Decorator to validate the presence of `car_id`."""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.car_id:
                return {"Error": "`car_id` is required in the URL"}, HTTPStatus.BAD_REQUEST

            car = self._get_car()
            if not car:
                return {"Error": "Car not found"}, HTTPStatus.NOT_FOUND

            return func(self, *args, **kwargs)
        return wrapper

    def check_primary_image_data(func):
        """Decorator to validate primary image data."""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            data = request.get_json()
            if not data or "image_id" not in data:
                return {"Error": "`image_id` is required in the request body"}, HTTPStatus.BAD_REQUEST

            image = self._get_image(data["image_id"])
            if not image:
                return {"Error": "Image not found for this car"}, HTTPStatus.NOT_FOUND

            return func(self, *args, **kwargs)
        return wrapper


    def get(self, car_id):
        """Fetch the primary image for a specific car."""
        try:
            car = self.session.query(Car).filter_by(car_id=car_id).first()
            if not car or not car.primary_image_id:
                return {"Error": "Primary image not found for this car."}, HTTPStatus.NOT_FOUND

            primary_image = self.session.query(CarImage).filter_by(image_id=car.primary_image_id).first()
            return {"car_id": car_id, "primary_image_url": primary_image.image_url}, HTTPStatus.OK
        except Exception as e:
            return {"Error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
        
        
    @check_car_id
    @check_primary_image_data
    def patch(self):
        """Set a primary image for the car."""
        try:
            data = request.get_json()
            car = self._get_car()

            # Update the primary image ID
            car.primary_image_id = data["image_id"]
            self.session.commit()

            return {"Success": "Primary image set successfully"}, HTTPStatus.OK

        except Exception as e:
            return {"Error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
