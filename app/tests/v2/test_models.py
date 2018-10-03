# #app/tests/v2/test_models.py
#
# """
# Test storage models
# """
# import unittest
#
# #local import
# from app.api.v2.models import FoodOrders
# from app import create_app
# from .base import BaseTestCase
#
# class TestModels(BaseTestCase):
#     """Test storage models"""
#
#
#     def test_config(self):
#         """Test configurations"""
#         self.assertEqual(self.app.testing, True)
#         self.assertNotEqual(self.app.testing, False)
#
#     def test_meals_model_has_one_dummy_record(self):
#         """Meals table has one record initially"""
#         self.assertNotEqual(len(self.orders.get_menu()), 1)
#
#     def test_orders_model_has_one_dummy_record(self):
#         """Orders table has one record initially"""
#         self.assertNotEqual(len(self.orders.get_orders()), 1)
#
#     def test_users_model_has_one_dummy_record(self):
#         """Users table has one record initially"""
#         self.assertNotEqual(len(self.orders.get_users()), 1)
#
# # if __name__ == '__main__':
# #     unittest.main()
