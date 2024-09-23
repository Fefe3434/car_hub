from http import HTTPStatus
from flask import request
from flask_restful import Resource
from app.data.model_db.db_cars_hub import User
from app.shared.password.password import Password
from app.utils.database.db_connexion import DbConnexion as DBConnection


class Register(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='Register')
        self.user_id = request.args.get('user_id')
        self.data = request.get_json()  

    def post(self):
        try:
            if not self.data:
                return {'Error': 'Request data is empty'}, HTTPStatus.BAD_REQUEST

            data = self.data
            name = data.get('name')
            phone_number = data.get('phone_number')
            role = data.get('role', 'buyer')  
            seller_type = data.get('seller_type', 'particulier')  
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            if not name or not phone_number or not role or not seller_type or not email or not password or not confirm_password:
                return {'Error': 'All fields (name, phone_number, role, seller_type, email, password, confirm_password) are required'}, HTTPStatus.BAD_REQUEST

            if password != confirm_password:
                return {'Error': 'Passwords do not match'}, HTTPStatus.BAD_REQUEST

            session = self.db_connection.get_session(service='Register')
            user = session.query(User).filter_by(email=email).first()
            if user:
                return {'Error': 'User already exists, please login'}, HTTPStatus.CONFLICT

            hashed_password = Password(password).hashPassword

            new_user = User(
                name=name,
                email=email,
                password=hashed_password,
                phone_number=phone_number,
                role=role,
                seller_type=seller_type,
                isadmin=0  
            )
            session.add(new_user)
            session.commit()

            return {'Message': 'Account created successfully, you can now log in.'}, HTTPStatus.CREATED

        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.BAD_REQUEST