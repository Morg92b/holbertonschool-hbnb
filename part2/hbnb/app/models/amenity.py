import uuid
from datetime import datetime
from base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("The name of the equipment is mandatory and must not exceed 50 characters")
        self.name = name

    def save(self):
        super().save()

    def update(self, data):
        for key, value in data.items():
            if key == "name" and value:
                if len(value) > 50:
                    raise ValueError("The equipment name must not exceed 50 characters")
                self.name = value
        super().update(data)