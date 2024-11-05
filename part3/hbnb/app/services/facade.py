from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
# from flask import jsonify

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    """USER CONFIG"""
    def create_user(self, user_data):
        user = User(**user_data)
        # user.is_owner = user_data.get("is_owner", False)
        self.user_repo.add(user)
        print(f"User created: {user.id}")
        # return user.to_dict()
        return user.id

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        user.update(user_data)
        self.user_repo.update(user_id, user)
        return user.to_dict()


    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

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
            raise ValueError("Amenity not found")
        amenity.update(amenity_data)
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

    """PLACE CONFIG"""
    def create_place(self, place_data, auth_user_id):
        # required_fields = ['title', 'description', 'price', 'latitude', 'longitude', 'owner_id']
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
        self.place_repo.add(place)

        for amenity_id in amenities:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Invalid data: Amenity with ID {amenity_id} not found")
            place.add_amenity(amenity)

        print(f"Place created successfully: {place.id}")

        place_dict = self.to_dict_place(place)

        return place_dict


    def to_dict_place(self, place_data):
        place_dict = place_data.to_dict()
        owner_id = place_dict.pop('owner_id')
        print(f'owner_id: {owner_id}')
        amenities = place_dict.pop('amenities')
        reviews = place_dict.pop('reviews')

        owner = self.user_repo.get(owner_id)
        owner_dict = {
            "owner_id": owner_id,
            "first_name": owner.first_name,
            "last_name": owner.last_name,
            "email": owner.email
        }

        place_dict.setdefault("owner", owner_dict)
        place_dict.setdefault("amenities", amenities)
        place_dict.setdefault("reviews", reviews)

        return place_dict


    def get_place(self, place_id): #works
        place_dict = self.place_repo.get(place_id)
        # if place_dict:
        #     place_dict = self.to_dict_place(place_dict)

        return place_dict

    def get_all_places(self):
        places = self.place_repo.get_all()
        return [self.to_dict_place(place) for place in places]

    def update_place(self, place_id, place_data, auth_user_id):
        place = self.get_place(place_id)
        if not place:
            raise NotFoundError("Place not found")

        # if 'owner_id' not in place_data:
        #     raise ValueError("owner id is required")

        # owner = self.user_repo.get(place_data.get('owner_id'))
        owner = self.user_repo.get(auth_user_id)
        if not owner:
            raise ValueError("Owner not found, Invalid data: owner id")
        # if not owner.is_owner:
        #     raise ValueError("Owner not authorized to create places")

        amenities = place_data.pop('amenities', [])

        # place.update(place_data, owner=owner.to_dict())
        place.update(place_data)
        ### !!ask chong,  place.owner_id は変更可能？？

        place.amenities = []
        for amenity_id in amenities:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
            place.add_amenity(amenity)

        self.place_repo.update(place_id, place)

        return place.to_dict()

    """REVIEWS CONFIG"""
    def create_review(self, review_data, auth_user_id):

        # required_fields = ['text', 'rating', 'user_id', 'place_id']
        required_fields = ['text', 'rating', 'place_id']
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")

        """Checking DATA"""
        # user_id = review_data.get('user_id')
        # if not user_id:
        #     raise ValueError("User id is required")

        # user = self.user_repo.get(user_id)
        # if not user:
        #     raise ValueError("Invalid data: user id, User not found")

        place_id = review_data.get('place_id')
        if not place_id:
            raise ValueError("Place id is required")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Invalid data: place id, Place not found")

        # Check that the place_id in the request belongs to a place the user does not own.
        if place.owner_id == auth_user_id:
            raise Exception("You cannot review your own place.")

        # Check that the user has not already reviewed this place.
        reviews = self.get_reviews_by_place(place_id)
        if reviews:
            for review in reviews:
                if review['user_id'] == auth_user_id:
                    raise Exception("You cannot review your own place.")

        """New review"""
        new_review = Review(**review_data, user_id=auth_user_id)

        # new_review = Review(
        #     text=review_data['text'],
        #     rating=review_data['rating'],
        #     place=place,
        #     user=user
        #     )
        self.review_repo.add(new_review)

        """ add review to place review_list """
        # self.place_repo.update(place.id, place)

        review_dict = {
            'id': new_review.id,
            'text': review_data['text'],
            'rating': review_data['rating'],
            # 'user_id': review_data['user_id']
            'user_id': auth_user_id
        }

        place.add_review(review_dict)

        return new_review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        reviews = [review for review in self.review_repo._storage.values() if review.place.id == place_id]
        return reviews

    def update_review(self, review_id, review_data, auth_user_id):

        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        # required_fields = ['place_id']
        # for field in required_fields:
        #     if field not in review_data:
        #         raise ValueError(f"Missing required field: {field}")

        # if not review_data.get('place_id'):
        #     raise ValueError("Place id is required")

        # if not review_data.get('user_id'):
        #     raise ValueError("User id is required")

        # if not review.place_id == review_data.get('place_id'):
        #     raise ValueError("unmatch the place registered")

        if not review.user_id == auth_user_id:
            raise Exception("Unauthorized action.")

        review.update_review(review_data)
        self.review_repo.update(review_id, review)

        """ update review to place review list """
        place = self.get_place(review_data.get('place_id'))
        for index in range(len(place.reviews)):
            if place.reviews[index]['id'] == review_id:
                if 'text' in review_data:
                    place.reviews[index]['text'] = review_data['text']
                if 'rating' in review_data:
                    place.reviews[index]['rating'] = review_data['rating']

        return review

    def delete_review(self, review_id, auth_user_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        if not review.user_id == auth_user_id:
            raise Exception("Unauthorized action.")

        """ remove review from place review_list """
        place = self.get_place(review.place_id)
        for index in range(len(place.reviews)):
            if place.reviews[index]['id'] == review_id:
                del place.reviews[index]

        self.review_repo.delete(review_id)


class NotFoundError(Exception):
    pass
