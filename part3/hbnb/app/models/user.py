import re
from .base_model import BaseModel
from app.extensions import bcrypt


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False, is_owner=False):
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
        self.is_owner = is_owner

        self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')


    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)


    def update(self, data):

        if 'first_name' in data:
            if not data['first_name'] or len(data['first_name']) > 50:
                raise ValueError("The first name is required and must contain a maximum of 50 characters")

        if 'last_name' in data:
            if not data['last_name'] or len(data['last_name']) > 50:
                raise ValueError("The last name is required and must contain a maximum of 50 characters")

        if 'email' in data:
            if not data['email']:
                raise ValueError("The email is required")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
                raise ValueError("The email address is invalid")

        super().update(data)

    def to_dict(self):
        """Convert the User object to a dictionary for JSON serialization."""
        return {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_owner': self.is_owner
            }
