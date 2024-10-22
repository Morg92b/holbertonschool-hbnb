from app.models.base_model import BaseModel


class ValidationError(Exception):
    pass


class Validator_place:
    @staticmethod
    def validate_presence(value, field_name):
        if not value:
            raise ValidationError(f"{field_name} is required")

    @staticmethod
    def validate_length(value, field_name, max_length):
        if len(value) > max_length:
            raise ValidationError(f"{field_name} must be less than or equal to {max_length} characters")

    @staticmethod
    def validate_value(value, field_name, min_value, max_value):
        if value < min_value or value > max_value:
            raise ValidationError(f"{field_name} must be within the range of {min_value} to {max_value}")

    @staticmethod
    def validate_value_positive(value, field_name):
        if value <= 0:
            raise ValidationError(f"{field_name} must be a positive value")

    @staticmethod
    def validate_place(place_data):
        """ Validating place attributes """
        for key, value in place_data.items():
            if key == 'title':
                Validator_place.validate_presence(value, "title")
                Validator_place.validate_length(value, "title", 100)
            elif key == 'price':
                Validator_place.validate_value_positive(value, "price")
            elif key == 'latitude':
                Validator_place.validate_value(value, "latitude", -90.0, 90.0)
            elif key == 'longitude':
                Validator_place.validate_value(value, "longitude", -180.0, 180.0)
            elif key == 'owner_id':
                Validator_place.validate_presence(value, "owner_id")


class Place(BaseModel):
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

        place_data = {
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id
        }

        Validator_place.validate_place(place_data)

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def update(self, data):
        Validator_place.validate_place(data)
        super().update(data)
