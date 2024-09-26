from functools import wraps
from http import HTTPStatus
from flask import request
from flask_restful import Resource

from app.utils.database.db_connexion import DbConnexion as DBConnection
from app.data.model_db.db_cars_hub import Review, User
from app.shared.user_info.user_info import UserInfo
from app.data.models.reviews import ReviewModel, ReviewResponseModel


class Reviews(Resource):
    REQUIRED_FIELDS = ['reviewed_user_id', 'rating']

    def __init__(self) -> None:
        super().__init__()
        self.db_connection = DBConnection(service='Review')
        self.session = self.db_connection.get_session(service='Review')
        self.review_id = request.args.get('review_id')
        self.reviewed_user_id = request.args.get('reviewed_user_id')
        self.data = request.data
        self.strategy = ReviewResponseModel(ReviewModel(), self.session)
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
            review = self.session.query(Review).filter_by(review_id=self.review_id).first()
            if not review:
                return {'Error': 'Review not found'}, HTTPStatus.NOT_FOUND
            if review.reviewer_id != self.current_user.user_id:
                return {'Error': 'Unauthorized: You can only modify your own reviews'}, HTTPStatus.UNAUTHORIZED
            return func(self, *args, **kwargs)
        return wrapper

    def get(self):
        try:
            if self.reviewed_user_id:
                reviews = self.session.query(Review).filter_by(reviewed_user_id=self.reviewed_user_id).all()
                if not reviews:
                    return {'message': 'No reviews found for this user'}, HTTPStatus.NOT_FOUND

                reviews_list = [self.strategy.compose(review) for review in reviews]
                return reviews_list, HTTPStatus.OK

            return {'Error': 'Please provide a reviewed_user_id'}, HTTPStatus.BAD_REQUEST

        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @validate_data
    def post(self):
        try:
            reviewer_id = self.current_user.user_id
            reviewed_user_id = self.data.get('reviewed_user_id')

            if reviewer_id == reviewed_user_id:
                return {'Error': 'You cannot review yourself'}, HTTPStatus.BAD_REQUEST

            if not self.session.query(User).filter(User.user_id == reviewed_user_id).first():
                return {'Error': 'Reviewed user not found'}, HTTPStatus.NOT_FOUND

            new_review = Review(
                reviewer_id=reviewer_id,
                reviewed_user_id=reviewed_user_id,
                rating=self.data['rating'],
                review_text=self.data.get('review_text', ''),
            )
            self.session.add(new_review)
            self.session.commit()

            return {'Success': 'Review created', 'review_id': new_review.review_id}, HTTPStatus.CREATED

        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @validate_ownership
    def patch(self):
        try:
            review = self.session.query(Review).filter_by(review_id=self.review_id, reviewer_id=self.current_user.user_id).first()
            if not review:
                return {'Error': 'Review not found or unauthorized'}, HTTPStatus.NOT_FOUND

            if 'rating' in self.data:
                review.rating = self.data['rating']
            if 'review_text' in self.data:
                review.review_text = self.data['review_text']

            self.session.commit()
            return {'Success': 'Review updated', 'review_id': review.review_id}, HTTPStatus.OK
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @validate_ownership
    def delete(self):
        try:
            review = self.session.query(Review).filter_by(review_id=self.review_id, reviewer_id=self.current_user.user_id).first()
            if not review:
                return {'Error': 'Review not found or unauthorized'}, HTTPStatus.NOT_FOUND

            self.session.delete(review)
            self.session.commit()

            return {'Success': 'Review deleted'}, HTTPStatus.OK
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR