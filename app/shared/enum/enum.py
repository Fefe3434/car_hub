from flask_restful import Resource
from http import HTTPStatus
from app.data.model_db.db_cars_hub import TransmissionEnum, SellerTypeEnum, RoleEnum

# Dictionary to map URL parameters to Enum classes
ENUM_CLASSES = {
    'transmission': TransmissionEnum,
    'seller_type': SellerTypeEnum,
    'role': RoleEnum,
}

class EnumResource(Resource):
    def get(self, enum_name):
        try:
            if enum_name not in ENUM_CLASSES:
                return {'Error': f"Enum {enum_name} not found"}, HTTPStatus.NOT_FOUND

            enum_class = ENUM_CLASSES[enum_name]
            enum_values = [e.value for e in enum_class]

            return {enum_name: enum_values}, HTTPStatus.OK
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
