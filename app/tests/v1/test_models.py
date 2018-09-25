#app/tests/v1/test_models.py

"""
Test storage models
"""
import unittest

#local import
from app.api.v1.models import FoodOrders
from app import create_app

class TestModels(unittest.TestCase):
    """Test storage models"""


    def setUp(self):
        """Define and Initalize test variables"""
        self.app = create_app(app_config_name="testing")
        self.orders = FoodOrders()
        self.client = self.app.test_client

    def test_config(self):
        """Test configurations"""
        self.assertEqual(self.app.testing, True)
        self.assertNotEqual(self.app.testing, False)

    def test_users_model_is_empty_initially(self):
        """Test the user data structure is initially empty"""
        self.assertEqual(len(self.orders.get_users()), 0)
        self.assertNotEqual(len(self.orders.get_users()), 1)

    def test_orders_model_is_empty_initially(self):
        """Test the food orders data structure is initially empty"""
        self.assertEqual(len(self.orders.get_orders()), 0)
        self.assertNotEqual(len(self.orders.get_orders()), 1)

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
        self.assertEqual(len(self.orders.get_orders()), 1)
        self.assertNotEqual(len(self.orders.get_orders()), 0)

    def test_push1_one_user_record(self):
        """Test when one user is registered"""
        user = {
            "user_id": 1,
            "username": "Promaster",
            "password": "Pmutondo12@gmail.com"
        }
        self.orders.set_users(user)
        self.assertEqual(len(self.orders.get_users()), 1)
        self.assertNotEqual(len(self.orders.get_users()), 0)
#
# if __name__ == '__main__':
#     unittest.main()
