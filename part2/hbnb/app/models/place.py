from base_model import BaseModel


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

        place_data = {
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner
        }

        Place.verification_attr(place_data)

        # if not self.title:
        #     raise ValueError("title is required")

        # if len(self.title) > 100:
        #     raise ValueError("title must be less than or equal to 100 characters")

        # if self.price <= 0:
        #     raise ValueError("price must be a positive value")
        
        # if self.latitude < -90 or self.latitude > 90:
        #     raise ValueError("latitude must be within the range of -90.0 to 90.0")

        # if self.longitude < -180 or self.longitude > 180:
        #     raise ValueError("longitude must be within the range of -180.0 to 180.0")

        # if not self.owner:
        #     raise ValueError("owner is required")

    @classmethod
    def verification_attr(cls, dict_attr):
        if "title" in dict_attr:
            if not dict_attr["title"]:
                raise ValueError("title is required")

            if len(dict_attr["title"]) > 100:
                raise ValueError("title must be less than or equal to 100 characters")

        if "price" in dict_attr:
            if dict_attr["price"] <= 0:
                raise ValueError("price must be a positive value")

        if "latitude" in dict_attr:
            if dict_attr["latitude"] < -90 or dict_attr["latitude"]  > 90:
                raise ValueError("latitude must be within the range of -90.0 to 90.0")

        if "longitude" in dict_attr:
            if dict_attr["longitude"] < -180 or dict_attr["longitude"]  > 180:
                raise ValueError("longitude must be within the range of -180.0 to 180.0")

        if "owner" in dict_attr:
            if not dict_attr["owner"]:
                raise ValueError("owner is required")


    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def save(self):
        super().save()

    def update(self, data):
        Place.verification_attr(data)
        super().update(data)
