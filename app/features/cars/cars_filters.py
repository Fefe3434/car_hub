from sqlalchemy import and_
from app.data.model_db.db_cars_hub import Car

class CarsFilter:
    def __init__(self, session, query_params):
        self.session = session
        self.query_params = query_params

    def apply_filters(self):
        query = self.session.query(Car)
        filters = []

        if 'brand_id' in self.query_params:
            filters.append(Car.brand_id == self.query_params['brand_id'])

        if 'model_id' in self.query_params:
            filters.append(Car.model_id == self.query_params['model_id'])

        if 'min_price' in self.query_params and 'max_price' in self.query_params:
            filters.append(Car.price.between(self.query_params['min_price'], self.query_params['max_price']))

        if 'min_mileage' in self.query_params and 'max_mileage' in self.query_params:
            filters.append(Car.mileage.between(self.query_params['min_mileage'], self.query_params['max_mileage']))

        if 'fuel_type_id' in self.query_params:
            filters.append(Car.fuel_type_id == self.query_params['fuel_type_id'])

        if 'transmission' in self.query_params:
            filters.append(Car.transmission == self.query_params['transmission'])

        if 'location' in self.query_params:
            filters.append(Car.location.ilike(f"%{self.query_params['location']}%"))

        if 'emission_class_id' in self.query_params:
            filters.append(Car.emission_class_id == self.query_params['emission_class_id'])

        if not filters:
            return query.all()

        return query.filter(and_(*filters)).all()
