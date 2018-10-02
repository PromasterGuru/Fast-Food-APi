#app/__init__.py

"""
Initalize the app and load configurations
"""

from flask_api import FlaskAPI
from flask_restful import Api
from flask_jwt_extended import JWTManager


#local imports
from instance.config import app_config
# from .api.v1.views import Login, Register, Orders, Order
from .api.v2.database import DB
from .api.v2.views import Login, Register, UserOrders,\
 AdminOrders, AdminOrder, Menu, Users

def create_app(config_name):
    """Wraps the creation of a new Flask object"""
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    JWTManager(app)
    # app_context = app.app_context()
    # app_context.push()
    DB().init_db()

    api = Api(app)

    api.add_resource(Login, '/auth/login')
    api.add_resource(Register, '/auth/signup')
    api.add_resource(UserOrders, '/users/orders')
    api.add_resource(AdminOrders, '/orders/')
    api.add_resource(AdminOrder, '/orders/<int:order_id>')
    api.add_resource(Menu, '/menu')
    api.add_resource(Users, '/users/<int:user_id>')


    return app
