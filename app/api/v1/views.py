#app/api/v1/views.py

'''
Implementation of API EndPoint
'''
import os
import datetime
import hashlib
from flask import jsonify,request,abort
from flask_restful import Resource,Api
from flask_httpauth import HTTPDigestAuth

#local imports
from .models import FoodOrders

auth = HTTPDigestAuth()

class Resource(Resource):


    """Throws error messages"""
    def get(self, *args, **kwargs):
        """Abort with error code 405"""
        abort(405)


class Register(Resource):
    """Resigsters new users"""


    users = FoodOrders()

    def validate_credentials(self):
        '''Validate user inputs'''
        if (not request.json or not "username" in request.json
                             or not "password" in request.json
                             ):
                             abort(400)

    def post(self):
        '''Register new users'''
        self.validate_credentials()
        uname = request.json['username']
        password = hashlib.md5(request.json['password'].encode()).hexdigest()
        if uname in self.users.get_users():
            abort(401) #An authorized
        else:
            self.users.set_users(uname,password)
            result = {"User":"You have successfully registered as "+uname}
            response = jsonify(result)
            response.status_code = 201 #Created
            return response


class Login(Register):
    '''Authenticates users'''


    @auth.get_password
    def get(self,username,password):
        '''Login'''
        if not(username or password):
            abort(400) #Bad request
        elif username not in self.users.get_users():
            abort(401) #An authorized
        else:
            uname = username
            password = hashlib.md5(password.encode()).hexdigest()
            if self.users.get_users()[uname] == password:
                return True
            return False


class Orders(Resource):
    """Class that holds the API endpoints that deals with multiple orders"""


    orders = FoodOrders()

    #@auth.login_required
    def get(self):
        '''Get all the orders.'''
        result = {"Orders": self.orders.get_orders()}
        response = jsonify(result)
        response.status_code = 200 #OK
        return response

    def post(self):
        '''Place a new order'''
        if not request.json or not "order_item" in request.json:
            abort(400) #Bad Request
        if not self.orders.get_orders():
            order_id = 1
        else:
            order_id = self.orders.get_orders()[-1]['id'] + 1
        new_order = {
            "id": order_id,
            "order_item": request.json['order_item'],
            "description": request.json['description'],
            "quantity": request.json['quantity'],
    	    "order_date":str(datetime.datetime.now())[:19],
            "status": "Pedding"
        }
        self.orders.set_orders(new_order)
        result = {"Order": new_order}
        response = jsonify(result)
        response.status_code = 201 #Created
        return response


class Order(Orders):
    '''Holds API endpoints with specific orders'''


    food_orders = Orders.orders.get_orders()

    def validate_request(self,orderId):
        order = [order for order in self.food_orders if order['id'] == orderId]
        if not order:
            abort(404) #Not Found
        else:
            return order

    def get(self,orderId):
        '''Fetch a specific order'''
        self.validate_request(orderId)
        result = {"Order": self.validate_request(orderId)}
        response = jsonify(result)
        response.status_code = 200 #OK
        return response

    def put(self,orderId):
        '''Update the status of an order.'''
        order = self.validate_request(orderId)
        order[0]['status'] = request.json['status']
        result = {"Order": order}
        response = jsonify(result)
        response.status_code = 200 #OK

    def delete(self,orderId):
        '''Delete an order'''
        self.food_orders.remove(
                                self.validate_request(orderId)[0]
                                )
        result = {"Result": self.validate_request(orderId)[0]}
        response = jsonify(result)
        response.status_code = 200 #OK
