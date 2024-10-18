from base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        review_data = {
            "text": self.text,
            "rating": self.rating,
            "place": self.place,
            "user": self.user
        }

        Review.verification_attr(review_data)

        # if not self.text:
        #     raise ValueError("text is required")

        # if self.rating < 1 or self.rating > 5:
        #     raise ValueError("rating must be between 1 and 5")

        # if not self.place:
        #     raise ValueError("place is required")

        # if not self.user:
        #     raise ValueError("user is required")

    @classmethod
    def verification_attr(cls, dict_attr):
        if "text" in dict_attr:
            if not dict_attr["text"]:
                raise ValueError("text is required")

        if "rating" in dict_attr:
            if dict_attr["rating"] < 1 or dict_attr["rating"]  > 5:
                raise ValueError("rating must be between 1 and 5")

        if "place" in dict_attr:
            if not dict_attr["place"]:
                raise ValueError("place is required")

        if "user" in dict_attr:
            if not dict_attr["user"]:
                raise ValueError("user is required")

    def save(self):
        super.save()

    def update(self, data):
        Review.verification_attr(data)
        super.update(data)
