from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.data.model_db.db_cars_hub import Message, User, Car
from app.shared.user_info.user_info import UserInfo
from app.data.models.messages import MessageModel, MessageResponseModel


class Messages(Resource):
    REQUIRED_FIELDS = ['receiver_id', 'message_body']

    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='Messages')
        self.session = self.db_connection.get_session(service='Messages')
        self.message_id = request.args.get('message_id')
        self.receiver_id = request.args.get('receiver_id')
        self.data = request.json
        self.strategy = MessageResponseModel(MessageModel(), self.session)
        self.current_user = UserInfo(self.session).get_user

    def validate_data(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            missing_fields = [field for field in self.REQUIRED_FIELDS if field not in self.data]
            if missing_fields:
                return {'Error': f'Missing required fields: {", ".join(missing_fields)}'}, HTTPStatus.BAD_REQUEST
            return func(self, *args, **kwargs)
        return wrapper

    def validate_ownership(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            message = self.session.query(Message).filter_by(message_id=self.message_id).first()
            if not message:
                return {'Error': 'Message not found'}, HTTPStatus.NOT_FOUND
            if message.sender_id != self.current_user.user_id:
                return {'Error': 'Unauthorized: You can only modify your own messages'}, HTTPStatus.UNAUTHORIZED
            return func(self, *args, **kwargs)
        return wrapper

    def get(self):
        try:
            user_id = self.current_user.user_id
            messages = self.session.query(Message).filter(
                (Message.sender_id == user_id) | (Message.receiver_id == user_id)
            ).all()

            if not messages:
                return {'message': 'No messages found'}, HTTPStatus.NOT_FOUND

            messages_list = [self.strategy.compose(message) for message in messages]

            return messages_list, HTTPStatus.OK

        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @validate_data
    def post(self):
        try:
            sender_id = self.current_user.user_id
            receiver_id = self.data.get('receiver_id')
            message_body = self.data.get('message_body')
            car_id = self.data.get('car_id')

            if not self.session.query(User).filter(User.user_id == receiver_id).first():
                return {'Error': 'Receiver not found'}, HTTPStatus.NOT_FOUND

            # Create a new message
            new_message = Message(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message_body=message_body,
                car_id=car_id
            )

            self.session.add(new_message)
            self.session.commit()

            return {'Success': 'Message sent', 'message_id': new_message.message_id}, HTTPStatus.CREATED

        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    # @validate_ownership
    # def patch(self):
    #     try:
    #         message = self.session.query(Message).filter_by(message_id=self.message_id, sender_id=self.current_user.user_id).first()
    #         if not message:
    #             return {'Error': 'Message not found or unauthorized'}, HTTPStatus.NOT_FOUND

    #         if 'message_body' in self.data:
    #             message.message_body = self.data['message_body']

    #         self.session.commit()
    #         return {'Success': 'Message updated', 'message_id': message.message_id}, HTTPStatus.OK
    #     except Exception as e:
    #         self.session.rollback()
    #         return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @validate_ownership
    def delete(self):
        try:
            message = self.session.query(Message).filter_by(message_id=self.message_id, sender_id=self.current_user.user_id).first()
            if not message:
                return {'Error': 'Message not found or unauthorized'}, HTTPStatus.NOT_FOUND

            self.session.delete(message)
            self.session.commit()

            return {'Success': 'Message deleted'}, HTTPStatus.OK
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
