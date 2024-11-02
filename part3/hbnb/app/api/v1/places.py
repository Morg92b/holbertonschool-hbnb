from flask_restx import Namespace, Resource, fields
from flask import current_app

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(required=False, description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model), required=False, description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        facade = current_app.config['FACADE']
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data)
            return new_place, 201
        except ValueError as e:
            return {"Error": str(e)}, 400
        except Exception as e:
            return {"Error": str(e)}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        facade = current_app.config['FACADE']
        list_of_places = facade.get_all_places()

        if not list_of_places:
            return {'error': 'List of place not found'}, 404

        return list_of_places

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        facade = current_app.config['FACADE']
        place = facade.get_place(place_id)
        if not place:
            return {"Error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        facade = current_app.config['FACADE']
        place_data = api.payload

        try:
            updated_place = facade.update_place(place_id, place_data)
            if not updated_place:
                return {"Error": "Place not found"}, 404
            # return updated_place, 200
            return {"message": "Place updated successfully"}, 200
        except ValueError as e:
            return {"Error": str(e)}, 400