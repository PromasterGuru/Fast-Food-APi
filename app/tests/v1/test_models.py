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

    def test_isEmpty_init(self):
        """Test the data structures are initially empty"""
        self.assertEqual(0,len(self.orders.get_orders()))
        self.assertEqual(0,len(self.orders.get_users()))

    def test_push1_record(self):
        """Test when one record is added"""
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
        self.assertEqual(1,len(self.orders.get_users()))

if __name__ == '__main__':
    unittest.main()
