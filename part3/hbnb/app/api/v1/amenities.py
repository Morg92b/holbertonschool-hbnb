from flask_restx import Namespace, Resource, fields
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import NotFoundError, AuthError

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new amenity"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        facade = current_app.config['FACADE']
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity, 201  
        except ValueError as e:
            return {"Error": str(e)}, 400
        except Exception as e:
            return {"Error": "Failed to create amenity: " + str(e)}, 500


    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        facade = current_app.config['FACADE']
        amenities = facade.get_all_amenities()
        if not amenities:
            return {'error': 'List of amenities not found'}, 404

        return [amenity.to_dict() for amenity in amenities], 200  


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        facade = current_app.config['FACADE']
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200  

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        facade = current_app.config['FACADE']
        amenity_data = api.payload
        try:
            # updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            # return updated_amenity.to_dict(), 200  # Utilise to_dict ici
            facade.update_amenity(amenity_id, amenity_data)
            return {"message": "Amenity updated successfully"}, 200
        except ValueError as e:
            return {"ValueError": str(e)}, 400
        except NotFoundError as e:
            return {"Error": str(e)}, 404
        except Exception as e:
            return {"Error": "Failed to update amenity: " + str(e)}, 500
