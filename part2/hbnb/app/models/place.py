import uuid
from datetime import datetime
from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
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
        
        if not self.owner:
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
            'owner': self.owner,
            'amenities': [amenity.to_dict() for amenity in self.amenities],
            'reviews': [review for review in self.reviews]
        }
    
    def update(self, data, owner):

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

        self.owner = owner
        super().update(data)

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)