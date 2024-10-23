from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.place import ValidationError
from app.api.v1.users import UserResource
from app.api.v1.amenities import AmenityResource

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model_post = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
#    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

place_model_put = api.model('Place', {
    'title': fields.String(required=False, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude of the place'),
    'longitude': fields.Float(required=False, description='Longitude of the place'),
    'owner_id': fields.String(required=False, description='ID of the owner'),
#    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model_post)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        # try:
        #     # check id_owner
        #     owner_dict = UserResource.get(self, place_data['owner_id'])
        #     if owner_dict[1] == 404:
        #         raise ValidationError('error: Owner not found')
        
        #     if owner_dict[0]['is_owner'] is False:
        #         raise ValidationError('error: This id user is not Owner')
            
        #     # check id_amenity
        #     if 'amenities' in place_data:
        #         amenity_list = place_data['amenities']

        #         for amenity_id in amenity_list:
        #             amenity_dict = AmenityResource.get(self, amenity_id)
        #             if amenity_dict[1] == 404:
        #                 raise ValidationError(f'error: This id ({amenity_id}) not found in Amenity data')

        new_place = facade.create_place(place_data)

        return {'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id,
                'amenities': new_place.amenities
        }, 201
        
        # except ValidationError as e:
        #     return {'Validationerror': str(e)}, 400

        # except Exception as e:
        #     return {'error': 'An unexpected error occurred: ' + str(e)}, 500

    @api.response(200, 'List of places retrieved successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'List of places not found')
    def get(self):
        """Retrieve a list of all places"""
        place_list = facade.get_all_places()
        if not place_list:
            return {'error': 'List of places not found'}, 404

        return_list =[]
        for place in place_list:
            return_dict = {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner_id
            }
            
            owner_dict = UserResource.get(self, place.owner_id)
            return_dict['owner'] = owner_dict[0]

            return_dict['amenities']= place.amenities

            return_list.append(return_dict)
        
        return return_list


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        return_dict = {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
        }
            
        owner_dict = UserResource.get(self, place.owner_id)
        return_dict['owner'] = owner_dict[0]

        return_dict['amenities']= place.amenities

        return return_dict, 200

    @api.expect(place_model_put)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        place_data = api.payload

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'place not found'}, 404

        try:
            if 'owner_id' in place_data:
                owner_dict = UserResource.get(self, place_data['owner_id'])
                if owner_dict[1] == 404:
                    raise ValidationError('error: Owner not found')
        
                if owner_dict[0]['is_owner'] is False:
                    raise ValidationError('error: This id user is not Owner')

            new_place = facade.update_place(place_id, place_data)
            return {"message": "Place updated successfully"}, 201

        except ValidationError as e:
            return {'Validationerror': str(e)}, 400

        except Exception as e:
            return {'error': 'An unexpected error occurred: ' + str(e)}, 500
