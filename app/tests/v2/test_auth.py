#app/tests/v2/test_auth.py

'''Implement classes and methods for testing API Endpoints.'''

import json
import unittest
import jwt
import os
from .base import BaseTestCase


class TestAuthentication(BaseTestCase):
    '''This class represents user authentication unit tests'''


    def test_config(self):
        """Test configurations"""
        self.assertEqual(self.app.testing, True)


    def test_user_registration(self):
        """User registration"""
        # Try to register an already registered Account
        resp = self.register_user()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], 'Promaster18 registered successfully')
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertNotEqual(resp.status_code, 200)

    def test_registration_for_existing_user(self):
        """Dublicate accounts"""
        resp = self.register_existing_user()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], 'Account is already registered')
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 401)
        self.assertNotEqual(resp.status_code, 201)

    def test_user_registration_with_invalid_email(self):
        """User registration with invalid email, missing '@'  """
        resp = self.register_user_invalid_email()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "You entered an invalid email address, "
                  +"missing '@' or '.'")
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertNotEqual(resp.status_code, 201)

    def test_user_registration_with_invalid_username(self):
        """User registration with invalid username, less than 6 characters"""
        resp = self.register_user_invalid_username()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "Username must contain atleast 6 characters!!")
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertNotEqual(resp.status_code, 201)

    def test_user_registration_with_short_password(self):
        """User registration with password having less than 8 characters"""
        resp = self.register_user_short_password()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "password must have more than 8 characters!!")
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertNotEqual(resp.status_code, 201)

    def test_user_registration_password_missing_numeric_characters(self):
        """User registration when passord has no numeric characters"""
        resp = self.register_user_non_numeric_password()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "password must contain a at least one number!!")
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertNotEqual(resp.status_code, 201)

    def test_user_registration_password_missing_capital_letters(self):
        """User registration when passord has no capital letters"""
        resp = self.register_user_password_has_no_caps()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "password must contain a capital letter!!")
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertNotEqual(resp.status_code, 201)

    def test_bad_request_for_registration(self):
        """User registration without important fields"""
        resp = self.bad_registration_request()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "Some very important fields are missing, "
                                             +"please confirm and fill them")
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertNotEqual(resp.status_code, 201)


    def test_user_login_token(self):
        """Text a token was generated"""
        resp = self.get_user_token()
        self.assertTrue(resp)

    def test_user_login(self):
        """Test user login with valid credentials"""
        #Test user login after test_user_registration
        resp = self.user_login()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], 'Login successful, Welcome Promaster')
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.status_code, 201)
        self.assertNotEqual(resp.status_code, 400)
        self.assertNotEqual(resp.status_code, 404)
        self.assertNotEqual(resp.status_code, 401)

    def test_user_login_without_username_or_password(self):
        """Test user login with invalid credentials"""
        resp = self.user_invalid_login1()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], 'User not verified, Please login again!')
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 401)
        self.assertNotEqual(resp.status_code, 201)
        self.assertNotEqual(resp.status_code, 400)
        self.assertNotEqual(resp.status_code, 404)
        self.assertNotEqual(resp.status_code, 200)

    def test_user_login_without_username_or_password(self):
        """Test user login with invalid credentials"""
        resp = self.user_invalid_login1()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], 'User not verified, Please login again!')
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 401)
        self.assertNotEqual(resp.status_code, 201)
        self.assertNotEqual(resp.status_code, 400)
        self.assertNotEqual(resp.status_code, 404)
        self.assertNotEqual(resp.status_code, 200)

    def test_user_login_without_username_or_password(self):
        """Test user login with invalid credentials"""
        resp = self.user_invalid_login2()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], 'Username not registered, please register!!!')
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 401)
        self.assertNotEqual(resp.status_code, 201)
        self.assertNotEqual(resp.status_code, 400)
        self.assertNotEqual(resp.status_code, 404)
        self.assertNotEqual(resp.status_code, 200)

    def test_user_login_without_username_or_password(self):
        """Test user login with invalid credentials"""
        resp = self.user_invalid_login3()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], 'Username or password was incorrect!')
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 401)
        self.assertNotEqual(resp.status_code, 201)
        self.assertNotEqual(resp.status_code, 400)
        self.assertNotEqual(resp.status_code, 404)
        self.assertNotEqual(resp.status_code, 200)

    def test_update_user_roles(self):
        """Admin can update user role"""
        resp = self.update_user_role()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], 'Users roles successfully changed to Admin')
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 200)

    def test_bad_request_foer_user_roles_update(self):
        """Bad request for user role update"""
        resp = self.update_user_role_bad_request()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], 'Please enter all the required fields')
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 400)

    def test_update_for_unexisting_user(self):
        """Attempt to update unexisting user"""
        resp = self.update_unexisting_user_role()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "User not found!")
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 404)

# # # if __name__ == "__main__":
# # #     unittest.main()
