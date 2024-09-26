import json
from app.utils.models.absract_request_strategy import AbstractResponseComposeStrategy
from app.data.model_db.db_cars_hub import User

class ReviewResponseModel(AbstractResponseComposeStrategy):
    def __init__(self, model, session):
        super().__init__(model)
        self.session = session

    def compose(self, response_body: json):
        reviewer = self.session.query(User).filter_by(user_id=response_body.reviewer_id).first()
        reviewed_user = self.session.query(User).filter_by(user_id=response_body.reviewed_user_id).first()

        return {
            'review_id': response_body.review_id,
            'reviewer': reviewer.name if reviewer else 'Unknown',
            'reviewed_user': reviewed_user.name if reviewed_user else 'Unknown',
            'reviewer_id': response_body.reviewer_id, 
            'reviewed_user_id': response_body.reviewed_user_id,  
            'rating': str(response_body.rating),
            'review_text': response_body.review_text,
            'created_at': response_body.created_at.strftime('%Y-%m-%d %H:%M:%S') if response_body.created_at else None
        }

class ReviewModel:
    def __init__(self) -> None:
        self.review_id = None
        self.reviewer = None  
        self.reviewed_user = None  
        self.reviewer_id = None 
        self.reviewed_user_id = None 
        self.rating = None
        self.review_text = None
        self.created_at = None