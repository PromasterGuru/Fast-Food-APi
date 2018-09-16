#app/__init__.py

"""
Initalize the app and load configurations
"""

import os
from instance.config import my_app_config
from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# Load the views
from app.api.v1 import views

# Load the config file
app.config.from_object(my_app_config[os.getenv('FLASK_ENV')])
