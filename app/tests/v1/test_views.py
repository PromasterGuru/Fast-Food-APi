#app/tests/test_views.py

'''Implement classes and methods for testing API Endpoints.'''

import json
import unittest
from app import app

class RouteTestCases(unittest.TestCase):
    '''This class represents the orders test cases'''

    def setUp(self):
        '''Define variables and initialize app'''
        self.client = app.test_client
        self.order = {
            'order_item': 'Tater tots',
            'description': 'These are Pieces of deep-fried, potatoes.',
            'quantity': 7,
            'status': 'Accepted'
        }

    def test_user_can_place_an_order(self):
        '''Test API can create a new order (POST request)'''
        resp = self.client().post(
            '/api/v1/orders',
            data=json.dumps(self.order),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(resp.status_code, 201, msg='Error: Expected 201')

    def test_user_can_get_all_orders(self):
        '''Test API can return all the orders (GET request)'''
        resp = self.client().get(
            '/api/v1/orders',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(resp.status_code, 200, msg='Error: Expected 200')

    def test_user_can_fetch_a_specific_order(self):
        '''Test API can return a specific order using its id (GET request)'''
        self.client().post(
            '/api/v1/orders',
            data=json.dumps(self.order),
            headers={'content-type': 'application/json'}
        )
        resp = self.client().get(
            '/api/v1/orders/1',
            headers={'Content-type': 'application/json'}
        )
        self.assertEqual(resp.status_code, 200, msg="Error: Expected 200")

    def test_user_can_update_order_status(self):
        '''Test API can modify the status of an order (PUT request)'''
        resp = self.client().put(
            '/api/v1/orders/1',
            data=json.dumps({'status': 'Accepted'}),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(resp.status_code, 202, msg="Error: Expected 202")

    def test_user_can_delete_an_order(self):
        '''Test API can delete an order (DELETE request)'''
        self.client().post(
            '/api/v1/orders',
            data=json.dumps(self.order),
            headers={'content-type': 'application/json'}
        )
        resp = self.client().delete(
            'api/v1/orders/1',
            headers={'Content-type': 'application/json'}
        )
        self.assertEqual(resp.status_code, 204, msg="Error: Expected 204")

    def test_malformed_url_for_place_order(self):
        '''Test API should return an error: Not found'''
        resp = self.client().post(
            '/api/v1/orders/',
            data=json.dumps(self.order),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(resp.status_code, 404, msg='Error: Expected 404')

    def test_malformed_url_for_get_all_orders(self):
        '''Test API should return an error: Not found'''
        resp = self.client().get(
            '/api/v1/orders/',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(resp.status_code, 404, msg='Error: Expected 404')

    def test_malformed_url_for_get_a_specific_order(self):
        '''Test API should return an error: Not found'''
        resp = self.client().get(
            '/api/v1/orders/-1',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(resp.status_code, 404, msg='Error: Expected 404')

    def test_malformed_url_for_update_an_order(self):
        '''Test API should return an error: Not found'''
        resp = self.client().put(
            '/api/v1/orders/-1',
            data=json.dumps({'status': 'Accepted'}),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(resp.status_code, 404, msg="Error: Expected 404")

if __name__ == "__main__":
    unittest.main()
