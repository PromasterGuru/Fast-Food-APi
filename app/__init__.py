#app/__init__.py

"""
Initalize the app and load configurations
"""

from flask_api import FlaskAPI
from instance.config import my_app_config


def create_app(app_config_name):
    """Wraps the creation of a new Flask object"""
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(my_app_config[app_config_name])
    app.config.from_pyfile('config.py')

    return app #return app after loading all the configurations settings
