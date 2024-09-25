import json

from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy


class ModelsResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model):
        super().__init__(model)

    def compose(self, response_body: json):
        return super().compose(response_body)


class ModelsModel:
    def __init__(self) -> None:
        self.model_id = None
        self.model_name = None


