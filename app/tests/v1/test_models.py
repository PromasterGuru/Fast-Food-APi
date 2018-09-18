#app/tests/v1/test_models.py

"""
Test storage models
"""
import unittest
import json
import os

#local import
from app.api.v1.models import FoodOrders
from app import create_app

class TestModels(unittest.TestCase):
    """Test storage models"""


    def setUp(self):
        """Define and Initalize test variables"""
        self.app = create_app(app_config_name = "testing")
        self.orders = FoodOrders()
        self.client = self.app.test_client

    def test_config(self):
        """Test configurations"""
        self.assertEqual(self.app.testing, True)
        self.assertNotEqual(self.app.testing, False)

    def test_user_model_isEmpty_init(self):
        """Test the user data structure is initially empty"""
        self.assertEqual(0,len(self.orders.get_orders()))
        self.assertNotEqual(1,len(self.orders.get_orders()))

    def test_user_model_isEmpty_init(self):
        """Test the food orders data structure is initially empty"""
        self.assertEqual(0,len(self.orders.get_orders()))
        self.assertNotEqual(1,len(self.orders.get_users()))

    def test_push1_one_food_order_record(self):
        """Test when one order record is added"""
        order = {
            "id": 1,
            "order_item": "Ugali",
            "description": "Hot when packed",
            "quantity": 5,
            "status": "Pedding"
        }
        self.orders.set_orders(order)
        self.orders.set_users("paul","mathenge")
        self.assertEqual(1,len(self.orders.get_orders()))
        self.assertNotEqual(0,len(self.orders.get_orders()))

    def test_push1_one_user_record(self):
        """Test when one user is registered in the database"""
        self.assertEqual(1,len(self.orders.get_users()))
        self.assertNotEqual(0,len(self.orders.get_users()))

if __name__ == '__main__':
    unittest.main()
