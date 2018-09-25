#app/api/v1/views.py

'''
Implementation of API EndPoint
'''
import os
import re
import datetime
from flask import jsonify, request
from flask_restful import Resource
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
# from functools import wraps

#local import
from .models import FoodOrders

current_user_id = 0

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         '''Validate user token'''
#         token = None
#
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#         #token = request.args.get('token')
#
#         if not token:
#             result = {"Message": "Token is missing, please login."}
#             response = jsonify(result)
#             response.status_code = 404 #Not found
#             return response
#
#         try:
#             data = jwt.decode(token,os.getenv('SECRET'))
#             current_user = data['user_id']
#             current_user_id = current_user
#         except Exception as error:
#             result = {"Message": "Your token is Invalid, please login."}
#             response = jsonify(result)
#             response.status_code = 401 #Un authorized
#             return response
#
#         return f(current_user, *args, **kwargs)
#
#     return decorated


class Register(Resource):
    """Resigsters new users"""


    users = FoodOrders()

    def post(self):
        '''Register new users'''
        if (not request.json
                or not "username" in request.json
                or not "password" in request.json
           ):
            result = {"Message": "Invalid username or password"}
            response = jsonify(result)
            response.status_code = 400 #Bad request
        else:
            uname = request.json['username']
            password = request.json['password']
            if not uname:
                result = {"Message": "Please enter your username!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
            elif len(uname) < 6:
                result = {"Message": "Username must contain atleast 6 characters!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
            elif not password:
                result = {"Message": "Please enter your password!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
            elif len(password) < 8:
                result = {"Message": "password must have more than 8 characters!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
            elif re.search('[0-9]', password) is None:
                result = {"Message": "password must contain a atleast one number!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
            elif re.search('[A-Z]', password) is None:
                result = {"Message": "password must contain a capital letter!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
            else:
                users = self.users.get_users()
                user = [user for user in users if user['username'] == uname]
                if not user:
                    password_hash = generate_password_hash(password, method='sha256')
                    user_id = len(users)+1
                    new_user = {
                        "user_id": user_id,
                        "username": uname,
                        "password": password_hash
                    }
                    self.users.set_users(new_user)
                    result = {"Message":"%s have been registered successfully"%(uname)}
                    response = jsonify(result)
                    response.status_code = 201 #Created
                else:
                    result = {"Message": "User is already registered, please login"}
                    response = jsonify(result)
                    response.status_code = 401 #An authorized
        return response


class Login(Register):
    '''Authenticates users'''


    def get(self):
        '''Login'''
        auth = request.authorization
        uname = auth.username
        password = auth.password
        if not auth or not uname or not password:
            result = {"Message": "User not verified, Please login again!"}
            response = jsonify(result)
            response.status_code = 401 #OK
            return response
        else:
            users = self.users.get_users()
            user = [user for user in users if user['username'] == uname]
            if not user:
                result = {"Message": "Username not registered, please register!!!"}
                response = jsonify(result)
                response.status_code = 401  #An authorized
                return response
            else:
                if check_password_hash(user[0]['password'], password):
                    users = self.users.get_users()
                    user_id = len(users)+1
                    current_user_id = user_id
                    token = jwt.encode({'user_id': user_id,
                                        'exp': datetime.datetime.utcnow()
                                               + datetime.timedelta(minutes=15)
                                        }, os.getenv('SECRET')
                                       )
                    result = {"Message": "Login successful, Welcome %s" %(uname)
                                         , "Token": token.decode('UTF-8')}
                    response = jsonify(result)
                    response.status_code = 200 #OK
                    return response
                else:
                    result = {"Message": "Wrong username or password!"}
                    response = jsonify(result)
                    response.status_code = 401 #Unauthorized
                    return response


class Orders(Resource):
    """Class that holds the API endpoints that deals with multiple orders"""


    orders = FoodOrders()

    # @token_required
    def get(self):
        '''Get all the orders.'''
        order = self.orders.get_orders()
        if order:
            result = {"Message": self.orders.get_orders()}
            response = jsonify(result)
            response.status_code = 200 #OK
        else:
            result = {"Message": "No orders found"}
            response = jsonify(result)
            response.status_code = 404 #OK
        return response

    # @token_required
    def post(self):
        '''Place a new order'''
        if not request.json or not "order_item" in request.json:
            result = {"Message": "Unknown request!!"}
            response = jsonify(result)
            response.status_code = 400 #Bad request
        else:
            orders = self.orders.get_orders()

            item = request.json['order_item']
            desc = request.json['description']
            order = [order for order in orders
                     if(
                         order['user_id'] == current_user_id and
                         order['order_item'] == item and
                         order['description'] == desc
                         )
                     ]
            order_id = len(orders)+1

            if not order:
                user_id = current_user_id
                qty = request.json['quantity']
                order_date = str(datetime.datetime.now())[:19]
                status = "Pedding"
                new_order = {
                    "user_id": user_id,
                    "order_id": order_id,
                    "order_item": item,
                    "description": desc,
                    "quantity": qty,
                    "order_date": order_date,
                    "status": status
                }
                self.orders.set_orders(new_order)
                result = {"Message": "Order placed successfully,"
                                     + " we will get back to you in 5 minutes"}
                response = jsonify(result)
                response.status_code = 201 #Created
            else:
                result = {"Message": "Dublicate orders not allowed!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
        return response


class Order(Orders):
    '''Holds API endpoints with specific orders'''


    def validate(self, order_id):
        """Ensure user enters a valid order"""
        found = False
        for order in self.orders.get_orders():
            if order['order_id'] == order_id:
                found = True
        return found

    def check_order(self, order_id):
        """Get user request"""
        order = [order for order in self.orders.get_orders()
                 if order['order_id'] == order_id
                 ]
        return order

    # @token_required
    def get(self, order_id):
        '''Fetch a specific order'''
        if not self.validate(order_id):
            result = {"Message": "No order found for id %d" %(order_id)}
            response = jsonify(result)
            response.status_code = 404 #Not found
        else:
            order = self.check_order(order_id)
            result = {"Message": order}
            response = jsonify(result)
            response.status_code = 200 #OK
        return response

    # @token_required
    def put(self, order_id):
        '''Update the status of an order'''
        if not self.validate(order_id):
            result = {"Message": "No order found for id %d" %(order_id)}
            response = jsonify(result)
            response.status_code = 404 #Not found
        else:
            order = self.check_order(order_id)
            status = request.json['status']
            order[0]['status'] = status
            result = {"Message": "Order successfully updated"}
            response = jsonify(result)
            response.status_code = 200 #OK
        return response

    # @token_required
    def delete(self, order_id):
        '''Delete an order'''
        if not self.validate(order_id):
            result = {"Message": "No order found for id %d" %(order_id)}
            response = jsonify(result)
            response.status_code = 404 #Not found
        else:
            orders = self.orders.get_orders()
            order_id = [order_id for order_id in range(len(orders))
                        if orders[order_id] == self.check_order(order_id)
                        ]
            orders.pop(0)
            result = {"Message": "Order deleted successfully"}
            response = jsonify(result)
            response.status_code = 200 #OK
        return response
