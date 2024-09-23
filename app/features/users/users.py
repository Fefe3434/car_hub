from http import HTTPStatus
from flask import request
from flask_restful import Resource
from app.data.model_db.db_cars_hub import User
from app.data.models.user import UserModel, UserResponseModel
from app.shared.user_info.user_info import UserInfo
from app.utils.database.db_connexion import DbConnexion as DBConnection
from dotenv import load_dotenv

from app.shared.password.password import Password
from app.utils.decorator.try_catch_decorator import try_catch_decorator

load_dotenv()

class Users(Resource):
    ARGUMENTS = ['user_id']
    ALLOWED_FIELDS_NO_ADMIN = ['password']
    ALLOWED_FIELDS_ADMIN = [
        'name',
        'email',
        'phone_number',
        'password',
        'role',
        'seller_type',
        'is_admin'
    ]

    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='Users')
        self.session = self.db_connection.get_session(service='Users')
        self.strategy = UserResponseModel(UserModel())
        self.data = request.data
        self.user_id = request.args.get('user_id')
        self.current_user = UserInfo(self.session).get_user

    def _check_arg_validity(self, allowed_arg):
        not_valid_argument = [arg for arg in request.args if arg not in allowed_arg]
        if not_valid_argument:
            raise ValueError(f"Invalid argument provided: {', '.join(not_valid_argument)}")
        not_valid_value = any(not request.args[arg] for arg in request.args)
        if not_valid_value:
            raise ValueError('No value for agument provided')
        
    def _check_required_arguments(self):
        missing_arguments = [arg for arg in self.ARGUMENTS if arg not in request.args]
        if missing_arguments:
            raise ValueError(f"Missing required arguments: {', '.join(missing_arguments)}")
        
    def _validate_request(self):
        self._check_arg_validity(self.ARGUMENTS)
        if request.method in {'PATCH', 'DELETE'}:
            self._check_required_arguments()
        if not self.current_user.is_admin:
            if request.method in {'GET', 'PATCH'}:
                if not self.user_id:
                    raise ValueError('No value for argument provided')
                if not request.args or int(self.user_id) != self.current_user.user_id:
                    raise PermissionError('Unauthorized')
            elif request.method in {'POST', 'DELETE'}:
                raise PermissionError('Unauthorized')
            
    def hash_password(self, password):
        password_obj = Password(password)
        if not password_obj.is_valid:
            raise ValueError('Invalid password')
        return password_obj.hashPassword
    
    def _request(self):
        if self.user_id:
            return self.session.query(User).filter(User.user_id == self.user_id).first()
        return self.session.query(User).all()

    def _check_required_fields(self, required_fields):
        missing_fields = [field for field in required_fields if field not in self.data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    def _remove_extra_fields(self, allowed_fields):
        extra_fields = [field for field in self.data if field not in allowed_fields]
        for field in extra_fields:
            self.data.pop(field)

    def _validate_data(self):
        if not self.current_user.is_admin:
            self._remove_extra_fields(self.ALLOWED_FIELDS_NO_ADMIN)
        else:
            if request.method == 'POST':
                self._check_required_fields(self.ALLOWED_FIELDS_ADMIN)
        self._remove_extra_fields(self.ALLOWED_FIELDS_ADMIN)

    def _update(self, data):
        for key, value in self.data.items():
            setattr(data, key, value)
        self.session.commit()
    
    @try_catch_decorator
    def get(self):
            self._validate_request()
            user = self._request()
            if not user:
                return {'Error': 'Data(s) not found'}, HTTPStatus.NOT_FOUND
            user = self.strategy.compose(user)
            return user, HTTPStatus.OK

    def post(self):
        try:
            self._validate_request()
            self._validate_data()
            self.data['password'] = self.hash_password(self.data.get('password'))
            user = User(**self.data)
            self.session.add(user)
            self.session.commit()
            return {'id_utiisateur': user.user_id}, HTTPStatus.CREATED
        except PermissionError as e:
            return {'Error': str(e)}, HTTPStatus.UNAUTHORIZED
        except ValueError as e:
            return {'Error': str(e)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def patch(self):
        try:
            self._validate_request()
            self._validate_data()
            user = self._request()
            if not user:
                return {'Error': 'User not found'}, HTTPStatus.NOT_FOUND
            if 'password' in self.data and self.data['password']:
                self.data['password'] = self.hash_password(self.data.get('password'))
            self._update(user)
            return {'id_utiisateur': user.user_id}, HTTPStatus.OK
        except PermissionError as e:
            return {'Error': str(e)}, HTTPStatus.UNAUTHORIZED
        except ValueError as e:
            return {'Error': str(e)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


    def delete(self):
        try:
            self._validate_request()
            user = self._request()
            if not user:
                return {'Error': 'User not found'}, HTTPStatus.NOT_FOUND
            self.session.delete(user)
            self.session.commit()
            return {'id_utilisateur': user.user_id}, HTTPStatus.OK
        except PermissionError as e:
            return {'Error': str(e)}, HTTPStatus.UNAUTHORIZED
        except ValueError as e:
            return {'Error': str(e)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR









