import json

from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy


class FeaturesCategoriesResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model):
        super().__init__(model)

    def compose(self, response_body: json):
        return super().compose(response_body)


class FeaturesCategoriesModel:
    def __init__(self) -> None:
        self.category_id = None
        self.category_name = None


