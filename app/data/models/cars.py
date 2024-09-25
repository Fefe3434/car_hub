import json
from typing import List

from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy
from app.data.model_db.db_cars_hub import Car


class CarsResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model):
        super().__init__(model)

    def compose(self, response_body: Car):
        return {
            'car_id': response_body.car_id,
            'brand': response_body.brand.brand_name,  
            'model': response_body.model.model_name,
            'price': str(response_body.price),
            'mileage': response_body.mileage,
            'fuel_type': response_body.fuel_type.fuel_type_name,
            'description': response_body.description,
            'engine_type': response_body.engine_type,
            'transmission': response_body.transmission.value, 
            'location': response_body.location,
            'image_url': response_body.image_url,
            'power': response_body.power,
            'latitude': str(response_body.latitude),
            'longitude': str(response_body.longitude),
            'emission_class': response_body.emission_class.emission_class_name if response_body.emission_class else None, 
            'announcement_title': response_body.announcement_title,
            'first_immatriculation': response_body.first_immatriculation.strftime('%Y-%m-%d')  
        }


class CarsModel:
    def __init__(self) -> None:
        self.car_id = None
        self.brand = None
        self.model = None
        self.price = None
        self.mileage = None
        self.fuel_type = None
        self.description = None
        self.engine_type = None
        self.transmission = None
        self.location = None
        self.image_url = None
        self.power = None
        self.latitude = None
        self.longitude = None
        self.emission_class = None
        self.announcement_title = None
        self.first_immatriculation = None 

