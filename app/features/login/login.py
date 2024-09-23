from http import HTTPStatus
from flask import request,make_response
from flask_restful import Resource
from app.data.models.login import LoginResponseModel, LoginModel
from app.data.model_db.db_cars_hub import User
from app.shared.password.password import Password
from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.utils.token.token import Token


class Login(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='Login')
        self.data = request.data

    def post(self):
        try:
            strategy = LoginResponseModel(LoginModel())
            data = self._tri_data_received()
            session = self.db_connection.get_session(service='Login')

            requete = session.query(User).filter_by(**data).first()
            data_user = {}

            if requete is None:
                return {'message': 'User not found. Please create an account by setting a password.'}, HTTPStatus.NOT_FOUND


            if(requete is not None):
                data_user = strategy.compose(requete)
                
                return self._get_authenticate(data['email'], data_user)
                        
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.BAD_REQUEST
    
    def _tri_data_received(self):
        try:
            data = self.data
            required_fields = ['email', 'password']

            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return {'Error': 'login error'}, HTTPStatus.BAD_REQUEST
            
            passwrd = Password(data['password'])
            data['password'] = passwrd.hashPassword

            return data
        
        except Exception as e:
            return {'Error': 'login error'}, HTTPStatus.BAD_REQUEST
    
    def _get_token(self, user):
        return Token().create_token(user)

    def _get_authenticate(self, user, data):
        token = self._get_token(user)
        data['Authorization'] = 'Bearer ' + str(token)
        response = make_response(data, HTTPStatus.ACCEPTED)
        #response.headers['Authorization'] = 'Bearer ' + str(token)

        return response


