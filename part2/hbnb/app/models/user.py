from app.models.base_model import BaseModel
import re


class ValidationError(Exception):
    pass


class Validator_user:
    @staticmethod
    def validate_presence(value, field_name):
        if not value:
            raise ValidationError(f"{field_name} is required")

    @staticmethod
    def validate_length(value, field_name, max_length):
        if len(value) > max_length:
            raise ValidationError(f"{field_name} must be less than or equal to {max_length} characters")

    @staticmethod
    def validate_email(value):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.fullmatch(regex, value):
            raise ValidationError("Invalid Email")

    @staticmethod
    def validate_user(user_data):
        """ Validating user attributes """
        for key, value in user_data.items():
            if key == 'first_name':
                Validator_user.validate_presence(value, "First name")
                Validator_user.validate_length(value, "First name", 50)
            elif key == 'last_name':
                Validator_user.validate_presence(value, "Last name")
                Validator_user.validate_length(value, "Last name", 50)
            elif key == 'email':
                Validator_user.validate_email(value)


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

        Validator_user.validate_user(user_data)

    def update(self, data):
        """ Validating the update data and update them """
        Validator_user.validate_user(data)
        super().update(data)
