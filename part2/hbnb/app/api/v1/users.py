from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.user import ValidationError

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model1 = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

user_model2 = api.model('User', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user')
})

facade = HBnBFacade()

@api.route('/')
class UserList(Resource):
    @api.expect(user_model1, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
        
        except ValidationError as e:
            return {'Validationerror': str(e)}, 400

        except Exception as e:
            return {'error': 'An unexpected error occurred: ' + str(e)}, 500

    @api.response(200, 'List of Users retrieved successfully')
    @api.response(404, 'List of Users not found')
    def get(self):
        """Get list of users"""
        user_list = facade.get_all_user()
        if not user_list:
            return {'error': 'List of Users not found'}, 404

        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in user_list], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model2, validate=True)
    @api.response(200, 'User details successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Put(Update) user details by ID"""
        user_data = api.payload

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered for other user'}, 400

        try:
            new_user = facade.update_user(user_id, user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

        except ValidationError as e:
            return {'Validationerror': str(e)}, 400

        except Exception as e:
            return {'error': 'An unexpected error occurred: ' + str(e)}, 500
