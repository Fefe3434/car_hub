import json
from typing import List

from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy


class LoginResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model):
        super().__init__(model)

    def compose(self, response_body: json):
        return super().compose(response_body)


class LoginModel:
    def __init__(self) -> None:
        self.user_id = None
        self.name = None
        self.Authorization = None


