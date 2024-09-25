import json

from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy


class FeaturesResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model):
        super().__init__(model)

    def compose(self, response_body: json):
        return super().compose(response_body)


class FeaturesModel:
    def __init__(self) -> None:
        self.feature_id = None
        self.feature_name = None


