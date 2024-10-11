from http import HTTPStatus
from sqlalchemy import and_
from app.data.model_db.db_cars_hub import Car, CarFeatureMap
from datetime import datetime


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

        if 'min_price' in self.query_params:
            filters.append(Car.price >= float(self.query_params['min_price']))
        if 'max_price' in self.query_params:
            filters.append(Car.price <= float(self.query_params['max_price']))

        if 'min_mileage' in self.query_params:
            filters.append(Car.mileage >= int(self.query_params['min_mileage']))
        if 'max_mileage' in self.query_params:
            filters.append(Car.mileage <= int(self.query_params['max_mileage']))

        if 'fuel_type_id' in self.query_params:
            fuel_type_id = int(self.query_params['fuel_type_id'])
            print(f"Applying fuel type filter: {fuel_type_id}")
            filters.append(Car.fuel_type_id == fuel_type_id)

        if 'emission_class_ids' in self.query_params:
            emission_class_ids = self.query_params['emission_class_ids'].split(',')
            filters.append(Car.emission_class_id.in_(emission_class_ids))

        if 'transmission' in self.query_params:
            filters.append(Car.transmission == self.query_params['transmission'])

        if 'location' in self.query_params:
            filters.append(Car.location.ilike(f"%{self.query_params['location']}%"))


        if 'min_power' in self.query_params:
            filters.append(Car.power >= int(self.query_params['min_power']))

        if 'max_power' in self.query_params:
            filters.append(Car.power <= int(self.query_params['max_power']))


        if 'features' in self.query_params and self.query_params['features']:
            feature_ids = self.query_params['features'].split(',')
            query = query.join(CarFeatureMap).filter(CarFeatureMap.feature_id.in_(feature_ids))


        if 'min_year' in self.query_params or 'max_year' in self.query_params:
            min_year = self.query_params.get('min_year', '1900')  
            max_year = self.query_params.get('max_year', str(datetime.now().year))  

            try:
                filters.append(
                    Car.first_immatriculation.between(f"{min_year}-01-01", f"{max_year}-12-31")
                )
            except ValueError:
                return {'Error': 'Invalid year format for min_year or max_year'}, HTTPStatus.BAD_REQUEST
        
        print("Query Params:", self.query_params)
        if not filters:
            return query.all()

        return query.filter(and_(*filters)).all()
