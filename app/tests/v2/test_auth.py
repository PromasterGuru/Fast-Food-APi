#app/tests/v2/test_auth.py

'''Implement classes and methods for testing API Endpoints.'''

import json
import unittest
import jwt
import os
from app import create_app


class TestAuthentication(unittest.TestCase):
    '''This class represents user authentication unit tests'''


    def setUp(self):
        '''Define variables and initialize app'''
        self.app = create_app(app_config_name="testing")
        self.client = self.app.test_client

    def test_config(self):
        """Test configurations"""
        self.assertEqual(self.app.testing, True)

    def test_register_for_new_users(self):
        """User can register for a new account"""
        user = {
            'user_id': 1,
            'username': 'Promaster@@',
            'password': 'Promaster2018',
        }
        resp = self.client().post(
            '/auth/signup',
            data=json.dumps(user),
            headers={'content-type': 'application/json'}
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 201, response['Message'])


    def test_register_for_registered_users(self):
        """User should not be allowed to register twice"""
        user = {
            'user_id': 1,
            'username': 'Promaster@@',
            'password': 'Promaster2018',
        }
        resp = self.client().post(
            '/auth/signup',
            data=json.dumps(user),
            headers={'content-type': 'application/json'}
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 401, response['Message'])

    def test_register_with_empty_username(self):
        """Test when username is left blank"""
        newuser = {
            "user_id": 1,
            "username": "",
            "password": "Promaster2018"
        }
        resp = self.client().post(
            '/auth/signup',
            data=json.dumps(newuser),
            headers={'content-type': 'application/json'}
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 400, response['Message'])

    def test_register_with_short_username(self):
        """When username is less than 6 characters"""
        newuser = {
            "user_id": 1,
            "username": "paul",
            "password": "Promaster2018"
        }
        resp = self.client().post(
            '/auth/signup',
            data=json.dumps(newuser),
            headers={'content-type': 'application/json'}
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 400, response['Message'])

    def test_register_without_password(self):
        """User tries to register without a password"""
        newuser = {
            "user_id": 1,
            "username": "Promaster",
            "password": ""
        }
        resp = self.client().post(
            '/auth/signup',
            data=json.dumps(newuser),
            headers={'content-type': 'application/json'}
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 400, response['Message'])

    def test_register_with_short_password(self):
        """Password less than 8 alphanumeric characters"""
        newuser = {
            "user_id": 1,
            "username": "Promaster",
            "password": "Pm2018"
        }
        resp = self.client().post(
            '/auth/signup',
            data=json.dumps(newuser),
            headers={'content-type': 'application/json'}
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 400, response['Message'])

    def test_register_for_password_without_numbers(self):
        """Password without atleast one numeric character"""
        newuser = {
            "user_id": 1,
            "username": "Promaster",
            "password": "Promaster"
        }
        resp = self.client().post(
            '/auth/signup',
            data=json.dumps(newuser),
            headers={'content-type': 'application/json'}
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 400, response['Message'])

    def test_register_for_password_without_capital_letters(self):
        """Password without atleast one capital letter"""
        newuser = {
            "user_id": 1,
            "username": "Promaster",
            "password": "promaster2018"
        }
        resp = self.client().post(
            '/auth/signup',
            data=json.dumps(newuser),
            headers={'content-type': 'application/json'}
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 400, response['Message'])

    def test_register_bad_request_with_username(self):
        """Username not included in the request"""
        newuser = {
            "password": "promaster2018"
        }
        resp = self.client().post(
            '/auth/signup',
            data=json.dumps(newuser),
            headers={'content-type': 'application/json'}
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 400, response['Message'])

    def test_register_bad_request_with_password(self):
        """Password not included in the request"""
        newuser = {
            "username": "Promaster"
        }
        resp = self.client().post(
            '/auth/signup',
            data=json.dumps(newuser),
            headers={'content-type': 'application/json'}
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 400, response['Message'])

    def test_login_with_valid_credentials(self):
        """Login with valid username and password"""
        newuser = {
            "user_id": 52156,
            "username": "PromasterXRE",
            "password": "Promaster2018"
        }
        self.client().post(
            '/auth/signup',
            data=json.dumps(newuser),
            headers={'content-type': 'application/json'}
        )
        resp = self.client().post(
            '/auth/login',
            data=json.dumps(newuser),
            headers={'content-type': 'application/json'}
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 200, response['Message'])

    def test_login_with_unregistered_username(self):
        """User enters unregistered username"""
        newuser = {
                'username': 'Promaster00',
                'password': 'Promaster2018'
        }
        resp = self.client().post(
            '/auth/login',
            data = json.dumps(newuser),
            headers = {
                        'content-type': 'application/json'
                    }
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 401)

    def test_login_with_wrong_password(self):
        """Login with wrong password"""
        newuser = {
                'username': 'Johnson784',
                'password': 'Promaster2018'
        }
        resp = self.client().post(
            '/auth/login',
            data = json.dumps(newuser),
            headers = {
                        'content-type': 'application/json'
                    }
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 401, response['Message'])

    def test_login_for_bad_requests(self):
        """Test login with no username or password"""
        newuser = {
                'username': 'Johnson784',
                'password': 'Promaster2018'
        }
        resp = self.client().post(
            '/auth/login',
            data = json.dumps(newuser),
            headers = {
                        'content-type': 'application/json'
                    }
        )
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 401, response['Message'])

#
# if __name__ == "__main__":
#     unittest.main()
