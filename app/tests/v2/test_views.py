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

    def test_user_cannot_update_unexisting_order_status(self):
        """Attempt to update unexisting order status"""
        resp = self.update_unexisting_order_status()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "No order found for id 98")
        self.assertEqual(resp.status_code, 404)


    def test_admin_can_delete_orders(self):
        """Any user can delete orders"""
        resp = self.delete_order()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "Order successfully deleted")
        self.assertEqual(resp.status_code, 200)

    def test_all_the_required_order_fields_are_entered(self):
        """Bad request order format"""
        resp = self.invalid_order_data()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "Unknown request! some fields missing!")
        self.assertEqual(resp.status_code, 400)

    def test_delete_for_unexisting_order(self):
        """Attempt to delete unexisting order item"""
        resp = self.invalid_delete_request()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "No order found for id 98")
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 404)

    def test_admin_can_view_all_orders(self):
        """View orders"""
        resp = self.view_all_orders()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 200)

    def test_admin_can_place_a_specific_order(self):
        """Admin can place an orders"""
        resp = self.place_specific_order()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertTrue(resp.content_type == 'application/json')
        self.assertEqual(resp.status_code, 201)

    def test_admin_can_place_an_order(self):
        """Admin can place an orders with a specific id"""
        resp = self.place_specific_order()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "Order successfully placed")
        self.assertEqual(resp.status_code, 201)

    def test_admin_order_with_missing_fields(self):
        """Admin order request in bad format"""
        resp = self.place_invalid_specific_order()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "Invalid request, some fields are missing!")
        self.assertEqual(resp.status_code, 400)

    def test_admin_order_unexisting_meal(self):
        """Admin attempt to order unexisting meal"""
        resp = self.order_unexisting_meal()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "No meal found for meal_id 98")
        self.assertEqual(resp.status_code, 400)

    def test_admin_can_get_a_specific_order(self):
        """Admin get a specific order"""
        resp = self.specific_order()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 200)

    def test_attempt_to_view_unexisting_order(self):
        """Attempt to view unexisting order"""
        resp = self.unexisting_order()
        response = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(response['Message'], "No order found for order id 34")
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
