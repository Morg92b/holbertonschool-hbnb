import uuid
import re
from datetime import datetime
from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("The first name is required and must contain a maximum of 50 characters")
        if not last_name or len(last_name) > 50:
            raise ValueError("The last name is required and must contain a maximum of 50 characters")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("The email address is invalid")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        

    def save(self):
        super().save()

    def update(self, data):
        
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        if 'email' in data and re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            self.email = data['email']
        super().update(data)


        
