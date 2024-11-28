from flask_restx import Namespace, Resource, fields
from flask import current_app

api = Namespace('admin', description='Admin operations')

# Define the user model for input validation and documentation
user_model_ad = api.model('User_ad', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_owner': fields.Boolean(required=False, description='Indicates if the user is an owner', default=False),
    'is_admin': fields.Boolean(required=True, description='Indicates if the user is an Administrator', default=True)
})


@api.route('/', methods=['POST'])
class CreateAdmin(Resource):
    @api.expect(user_model_ad, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new admin user"""
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

        return_message = {"message": "Administrator created successfully",
                          "admin user id":  new_user_id} 
        return return_message, 201

