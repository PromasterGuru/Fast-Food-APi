#app/tests/v2/test_views.py

'''Implement classes and methods for testing API Endpoints.'''

import json
import unittest
from app import create_app

# local imports
from .base import BaseTestCase


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

    # def test_admin_user_can_add_menu_options(self):
    #     """Any user can view the menu"""
    #     resp = self.add_menu_options()
    #     response = json.loads(resp.data.decode('utf-8'))
    #     self.assertTrue(resp.content_type == 'application/json')
    #     self.assertEqual(response['Message'], 'Menu item added successfully')
    #     self.assertEqual(resp.status_code, 201)

    # def test_config(self):
    #     """Test configurations"""
    #     self.assertEqual(self.app.testing, True)
    #
    # def test_attempt_to_get_orders_when_not_logged_in(self):
    #     '''User attempts to view all their orders when they haven't logged in'''
    #     resp = self.client().get(
    #         '/orders/',
    #         headers=dict(
    #             Authorization= self.user_token
    #             )
    #     )
    #     response = json.loads(resp.data.decode('utf-8'))
    #     self.assertEqual(resp.status_code, 404)
    #     self.assertEqual("Token is missing, please login.", response["Message"])
    #
    # # def test_view_menu(self):
    # #     """User can view menu items"""
    # #     newuser = {
    # #         'username': 'Promaster@@@',
    # #         'password': 'Promaster2018'
    # #     }
    # #     resp = self.client().post(
    # #         '/auth/login',
    # #         data=json.dumps(newuser),
    # #         headers={'content-type': 'application/json'}
    # #     )
    # #     response = json.loads(resp.data.decode('utf-8'))
    # #     self.user_token = response['Token']
    # #     menu = self.client().get(
    # #         '/orders',
    # #        headers=dict(Authorization="Bearer " + self.user_token)
    # #        )
    # #     resp = json.loads(menu.data.decode())
    # #     self.assertEqual(resp.status_code, self.user_token)
    #
    # # def test_attempt_to_get_orders_when_empty(self):
    #     '''Test for no records found when no order have beeen placed'''
    #     resp = self.client().get(
    #         '/orders',
    #         headers={P
    #             'Authorization' : self.user_token
    #         }
    #     )
    #     response = json.loads(resp.data.decode('utf-8'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertNotEqual("No order found", response['Message'])

