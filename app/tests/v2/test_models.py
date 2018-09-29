#app/tests/v1/test_models.py

"""
Test storage models
"""
import unittest
import datetime

#local import
from app.api.v2.models import FoodOrders
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

    def test_push1_one_menu_item(self):
        """Test when one order record is added"""
        meal_name = "Fish"
        meal_desc = "Three fried pieces"
        meal_price = 45.00
        self.orders.create_menu(meal_name, meal_desc, meal_price)
        self.assertNotEqual(len(self.orders.get_menu()), 0)

    def test_push1_one_user_record(self):
        """Test when one user is registered"""
        username = "Promaster"
        password = "Pmutondo12@gmail.com"
        self.orders.add_user(username, password)
        self.assertNotEqual(len(self.orders.get_users()), 0)

    # def test_push1_one_food_order_record(self):
    #     """Test when one order record is added"""
    #     order_id = len(self.orders.get_orders())-1
    #     user_id = len(self.orders.get_users())-1
    #     item = len(self.orders.get_menu())-1
    #     desc = "Kenyan modern pizza"
    #     qty= 98
    #     order_date = str(datetime.datetime.now())[:19]
    #     status = "New"
    #     self.orders.create_orders(order_id, user_id, item, desc, qty, order_date, status)
    #     self.assertNotEqual(len(self.orders.get_orders()), 0)

#
# if __name__ == '__main__':
#     unittest.main()
