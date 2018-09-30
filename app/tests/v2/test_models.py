#app/tests/v2/test_models.py

"""
Test storage models
"""
import unittest

#local import
from app.api.v2.models import FoodOrders
from app import create_app

class TestModels(unittest.TestCase):
    """Test storage models"""


    def setUp(self):
        """Define and Initalize test variables"""
        self.app = create_app(config_name="testing")
        self.orders = FoodOrders()
        self.client = self.app.test_client

    def test_config(self):
        """Test configurations"""
        self.assertEqual(self.app.testing, True)
        self.assertNotEqual(self.app.testing, False)

    def test_meals_model_is_empty_initially(self):
        """Test the food orders data structure is initially empty"""
        self.assertNotEqual(len(self.orders.get_menu()), 0)

    def test_orders_model_is_empty_initially(self):
        """Test the food orders data structure is initially empty"""
        self.assertNotEqual(len(self.orders.get_orders()), 0)

# if __name__ == '__main__':
#     unittest.main()
