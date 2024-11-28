from .base_model import BaseModel
from app.extensions import db
from sqlalchemy import ForeignKey


class Review(BaseModel):
    __tablename__ = 'TB_REVIEW'

    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), ForeignKey('TB_PLACE.id'), nullable=False)
    user_id = db.Column(db.String(36), ForeignKey('TB_USER.id'), nullable=False)


    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        # self.place = place
        self.place_id = place_id
        # self.user = user
        self.user_id = user_id
        
        if not self.text:
            raise ValueError("U need to write comment")

        if not (1 <= self.rating <= 5):
            raise ValueError("The new score must be between 1 and 5")

        # if not self.place:
        #     raise ValueError("The place must be exist")

        # if not self.user:
        #     raise ValueError("U need to register or connect Account")


    def update_review(self, data):

        for key, value in data.items():
            if key == 'text':
                if not value:
                    raise ValueError("U need to write comment")
            
            if key == 'rating':
                if not (1 <= value <= 5):
                    raise ValueError("The new score must be between 1 and 5")

        super().update(data)

    def to_dict(self):
        """Convert the review object to a dictionary"""
        return {
            'id': str(self.id),
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }