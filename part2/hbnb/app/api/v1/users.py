from flask_restx import Namespace, Resource, fields
from flask import current_app
from app.models.user import User

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'is_owner': fields.Boolean(required=False, description='Indicates if the user is an owner', default=False)
})

@api.route('/', methods=['POST'])
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        facade = current_app.config['FACADE']

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
        except Exception as e:
            return {"Error": str(e)}, 500
        return new_user, 201

    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        facade = current_app.config['FACADE']
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user details by ID"""
        facade = current_app.config['FACADE']
        user_data = api.payload
        existing_user = facade.get_user(user_id)
        if not existing_user:
            return {"Error": "User not found"}, 404
        try:
            updated_user = facade.update_user(user_id, user_data)
        except Exception as e:
            return {"Error": str(e)}, 500
        return {
            'id': updated_user['id'],
            'first_name': updated_user['first_name'],
            'last_name': updated_user['last_name'],
            'email': updated_user['email']
        }, 200
