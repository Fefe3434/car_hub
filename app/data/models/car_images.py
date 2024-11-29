import json
from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy

class CarImagesResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model):
        super().__init__(model)

    def compose(self, response_body: json):
        return super().compose(response_body)


class CarImagesModel:
    def __init__(self) -> None:
        self.image_id = None
        self.image_url = None
