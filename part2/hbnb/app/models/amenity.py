from app.models.base_model import BaseModel

class ValidationError(Exception):
    pass


class Validator_amenity:
    @staticmethod
    def validate_presence(value, field_name):
        if not value:
            raise ValidationError(f"{field_name} is required")

    @staticmethod
    def validate_length(value, field_name, max_length):
        if len(value) > max_length:
            raise ValidationError(f"{field_name} must be less than or equal to {max_length} characters")

    @staticmethod
    def validate_amenity(amenity_data):
        """ Validating user attributes """
        for key, value in amenity_data.items():
            if key == 'name':
                Validator_amenity.validate_presence(value, "name")
                Validator_amenity.validate_length(value, "name", 50)


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

        amenity_data = {
            "name": self.name
        }

        Validator_amenity.validate_amenity(amenity_data)

    def update(self, data):
        Validator_amenity.validate_amenity(data)
        super().update(data)
