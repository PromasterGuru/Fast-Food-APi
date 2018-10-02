#app/tests/v2/test_views.py

'''Implement classes and methods for testing API Endpoints.'''

import json
import unittest
from app import create_app

# local imports
from .base import BaseTestCase
from app.api.v2.models import FoodOrders


class TestRouteCases(BaseTestCase):
    '''This class represents the orders test cases'''


    def test_config(self):
        """Test configurations"""
        self.assertEqual(self.app.testing, True)

    def test_user_can_view_menu(self):
        """Any user can view the menu"""
        resp = self.view_menu_options()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 200)

    def test_admin_user_can_add_menu_options(self):
        """Any user can add menu option"""
        resp = self.add_menu_options()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], 'Menu item added successfully')
        self.assertEqual(resp.status_code, 201)
        self.assertNotEqual(resp.status_code, 401)

    def test_user_can_post_an_order(self):
        """Any user can post an order"""
        resp = self.post_order()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "Order successfully placed")
        self.assertEqual(resp.status_code, 201)

    def test_users_can_view_their_orders(self):
        """Any user can view their previous orders"""
        resp = self.view_orders()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 200)

    def test_users_can_updated_their_order_status(self):
        """Any user can update their order status"""
        resp = self.update_order_status()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "Order successfully updated")
        self.assertEqual(resp.status_code, 200)

    def test_admin_can_delete_orders(self):
        """Any user can delete orders"""
        resp = self.delete_order()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "Order successfully deleted")
        self.assertEqual(resp.status_code, 200)

if __name__ == "__main__":
    unittest.main()
