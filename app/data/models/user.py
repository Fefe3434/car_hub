import json

from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy


class UserResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model):
        super().__init__(model)

    def compose(self, response_body: json):
        return super().compose(response_body)


class UserModel:
    def __init__(self) -> None:
        self.user_id = None
        self.name = None
        self.email = None
        self.phone_humber = None
        self.role = None
        self.created_at = None
        self.seller_type = None



