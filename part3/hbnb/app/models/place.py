from .base_model import BaseModel
from app.models.amenity import PlaceAmenity
from app.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Place(BaseModel):
    __tablename__ = 'TB_PLACE'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, default=False)
    owner_id = db.Column(db.String(36), ForeignKey('TB_USER.id'), nullable=False)

    # Userとのリレーション（オーナー情報）
    owner = relationship('User', backref='tb_place_owner', lazy=True)

    tb_review = relationship('Review', backref='tb_place', lazy=True)
    amenity_place = relationship('PlaceAmenity', backref='tb_amenit_place', lazy='subquery')


    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
        
        if not self.title or len(self.title) > 100:
            raise ValueError("The title is mandatory and must be less than 100 characters")
        
        if self.price <= 0:
            raise ValueError("The price must be positive")
        
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        
        if not self.owner_id:
            raise ValueError("The owner is required")

        
    def to_dict(self):
        """Convert the Place object to a dictionary for JSON serialization."""
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
            # # 'owner_id': self.owner_id,
            # # 'amenities': [amenity.to_dict() for amenity in self.amenities],
            # # 'reviews': [review for review in self.reviews]
        }
    
    def update(self, data):

        for key, value in data.items():
            if key == 'title':
                if not value or len(value) > 100:
                    raise ValueError("The title is mandatory and must be less than 100 characters")
            
            if key == 'price':
                if value <= 0:
                    raise ValueError("The price must be positive")

            if key == 'latitude':
                if not (-90.0 <= value <= 90.0):
                    raise ValueError("Latitude must be between -90.0 and 90.0")

            if key == 'longitude':
                if not (-180.0 <= value <= 180.0):
                    raise ValueError("Longitude must be between -180.0 and 180.0")

        super().update(data)

    def add_review(self, review_id):
        """Add a review to the place."""
        self.reviews.append(review_id)

    def add_amenity(self, amenity_id):
        # """Add an amenity to the place."""
        # self.amenities.append(amenity)

        """Add an amenity to this place."""
        place_amenity = PlaceAmenity(place_id=self.id, amenity_id=amenity_id)
        self.amenity_place.append(place_amenity)