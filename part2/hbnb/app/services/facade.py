from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from flask import jsonify

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    """USER CONFIG"""
    def create_user(self, user_data):
        user = User(**user_data)
        user.is_owner = user_data.get("is_owner", False)
        self.user_repo.add(user)
        print(f"User created: {user.id}")
        return user.to_dict()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        user.update(user_data)
        self.user_repo.update(user_id, user)
        return user.to_dict()


    def get_user(self, user_id):
        return self.user_repo.get(user_id)
        # user = self.user_repo.get(user_id)
        # if user:
        #     return user
        # else:
        #     return jsonify({"Error": "User not found"}), 404

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
    def create_place(self, place_data):
        print("Users in repository:", [user.id for user in self.user_repo.get_all()])
        owner = self.user_repo.get(place_data.get('owner_id')) 
        print(f"Owner ID: {place_data.get('owner_id')}, Found Owner: {owner}")  # Debug

        required_fields = ['title', 'description', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data:
                raise ValueError(f"Missing required field: {field}")

        if not owner:
            raise ValueError("Owner not found")
        if not owner.is_owner:
            raise ValueError("Owner not authorized to create places")

        amenities = place_data.pop('amenities', [])
        place_data.pop('owner_id', None)  

        
        # try:           
        #     place = Place(owner=owner.to_dict(), **place_data)
        #     self.place_repo.add(place)
        # except Exception as e:
        #     print(f"Error creating place: {str(e)}")
        #     return None

        place = Place(owner=owner.to_dict(), **place_data)
        self.place_repo.add(place)

        for amenity_id in amenities:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
            place.add_amenity(amenity)

        print(f"Place created successfully: {place.id}")
        return place.to_dict()


    def get_place(self, place_id): #works
        place = self.place_repo.get(place_id)
        print(f"voici la place", place)
        # if place:
        #     owner_id = place.id
        #     owner = self.user_repo.get(owner_id)  # Get the owner
        #     print(f"voici la owner", owner_id)
        #     if owner:
        #         place.owner = owner
        #     amenities = []
        #     if place.amenities:
        #         for amenity_id in place.amenities:
        #             amenity = self.amenity_repo.get(amenity_id)
        #             if amenity:  # Vérifie si l'amenity existe
        #                 amenities.append(amenity.to_dict())
        #             else:
        #                 print(f"Amenity with ID {amenity_id}")
        #     if amenities:
        #         place.amenities = amenities  # Ajoute les amenities trouvés
        #     return place
        # return None

        return place

    def get_all_places(self):
        places = self.place_repo.get_all()
        return [place.to_dict() for place in places]

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        if 'owner_id' not in place_data:
            raise ValueError("owner id is required")

        owner = self.user_repo.get(place_data.get('owner_id')) 
        if not owner:
            raise ValueError("Owner not found")
        if not owner.is_owner:
            raise ValueError("Owner not authorized to create places")

        amenities = place_data.pop('amenities', [])
        place.update(place_data, owner=owner.to_dict())
        
        # if isinstance(place.owner, dict):
        #     raise ValueError("Owner must be an object of User")
        # self.place_repo.update(place_id, place)
        
        place.amenities = []
        for amenity_id in amenities:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
            place.add_amenity(amenity)

        self.place_repo.update(place_id, place)

        return place.to_dict()

    """REVIEWS CONFIG"""
    def create_review(self, review_data):
        """Checking DATA"""
        user = self.user_repo.get(review_data.get('user_id'))
        place = self.place_repo.get(review_data.get('place_id'))
        if not user:
            raise ValueError("User not found")
        if not place:
            raise ValueError("Place not found")
        """New review"""
        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
            )
        self.review_repo.add(new_review)
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

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        
        new_text = review_data.get('text')
        new_rating = review_data.get('rating')
        review.update_review(review_data, new_text, new_rating)
        self.review_repo.update(review_id, review)

        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)