#     def test_user_can_place_an_order_if_not_dublicate(self):
#         '''Test API can create a new order (POST request)'''
#         newuser = {
#                 'username': 'Promaster00',
#                 'password': 'Promaster2018'
#         }
#         login_resp = self.client().post(
#             '/auth/login',
#             data=json.dumps(dict(newuser)),
#             content_type='application/json'
#         )
#         user_login = json.loads(login_resp.data.decode())
#         resp = self.client().get(
#             '/orders/',
#             headers=dict(
#                 Authorization='Bearer ' + json.loads(
#                     login_resp.data.decode()
#                 )['x-access-token']
#             )
#         )
#         self.assertEqual(resp.status_code, 404, user_login["Message"])
#         self.client().post(
#             '/api/v1/orders',
#             data=json.dumps(self.order),
#             headers={'content-type': 'application/json'}
#         )
#         resp = self.client().post(
#             '/api/v1/orders',
#             data=json.dumps(self.order),
#             headers={'content-type': 'application/json'}
#         )
#         response = json.loads(resp.data.decode('utf-8'))
#         self.assertEqual(resp.status_code, 400, response["Message"])
# #
#     def test_attempt_to_place_orders_without_order_item(self):
#         '''Test user attempts to place Unknown order i.e. without the order item'''
#         self.order = {
#             'description': 'These are Pieces of deep-fried, potatoes.',
#             'quantity': 7,
#             'status': 'Accepted'
#         }
#         resp = self.client().post(
#             '/api/v1/orders',
#             data=json.dumps(self.order),
#             headers={'content-type': 'application/json'}
#         )
#         response = json.loads(resp.data.decode('utf-8'))
#         self.assertEqual(resp.status_code, 400, response["Message"])
#
#     def test_user_can_get_all_orders(self):
#         '''Test API can return all the orders (GET request)'''
#         resp = self.client().get(
#             '/api/v1/orders',
#             headers={'content-type': 'application/json'}
#         )
#         response = json.loads(resp.data.decode('utf-8'))
#         self.assertEqual(resp.status_code, 200, response["Message"])
#
#     def test_user_can_fetch_a_specific_order(self):
#         '''Test API can return a specific order using its id (GET request)'''
#         self.client().post(
#             '/api/v1/orders',
#             data=json.dumps(self.order),
#             headers={'content-type': 'application/json'}
#         )
#         resp = self.client().get(
#             '/api/v1/orders/1',
#             headers={'Content-type': 'application/json'}
#         )
#         response = json.loads(resp.data.decode('utf-8'))
#         self.assertEqual(resp.status_code, 200, response["Message"])
#
#     def test_user_attempt_to_fetch_un_existing_order(self):
#         '''Test cannot fetch an order that doesen't exist'''
#         self.client().post(
#             '/api/v1/orders',
#             data=json.dumps(self.order),
#             headers={'content-type': 'application/json'}
#         )
#         resp = self.client().get(
#             '/api/v1/orders/2',
#             headers={'Content-type': 'application/json'}
#         )
#         response = json.loads(resp.data.decode('utf-8'))
#         self.assertEqual(resp.status_code, 404, response["Message"])
#
#     def test_user_can_update_order_status(self):
#         '''Test API can modify the status of an order (PUT request)'''
#         self.client().post(
#             '/api/v1/orders',
#             data=json.dumps(self.order),
#             headers={'content-type': 'application/json'}
#         )
#         resp = self.client().put(
#             '/api/v1/orders/1',
#             data=json.dumps({'status': 'Accepted'}),
#             headers={'content-type': 'application/json'}
#         )
#         response = json.loads(resp.data.decode('utf-8'))
#         self.assertEqual(resp.status_code, 200, response["Message"])
#
#     def test_for_attempt_to_update_un_existing_order(self):
#         """Unexisting order cannot be updated"""
#         self.client().post(
#             '/api/v1/orders',
#             data=json.dumps(self.order),
#             headers={'content-type': 'application/json'}
#         )
#         resp = self.client().put(
#             '/api/v1/orders/2',
#             data=json.dumps({'status': 'Accepted'}),
#             headers={'content-type': 'application/json'}
#         )
#         response = json.loads(resp.data.decode('utf-8'))
#         self.assertEqual(resp.status_code, 404, response["Message"])
#
#     def test_user_can_delete_an_order(self):
#         '''Test API can delete an order (DELETE request)'''
#         self.client().post(
#             '/api/v1/orders',
#             data=json.dumps(self.order),
#             headers={'content-type': 'application/json'}
#         )
#         resp = self.client().delete(
#             'api/v1/orders/1',
#             headers={'Content-type': 'application/json'}
#         )
#         response = json.loads(resp.data.decode('utf-8'))
#         self.assertEqual(resp.status_code, 200, response["Message"])
#
#     def test_for_attempt_to_delete_un_existing_order(self):
#         """Unexisting order cannot be updated"""
#         self.client().post(
#             '/api/v1/orders',
#             data=json.dumps(self.order),
#             headers={'content-type': 'application/json'}
#         )
#         resp = self.client().delete(
#             'api/v1/orders/2',
#             headers={'Content-type': 'application/json'}
#         )
#         response = json.loads(resp.data.decode('utf-8'))
#         self.assertEqual(resp.status_code, 404, response["Message"])
#
#     def test_malformed_url_for_place_order(self):
#         '''Test API should return an error: Not found'''
#         resp = self.client().post(
#             '/api/v1/orders/',
#             data=json.dumps(self.order),
#             headers={'content-type': 'application/json'}
#         )
#         self.assertEqual(resp.status_code, 404)
#
#     def test_malformed_url_for_get_all_orders(self):
#         '''Test API should return an error: Not found'''
#         resp = self.client().get(
#             '/api/v1/orders/',
#             headers={'content-type': 'application/json'}
#         )
#         self.assertEqual(resp.status_code, 404)
#
#     def test_malformed_url_for_get_a_specific_order(self):
#         '''Test API should return an error: Not found'''
#         resp = self.client().get(
#             '/api/v1/orders/-1',
#             headers={'content-type': 'application/json'}
#         )
#         self.assertEqual(resp.status_code, 404)
#
#     def test_malformed_url_for_update_an_order(self):
#         '''Test API should return an error: Not found'''
#         resp = self.client().put(
#             '/api/v1/orders/-1',
#             data=json.dumps({'status': 'Accepted'}),
#             headers={'content-type': 'application/json'}
#         )
#         self.assertEqual(resp.status_code, 404)

# if __name__ == "__main__":
#     unittest.main()
