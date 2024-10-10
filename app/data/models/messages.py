import json
from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy
from app.data.model_db.db_cars_hub import User, Car

class MessageResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model, session):
        super().__init__(model)
        self.session = session

    def compose(self, response_body: json):
        sender = self.session.query(User).filter_by(user_id=response_body.sender_id).first()
        receiver = self.session.query(User).filter_by(user_id=response_body.receiver_id).first()
        car = self.session.query(Car).filter_by(car_id=response_body.car_id).first() if response_body.car_id else None

        return {
            'message_id': response_body.message_id,
            'sender': sender.name if sender else 'Unknown',
            'receiver': receiver.name if receiver else 'Unknown',
            'message_body': response_body.message_body,
            'car': car.announcement_title if car else 'No car linked',
            'created_at': response_body.created_at.strftime('%Y-%m-%d %H:%M:%S') if response_body.created_at else None
        }

class MessageModel:
    def __init__(self) -> None:
        self.message_id = None
        self.sender = None  
        self.receiver = None  
        self.sender_id = None  
        self.receiver_id = None  
        self.message_body = None
        self.car_id = None  
        self.created_at = None
