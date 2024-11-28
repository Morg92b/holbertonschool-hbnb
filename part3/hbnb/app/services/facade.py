# from app.persistence.repository import InMemoryRepository
from app.persistence.repository import UserRepository, PlaceRepository, ReviewRepository, AmenityRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    """USER CONFIG"""
    def create_user(self, user_data):
        # required_fields = ['first_name', 'last_name', 'email', 'password']
        # for field in required_fields:
        #     if field not in user_data:
        #         raise ValueError(f"Missing required field: {field}")

        user = User(**user_data)
        self.user_repo.add(user)
        print(f"User created: {user.id}")
        return user.id


    def update_user(self, user_id, user_data):
    ## task3 check with user authentification
    # def update_user(self, user_id, user_data, auth_user_id):

        # user = self.get_user(user_id)
        # if not user:
        #     raise NotFoundError("User not found")
        
        ## task3 check with user authentification
        # if user.id != auth_user_id:
        #     raise AuthError("Unauthorized action.")

        ## task3 Prevent the user from modifying their email and password in this endpoint.
        # not_required_fields = ['email', 'password']
        # for field in not_required_fields:
        #     if field in user_data:
        #         raise ValueError("You cannot modify email or password.")

        user = self.get_user(user_id)
        user.update(user_data)
        self.user_repo.update(user_id, user)
        return user.to_dict()


    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        # return self.user_repo.get_by_attribute('email', email)
        return self.user_repo.get_user_by_email(email)

    """AMENITY CONFIG"""
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity.to_dict()

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise NotFoundError("Amenity not found")
        amenity.update(amenity_data)
        self.amenity_repo.update(amenity_id, amenity)

        return amenity

    """PLACE CONFIG"""
    def create_place(self, place_data, auth_user_id):
        required_fields = ['title', 'description', 'price', 'latitude', 'longitude']
        for field in required_fields:
            if field not in place_data:
                raise ValueError(f"Missing required field: {field}")

        # owner = self.user_repo.get(place_data.get('owner_id'))
        # if not owner:
        #     raise ValueError("Invalid owner id")
        # if owner.id != auth_user_id:
        #     raise ValueError("Invalid owner id")
        # if not owner.is_owner:
        #     raise ValueError("Owner not authorized to create places")

        amenities = place_data.pop('amenities', [])

        place = Place(**place_data, owner_id=auth_user_id)

        for amenity_id in amenities:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Invalid data: Amenity with ID {amenity_id} not found")
            place.add_amenity(amenity_id)

        self.place_repo.add(place)

        print(f"Place created successfully: {place.id}")

        place_dict = self.place_repo.get(place.id)

        return place_dict


    def to_dict_place(self, place_data):
        return_dict = {
            'id': place_data.id,
            'title': place_data.title,
            'description': place_data.description,
            'price': place_data.price,
            'latitude': place_data.latitude,
            'longitude': place_data.longitude,
            'owner_id': place_data.owner_id
        }

        owner = place_data.owner
        owner_dict = {
            "owner_id": owner.id,
            "first_name": owner.first_name,
            "last_name": owner.last_name,
            "email": owner.email
        }
        return_dict.setdefault("owner", owner_dict)

        amenities_list = []
        for place_amenity in place_data.amenity_place:
            amenity_dict = {
                "amenity_id": place_amenity.amenity_id,
                "name": place_amenity.amenity.name
            }
            amenities_list.append(amenity_dict)

        return_dict.setdefault("amenities", amenities_list)

        review_list = []
        for review in place_data.tb_review:
            review_dict = {
                "review_id": review.id,
                "text": review.text,
                "rating": review.rating,
                # "place_id": review.place_id,
                "user_id": review.user_id
            }
            review_list.append(review_dict)
        return_dict.setdefault("reviews", review_list)
        return return_dict


    def get_place(self, place_id):
        place_data = self.place_repo.get(place_id)
        return place_data

    def get_all_places(self):
        places = self.place_repo.get_all()
        return [self.to_dict_place(place) for place in places]

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)

        # check owner_id
        if 'owner_id' in place_data:
            owner_up = self.user_repo.get(place_data.get('owner_id'))
            if not owner_up:
                raise ValueError("Owner not found, Invalid data: owner_id")
            if not owner_up.is_owner:
                raise ValueError("Owner not authorized to create places")

        amenities = place_data.pop('amenities', [])

        place.update(place_data)

        place.amenities = []
        for amenity_id in amenities:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
            place.add_amenity(amenity_id)

        self.place_repo.update(place_id, place)

        return

    def delete_place(self, place_id, auth_user_id, auth_is_admin):
        place = self.get_place(place_id)
        if not place:
            raise NotFoundError("Place not found")

        if not auth_is_admin and place.owner_id != auth_user_id:
            raise AuthError("Unauthorized action.")

        self.place_repo.delete(place_id)


    """REVIEWS CONFIG"""
    def create_review(self, review_data, auth_user_id):

        # required_fields = ['text', 'rating', 'user_id', 'place_id']
        required_fields = ['text', 'rating', 'place_id']
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")

        """Checking DATA"""
        place_id = review_data.get('place_id')
        if not place_id:
            raise ValueError("Place id is required")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Invalid data: place_id, Place not found")

        # Check that the place_id in the request belongs to a place the user does not own.
        if place.owner_id == auth_user_id:
            raise AuthError("You cannot review your own place.")

        # Check that the user has not already reviewed this place.
        reviews = self.get_reviews_by_place(place_id)
        if reviews:
            for review in reviews:
                if review.user_id == auth_user_id:
                    raise AuthError("You have already reviewed this place.")

        """New review"""
        new_review = Review(**review_data, user_id=auth_user_id)

        """ add review to place review_list """
        # # place.add_review(new_review.id)
        # # self.place_repo.update(place_id, place)

        self.review_repo.add(new_review)

        return new_review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise NotFoundError("Review not found")
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Invalid data: place_id, Place not found")
        # reviews = [review for review in self.review_repo._storage.values() if review.place_id == place_id]
        reviews = [review for review in self.review_repo.get_all() if review.place_id == place_id]
        return reviews

    def update_review(self, review_id, review_data, auth_user_id):

        review = self.get_review(review_id)
        if not review:
            raise NotFoundError("Review not found")

        if not review.user_id == auth_user_id:
            raise AuthError("Unauthorized action.")

        review.update_review(review_data)
        self.review_repo.update(review_id, review)

        return review

    def delete_review(self, review_id, auth_user_id, auth_is_admin):
        review = self.get_review(review_id)
        if not review:
            raise NotFoundError("Review not found")

        if not auth_is_admin and review.user_id != auth_user_id:
            raise AuthError("Unauthorized action.")

        # # """ remove review from place review_list """
        # # place = self.get_place(review.place_id)
        # # if review_id in place.reviews:
        # #     place.reviews.remove(review_id)
        # #     self.place_repo.update(review.place_id, place)

        self.review_repo.delete(review_id)


class NotFoundError(Exception):
    pass

class AuthError(Exception):
    pass
