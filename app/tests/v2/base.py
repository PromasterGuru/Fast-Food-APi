import json
import os
import sys
import unittest

# Local imports
from app import create_app


class BaseTestCase(unittest.TestCase):
    """Application base tests data"""


    def setUp(self):
        """Define and Initalize test variables"""
        self.app = create_app(config_name='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client

        self.valid_user = {
            "email": "pmutondo16@gmail.com",
            "username": "Promaster2020",
            "password": "Promaster2020"
        }

        self.invalid_user1 = {
            "email": "pmutondo16@gmailcom",
            "username": "Promaster2018",
            "password": "Promaster2018"
        }
        self.invalid_user2 = {
            "email": "pmutondo16@gmail.com",
            "username": "Prom",
            "password": "Promaster2018"
        }
        self.invalid_user3 = {
            "email": "pmutondo16@gmail.com",
            "username": "Promaster2018",
            "password": "Prom"
        }
        self.invalid_user4 = {
            "email": "pmutondo16@gmail.com",
            "username": "Promaster2019",
            "password": "Promasterpaul"
        }
        self.invalid_user5 = {
            "email": "pmutondo16@gmail.com",
            "username": "Promaster2018",
            "password": "promaster2018"
        }
        self.invalid_user6 = {
            "email": "pmutondo12@gmail.com",
            "username": "Promaster",
            "password": "Promaster2018"
        }
        self.valid_login = {
            "username": "Promaster",
            "password": "Promaster2018"
        }
        self.invalid_login1 = {
            "username": "Promaster2018",
            "password": ""
        }
        self.invalid_login2 = {
            "username": "Paul",
            "password": "Promaster2018"
        }
        self.invalid_login3 = {
            "username": "Promaster2018",
            "password": "Paul18"
        }
        self.menu = {
            "meal_id": 1,
            "name": "Pizza",
            "description": "Meat and veggie options to keep the whole family smiling.",
            "unit_price": 2.55
        }
        self.invalid_menu = {
            "name": "Pumkin Juice",
            "description": "African juice made of malched Pumkin",
            "price": 2.50
        }
        self.order = {
            "meal_id": "Pumkin Juice",
            "description": "Pumkin juice with no added sugar, "
                           +"Address: Stall Mall, Moi Aven.",
            "quantity": 2
        }
        self.invalid_order = {
            "meal_id": "",
            "description": "Pumkin juice with no added sugar, "
                           +"Address: Stall Mall, Moi Aven.",
            "quantity": 2
        }

    def register_user(self):
        """Register new user with dummy data"""
        return self.client().post(
            'auth/signup',
            data=json.dumps(self.valid_user),
            content_type='application/json')

    def register_user_invalid_email(self):
        """Register new user with dummy data"""
        return self.client().post(
            'auth/signup',
            data=json.dumps(self.invalid_user1),
            content_type='application/json')

    def register_user_invalid_username(self):
        """Register new user with dummy data"""
        return self.client().post(
            'auth/signup',
            data=json.dumps(self.invalid_user2),
            content_type='application/json')

    def register_user_short_password(self):
        """Register new user with dummy data"""
        return self.client().post(
            'auth/signup',
            data=json.dumps(self.invalid_user3),
            content_type='application/json')

    def register_user_non_numeric_password(self):
        """Register new user with dummy data"""
        return self.client().post(
            'auth/signup',
            data=json.dumps(self.invalid_user4),
            content_type='application/json')

    def register_user_password_has_no_caps(self):
        """Register new user with dummy data"""
        return self.client().post(
            'auth/signup',
            data=json.dumps(self.invalid_user5),
            content_type='application/json')

    def register_existing_user(self):
        """Register new user with dummy data"""
        return self.client().post(
            'auth/signup',
            data=json.dumps(self.invalid_user6),
            content_type='application/json')

    def user_login(self):
        """User can login"""
        return self.client().post(
            'auth/login',
            data=json.dumps(self.valid_login),
            content_type='application/json')

    def get_user_token(self):
        """Generate and return user token"""
        user_token = self.user_login().data.decode('utf-8')
        return user_token

    def view_menu_options(self):
        """View availlable menu options"""
        return self.client().get(
            '/menu',
            content_type='application/json')

    def add_menu_options(self):
        """View availlable menu options"""
        access_token = self.get_user_token()
        return self.client().post(
            '/menu',
            data=json.dumps(self.menu),
            headers=dict(Authorization="Bearer "+ access_token))
