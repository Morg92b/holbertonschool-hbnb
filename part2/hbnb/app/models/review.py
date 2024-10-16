import uuid
from datetime import datetime
from base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        if not (1 <= self.rating <= 5):
            raise ValueError("The new score must be between 1 and 5.")
        
        if not self.text:
            raise ValueError("U need to write comment")
        if not self.place:
            raise ValueError("The place must be exist")
        if not self.user:
            raise ValueError("U need to register or connect Account")

    def save(self):
        super().save()

    def update_review(self, data, new_text=None, new_rating=None):
        super().update(data)
        if new_text:
            self.text = new_text
        if new_rating:
            if not (1 <= new_rating <= 5):
                raise ValueError("The new score must be between 1 and 5.")
            self.rating = new_rating
        self.updated_at = datetime.now()