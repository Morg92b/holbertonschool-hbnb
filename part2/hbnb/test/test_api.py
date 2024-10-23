import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))


from app import create_app
import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app import HBnBFacade

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['FACADE'] = HBnBFacade()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.get_json()['message'])

    def test_create_user_invalid(self):
        """Test creating a user with invalid data."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input data', response.get_json()['Error'])

    def test_create_place_valid(self):
        """Test creating a valid place."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Nice Place",
            "price": 100,
            "latitude": 40.7128,
            "longitude": -74.0060
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Place created successfully', response.get_json()['message'])

    def test_create_place_invalid(self):
        """Test creating a place with invalid data."""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": -50,
            "latitude": 95,  # Invalid latitude
            "longitude": 200  # Invalid longitude
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input data', response.get_json()['error'])

    def test_create_review_valid(self):
        """Test creating a valid review."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "place_id": "valid-place-id",
            "user_id": "valid-user-id"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Review created successfully', response.get_json()['message'])

    def test_create_review_invalid(self):
        """Test creating a review with invalid data."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 6,  # Invalid rating
            "place_id": "invalid-place-id",
            "user_id": "invalid-user-id"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input data', response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()
