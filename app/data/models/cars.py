import json
from typing import List

from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy


class CarsResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model):
        super().__init__(model)

    def compose(self, response_body: json):
        return super().compose(response_body)


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


