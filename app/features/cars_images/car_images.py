import os
from functools import wraps
from http import HTTPStatus
from flask import request, jsonify, current_app
from flask_restful import Resource
from werkzeug.utils import secure_filename

from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.data.model_db.db_cars_hub import Car, CarImage
from app.data.models.car_images import CarImagesResponseModel, CarImagesModel

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class CarImages(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service="CarImages")
        self.session = self.db_connection.get_session(service="CarImages")
        self.strategy = CarImagesResponseModel(CarImagesModel())  # Response strategy

        # Ensure the upload folder exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    def _get_car(self, car_id):
        """Fetch the car object based on car_id."""
        return self.session.query(Car).filter_by(car_id=car_id).first()

    def allowed_file(self, filename):
        """Check if the file extension is allowed."""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def check_car_id(func):
        """Decorator to validate the presence of `car_id`."""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            car_id = request.form.get("car_id") or kwargs.get("car_id")
            if not car_id:
                return {"Error": "`car_id` is required in the URL or form data"}, HTTPStatus.BAD_REQUEST

            car = self._get_car(car_id)
            if not car:
                return {"Error": "Car not found"}, HTTPStatus.NOT_FOUND

            return func(self, car_id=car_id, *args, **kwargs)
        return wrapper

    def check_image_upload(func):
        """Decorator to validate image upload constraints."""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if "images" not in request.files:
                return {"Error": "No images provided"}, HTTPStatus.BAD_REQUEST

            files = request.files.getlist("images")
            if len(files) > 5:
                return {"Error": "You can upload up to 5 images only"}, HTTPStatus.BAD_REQUEST

            for file in files:
                if not self.allowed_file(file.filename):
                    return {"Error": f"Invalid file type: {file.filename}"}, HTTPStatus.BAD_REQUEST

            return func(self, *args, **kwargs)
        return wrapper

    @check_car_id
    @check_image_upload
    def post(self, car_id):
        """Handle image uploads for a car."""
        try:
            files = request.files.getlist("images")
            image_urls = []

            for file in files:
                # Generate a secure filename and save the file
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)

                # Generate the URL for the uploaded file
                image_url = f"{request.host_url}{UPLOAD_FOLDER}/{filename}".replace("\\", "/")

                # Save the file URL in the database
                image = CarImage(car_id=car_id, image_url=image_url)
                self.session.add(image)
                image_urls.append(self.strategy.compose(image))

            self.session.commit()
            return {"Success": "Images uploaded successfully", "images": image_urls}, HTTPStatus.CREATED

        except Exception as e:
            return {"Error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get(self, car_id):
        """Fetch images for a specific car."""
        try:
            images = self.session.query(CarImage).filter_by(car_id=car_id).all()
            if not images:
                return {"Error": "No images found for this car."}, HTTPStatus.NOT_FOUND

            images_data = [{"image_id": image.image_id, "image_url": image.image_url} for image in images]
            return {"car_id": car_id, "images": images_data}, HTTPStatus.OK
        except Exception as e:
            return {"Error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
