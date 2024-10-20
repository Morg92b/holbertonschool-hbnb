from app.persistence.repository import InMemoryRepository
from app.models.user import User, Validator_user
from app.models.amenity import Amenity, Validator_amenity

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

    def put_user(self, user_id, data):
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

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
