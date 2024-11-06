from flask_restx import Namespace, Resource, fields
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import NotFoundError, AuthError

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_owner': fields.Boolean(required=False, description='Indicates if the user is an owner', default=False)
})

user_model_up = api.model('User_up', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
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
            new_user_id = facade.create_user(user_data)
        except ValueError as e:
            return {"Error": str(e)}, 400
        except Exception as e:
            return {"Error": str(e)}, 500

        return_message = {"message": "User created successfully",
                          "user id":  new_user_id} 
        return return_message, 201

    
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

    @jwt_required()
    @api.expect(user_model_up, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user details by ID"""
        current_user = get_jwt_identity()

        facade = current_app.config['FACADE']
        user_data = api.payload
        # existing_user = facade.get_user(user_id)
        # if not existing_user:
        #     return {"NotFoundError": "User not found"}, 404
        
        # if existing_user.user_id != current_user['id']:
        #     return {"Unauthorized action."}, 403

        try:
            updated_user = facade.update_user(user_id, user_data, current_user['id'])
            return updated_user, 200

        except ValueError as e:
            return {"Error": str(e)}, 400
        except NotFoundError as e:
            return {"Error": str(e)}, 404
        except AuthError as e:
            return {"Error": str(e)}, 403
        except Exception as e:
            return {"Error": str(e)}, 500
