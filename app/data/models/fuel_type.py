import json

from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy


class FuelTypeResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model):
        super().__init__(model)

    def compose(self, response_body: json):
        return super().compose(response_body)


class FuelTypeModel:
    def __init__(self) -> None:
        self.fuel_type_id = None
        self.fuel_type_name = None


