from flask import Flask
from flask_restx import Api
from app.services.facade import HBnBFacade
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as place_ns


def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Init the facade
    app.config['FACADE'] = HBnBFacade()

    # Facade
    users_ns.facade = app.config['FACADE']
    amenities_ns.facade = app.config['FACADE']
    place_ns.facade = app.config['FACADE']

    # Register  namepsace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(place_ns, path='/api/v1/places')


    return app