from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.amenity import ValidationError

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

facade = HBnBFacade()

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {'id': new_amenity.id, 'name': new_amenity.name}, 201
        
        except ValidationError as e:
            return {'Validationerror': str(e)}, 400

        except Exception as e:
            return {'error': 'An unexpected error occurred: ' + str(e)}, 500

    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(404, 'List of amenities not found')
    def get(self):
        """Retrieve a list of all amenities"""
        amenity_list = facade.get_all_amenities()
        if not amenity_list:
            return {'error': 'List of amenities not found'}, 404

        return [{'id': amenity.id, 'name': amenity.name} for amenity in amenity_list], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'amenity not found'}, 404

        try:
            facade.update_amenity(amenity_id, amenity_data)
            return {"message": "Amenity updated successfully"}, 201

        except ValidationError as e:
            return {'Validationerror': str(e)}, 400

        except Exception as e:
            return {'error': 'An unexpected error occurred: ' + str(e)}, 500
