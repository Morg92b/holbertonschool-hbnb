from .base_model import BaseModel
from app.extensions import db

class Amenity(BaseModel):
    __tablename__ = 'TB_AMENITY'

    name = db.Column(db.String(50), nullable=False)


    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("The name of the equipment is mandatory and must not exceed 50 characters")
        self.name = name

    def update(self, data):
        for key, value in data.items():
            if key == "name":
                if not value or len(value) > 50:
                    raise ValueError("The equipment name must not exceed 50 characters")
        super().update(data)

    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }