from base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

        amenity_data = {
            "name": self.name
        }

        Amenity.verification_attr(amenity_data)

        # if not self.name:
        #     raise ValueError("name is required")

        # if len(self.name) > 50:
        #     raise ValueError("name must be less than or equal to 50 characters")

    @classmethod
    def verification_attr(cls, dict_attr):
        if "name" in dict_attr:
            if not dict_attr["name"]:
                raise ValueError("name is required")

            if len(dict_attr["name"]) > 50:
                raise ValueError("name must be less than or equal to 50 characters")

    def save(self):
        super().save()

    def update(self, data):
        Amenity.verification_attr(data)
        super().update(data)
