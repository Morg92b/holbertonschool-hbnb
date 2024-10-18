from base_model import BaseModel
import re


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        user_data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

        User.verification_attr(user_data)

        # if not self.first_name:
        #     raise ValueError("first_name is required")

        # if len(self.first_name) > 50:
        #     raise ValueError("first_name must be less than or equal to 50 characters")

        # if not self.last_name:
        #     raise ValueError("last_name is required")

        # if len(self.last_name) > 50:
        #     raise ValueError("last_name must be less than or equal to 50 characters")

        # regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # if not (re.fullmatch(regex, self.email)):
        #     raise ValueError("Invalid Email")

    @classmethod
    def verification_attr(cls, dict_attr):
        if "first_name" in dict_attr:
            if not dict_attr["first_name"]:
                raise ValueError("first_name is required")

            if len(dict_attr["first_name"]) > 50:
                raise ValueError("first_name must be less than or equal to 50 characters")

        if "last_name" in dict_attr:
            if not dict_attr["last_name"]:
                raise ValueError("last_name is required")

            if len(dict_attr["last_name"]) > 50:
                raise ValueError("last_name must be less than or equal to 50 characters")

        if "email" in dict_attr:
            regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not (re.fullmatch(regex, dict_attr["email"])):
                raise ValueError("Invalid Email")


    def save(self):
        super().save()

    def update(self, data):
        User.verification_attr(data)
        super().update(data)
