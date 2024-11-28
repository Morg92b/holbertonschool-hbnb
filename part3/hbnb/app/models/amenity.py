from .base_model import BaseModel
from app.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Amenity(BaseModel):
    __tablename__ = 'TB_AMENITY'

    name = db.Column(db.String(50), nullable=False)
    place_amenity = relationship('PlaceAmenity',  backref='tb_place_amenity', lazy=True)


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
    


class PlaceAmenity(BaseModel):
    __tablename__ = 'TB_PLACE_AMENITY'

    place_id = db.Column(db.String(36), ForeignKey('TB_PLACE.id'), nullable=False)
    amenity_id = db.Column(db.String(36), ForeignKey('TB_AMENITY.id'), nullable=False)

    amenity = relationship('Amenity', backref='placeamenity', lazy=True)

    def __init__(self, place_id, amenity_id):

        self.place_id = place_id
        self.amenity_id = amenity_id

# # Association table for Place et Amenity relationship
# place_amenity = db.Table('TB_PLACE_AMENITY',
#     Column('place_id', String, ForeignKey('TB_PLACE.id'), primary_key=True),
#     Column('amenity_id', String, ForeignKey('TB_AMENITY.id'), primary_key=True)
# )

