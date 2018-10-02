import json
import os
import sys
import unittest

# Local imports
from app import create_app
from app.api.v2.views import Role
from app.api.v2.models import FoodOrders

class BaseTestCase(unittest.TestCase):
    """Application base tests data"""


    def setUp(self):
        """Define and Initalize test variables"""
        self.app = create_app(config_name='testing')
        self.orders = FoodOrders()
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
            "username": "Promaster",
            "password": "Paul18"
        }
        self.menu = {
            "name": "Chapo",
            "description": "Meat and veggie options to keep the whole family smiling.",
            "unit_price": 2.50
        }
        self.invalid_menu = {
            "name": "Pumkin Juice",
            "description": "African juice made of malched Pumkin",
            "price": 2.50
        }
        self.order = {
            	"meal_id": 1,
            	"description": "Eight trapias and one solomon fish",
            	"quantity": 3
        }
        self.invalid_order = {
            "meal_id": "",
            "description": "Pumkin juice with no added sugar, "
                           +"Address: Stall Mall, Moi Aven.",
            "quantity": 2
        }

        self.update_order = {
            "status": "Complete"
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

    def user_invalid_login1(self):
        """User cannot login"""
        return self.client().post(
            'auth/login',
            data=json.dumps(self.invalid_login1),
            content_type='application/json')

    def user_invalid_login2(self):
        """User cannot login"""
        return self.client().post(
            'auth/login',
            data=json.dumps(self.invalid_login2),
            content_type='application/json')

    def user_invalid_login3(self):
        """User cannot login"""
        return self.client().post(
            'auth/login',
            data=json.dumps(self.invalid_login3),
            content_type='application/json')

    def get_user_token(self):
        """Generate and return user token"""
        resp_login = self.user_login()
        token = 'Bearer ' + json.loads(
            resp_login.data.decode()
            )['access_token']

        return token


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
            headers={
                "content-type": "application/json",
                "Authorization": access_token
            })

    def post_order(self):
        """User can post and order"""
        access_token = self.get_user_token()
        return self.client().post(
            '/users/orders',
            data=json.dumps(self.order),
            headers={
                "content-type": "application/json",
                "Authorization": access_token
            })

    def view_orders(self):
        """User can view their orders"""
        access_token = self.get_user_token()
        return self.client().get(
            '/users/orders',
            data=json.dumps(self.order),
            headers={
                "content-type": "application/json",
                "Authorization": access_token
            })

    def update_order_status(self):
        """Admin user can update orders"""
        access_token = self.get_user_token()
        return self.client().put(
            '/orders/1',
            data=json.dumps(self.update_order),
            headers={
                "content-type": "application/json",
                "Authorization": access_token
            })

    def delete_order(self):
        """Admin user can delete orders"""
        access_token = self.get_user_token()
        return self.client().delete(
            '/orders/1',
            data=json.dumps(self.order),
            headers={
                "content-type": "application/json",
                "Authorization": access_token
            })

    def drop_tables(self):
        """Delete all the testing tables"""
        self.orders.teatDown()
