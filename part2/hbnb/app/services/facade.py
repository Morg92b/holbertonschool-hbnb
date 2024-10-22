from app.persistence.repository import InMemoryRepository
from app.models.user import User, Validator_user
from app.models.amenity import Amenity, Validator_amenity
from app.models.place import Place, Validator_place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder for logic to create, read, update the user
    def create_user(self, user_data):
        """ Placeholder method for creating a user """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """ Placeholder method for geting the user infomation"""
        return self.user_repo.get(user_id)

    def get_all_user(self):
        """ Placeholder method for geting the all user's infomation """
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        """ Placeholder method for updating the user infomation"""
        Validator_user.validate_user(data)
        self.user_repo.update(user_id, data)
        return self.get_user(user_id)

    def get_user_by_email(self, email):
        """ Placeholder method for geting the user infomation by email """
        return self.user_repo.get_by_attribute('email', email)

    # Placeholder for logic to create, read, update the amenity
    def create_amenity(self, amenity_data):
        """ Placeholder for logic to create an amenity """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """ Placeholder for logic to retrieve an amenity by ID """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """ Placeholder for logic to retrieve all amenities """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """ Placeholder for logic to update an amenity """
        Validator_amenity.validate_amenity(amenity_data)
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.get_amenity(amenity_id)

    # Placeholder method for create, read, update the place
    def create_place(self, place_data):
        """ Placeholder for logic to create a place, including validation for price, latitude, and longitude """
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """ Placeholder for logic to retrieve a place by ID, including associated owner and amenities """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """ Placeholder for logic to retrieve all places """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """ Placeholder for logic to update a place """
        Validator_place.validate_place(place_data)
        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)
