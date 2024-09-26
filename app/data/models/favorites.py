from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy


class FavoritesResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model):
        super().__init__(model)

    def compose(self, response_body):
        return {
            'favorite_id': response_body.favorite_id,
            'user_id': response_body.user_id,
            'car': {
                'car_id': response_body.car.car_id,
                'brand': response_body.car.brand.brand_name,
                'model': response_body.car.model.model_name,
                'price': str(response_body.car.price),
                'mileage': response_body.car.mileage,
                'transmission': response_body.car.transmission.value,
                'location': response_body.car.location,
                'image_url': response_body.car.image_url,
                'power': response_body.car.power,
                'first_immatriculation': response_body.car.first_immatriculation.strftime('%Y-%m-%d'),
                'fuel_type': response_body.car.fuel_type.fuel_type_name,
                'emission_class': response_body.car.emission_class.emission_class_name if response_body.car.emission_class else None
            },
            'added_at': response_body.created_at.strftime('%Y-%m-%d %H:%M:%S') if response_body.created_at else None
        }


class FavoritesModel:
    def __init__(self) -> None:
        self.favorite_id = None
        self.user_id = None
        self.car_id = None
        self.created_at = None
        self.car = None  

