from flask_restx import Namespace, Resource, fields
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import NotFoundError, AuthError

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(required=False, description='Name of the amenity')
})

# user_model = api.model('PlaceUser', {
#     'id': fields.String(description='User ID'),
#     'first_name': fields.String(description='First name of the owner'),
#     'last_name': fields.String(description='Last name of the owner'),
#     'email': fields.String(description='Email of the owner')
# })

# review_model = api.model('PlaceReview', {
#     'id': fields.String(description='Review ID'),
#     'text': fields.String(description='Text of the review'),
#     'rating': fields.Integer(description='Rating of the place (1-5)'),
#     'user_id': fields.String(description='ID of the user')
# })

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    # 'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

place_model_up = api.model('Place_up', {
    'title': fields.String(required=False, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude of the place'),
    'longitude': fields.Float(required=False, description='Longitude of the place'),
    'owner_id': fields.String(required=False, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Not Found data')
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        if current_user['is_owner'] is False:
            return {'Error': 'No authorized for create places'}, 403

        facade = current_app.config['FACADE']
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data, current_user['id'])
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
            return {'message': 'No place created'}, 200

        return list_of_places

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        facade = current_app.config['FACADE']
        place_dict = facade.get_place(place_id)
        if not place_dict:
            return {"NotFoundError": "Place not found"}, 404

        place_dict = facade.to_dict_place(place_dict)
        return place_dict, 200


    @jwt_required()
    @api.expect(place_model_up)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()

        facade = current_app.config['FACADE']
        place_data = api.payload

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {"NotFoundError": "Place not found"}, 404

        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            # updated_place = facade.update_place(place_id, place_data, current_user['id'])
            # return updated_place, 200
            facade.update_place(place_id, place_data)
            return {"message": "Place updated successfully"}, 200
        except ValueError as e:
            return {"ValueError": str(e)}, 400
        except NotFoundError as e:
            return {"NotFoundError": str(e)}, 404
        except Exception as e:
            return {"Error": str(e)}, 500



    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        # Placeholder for the logic to delete a place
        current_user = get_jwt_identity()
        facade = current_app.config['FACADE']
        try:
            facade.delete_place(place_id, current_user['id'], current_user['is_admin'])
            return {"message": "Review deleted successfully"}, 200
        except NotFoundError:
            api.abort(404, f"Review with ID {place_id} not found")
        except AuthError as e:
                api.abort(403, str(e))

