import json

from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy


class EmissionClasseResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model):
        super().__init__(model)

    def compose(self, response_body: json):
        return super().compose(response_body)


class EmissionClasseModel:
    def __init__(self) -> None:
        self.emission_class_id = None
        self.emission_class_name = None


