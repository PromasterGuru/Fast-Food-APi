#app/api/v2/views.py

'''
Implementation of API EndPoint
'''
import os
import re
import datetime
# import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, make_response
from flask_restful import Resource
# from functools import wraps

#local import
from .models import FoodOrders

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
#             users = FoodOrders().get_users()
#             current_user = [current_user for current_user in users
#                  if current_user['user_id'] == data['user_id']
#                  ]
#         except Exception as error:
#             result = {"Message": "Your token is Invalid, please login."}
#             response = jsonify(result)
#             response.status_code = 401 #Un authorized
#             return response
#
#         return f(current_user, *args, **kwargs)
#
#     return decorated


class RegisterV2(Resource):
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
            elif uname in self.users.get_users():
                result = {"Message": "User is already registered, please login"}
                response = jsonify(result)
                response.status_code = 401 #An authorized
            else:
                password_hash = generate_password_hash(password, method='sha256')
                result = {"Message":self.users.set_users(uname, password_hash)}
                response = jsonify(result)
                response.status_code = 201 #Created
        return response


class LoginV2(RegisterV2):
    '''Authenticates users'''


    def get(self):
        '''Login'''
        if not request.json
         or not request.json['username']
         or not request.json['password']:
            result = {"Message": "User not verified, Please login again!"}
            response = jsonify(result)
            response.status_code = 401 #OK
        else:
            uname = request.json['username']
            password = request.json['password']
            users = self.users.get_users()
            user = [user for user in users if user['username'] == uname]
            if not user:
                result = {"Message": "Username not registered, please register!!!"}
                response = jsonify(result)
                response.status_code = 401  #An authorized
            else:
                if check_password_hash(user[0]['password'],password):
                    users = self.users.get_users()
                    user = [user for user in users if user['username'] == uname]
                    # token = jwt.encode({'user_id': user[0]['user_id'],
                    #                     'exp': datetime.datetime.utcnow()
                    #                     + datetime.timedelta(minutes=15)
                    #                     },os.getenv('SECRET'))
                    result = {"Message": "Login successful, Welcome %s" %(uname)}
                            # , "Token": token.decode('UTF-8')}
                    response = jsonify(result)
                    response.status_code = 200 #OK
                else:
                    result = {"Message": "Username or password was incorrect!"}
                    response = jsonify(result)
                    response.status_code = 401 #An authorized
        return response


class Menu(Resource):
    """Holds the food menu methods"""


    menu = self.menu.get_menu()

    def get(self):
        """Get available menu"""
        if not menu:
            result = {"Message": "Menu not availlable"}
            response = jsonify(result)
            response.status_code = 404 #Not found
            return response
        result = {"Message": self.menu.get_menu()}
        response = jsonify(result)
        response.status_code = 200 #OK
        return response

    def post(self):
        """Add a meal option to the menu."""
        if not request.json or not request.json['name'] or not request.json['description'] or not request.json['price']:
            result = {"Message": "Please input all menu fieds"}
            response = jsonify(result)
            response.status_code = 400 #Bad request
            return jsonify(response)
        meal_name = response.get['name']
        meal_desc = response.get['description']
        meal_price = response.get['price']
        result{"Message": self.menu.set_menu(meal_name, meal_desc, meal_price)}
        response = jsonify(result)
        response.status_code = 201 #Created
        return response

class OrdersV2(Resource):
    """Class that holds the API endpoints that deals with multiple orders"""


    orders = FoodOrders()

    # # @token_required
    def get(self):
        '''User can view their order history.'''
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
        '''Use can place a new order'''
        if not request.json or not "order_item" in request.json:
            result = {"Message": "Unknown request!!"}
            response = jsonify(result)
            response.status_code = 400 #Bad request
        else:
            user_id = current_user[0]['user_id']
            item = request.json['meal_id']
            desc = request.json['description']
            meal = [meal for meal in self.orders.get_menu()
                    if meal['meal_id'] == item
                    ]
            if not meal:
                result = {"Message": "Meal not found"}
                response = jsonify(result)
                response.status_code = 404 #Not found

            order = [order for order in self.orders.get_orders()
                     if(
                         order['user_id'] == user_id and
                         order['meal_id'] == item and
                         order['description'] == desc
                         )
                     ]
            if not order:
                qty = request.json['quantity']
                order_date = str(datetime.datetime.now())[:19]
                status = "Pedding"
                result = self.orders.set_orders(user_id, item, desc, qty, order_date, status)
                response = jsonify({"Message": result})
                response.status_code = 201 #Created
            else:
                result = {"Message": "Dublicate orders not allowed!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
        return response


class OrderV2(OrdersV2):
    '''Holds API endpoints with specific orders'''



    def validate(self, order_id):
        """Ensure user enters a valid order"""
        found = False
        for order in self.orders.get_orders():
            if order['id'] == order_id:
                found = True
        return found

    def check_order(self, order_id):
        """Get user request"""
        order = [order for order in self.orders.get_orders()
                 if order['id'] == order_id
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
    def post(self, order_id):
        '''Use can place a new order'''
        if not request.json or not "order_item" in request.json:
            result = {"Message": "Unknown request!!"}
            response = jsonify(result)
            response.status_code = 400 #Bad request
        else:
            user_id = current_user[0]['user_id']
            item = request.json['meal_id']
            desc = request.json['description']
            meal = [meal for meal in self.orders.get_menu()
                    if meal['meal_id'] == item
                    ]
            if not meal:
                result = {"Message": "Meal not found"}
                response = jsonify(result)
                response.status_code = 404 #Not found

            order = [order for order in self.orders.get_orders()
                     if(
                         order['user_id'] == user_id and
                         order['meal_id'] == item and
                         order['description'] == desc
                         )
                     ]
            if not order:
                qty = request.json['quantity']
                order_date = str(datetime.datetime.now())[:19]
                status = "Pedding"
                result = self.orders.set_orders(order_id, user_id, item, desc, qty, order_date, status)
                response = jsonify({"Message": result})
                response.status_code = 201 #Created
            else:
                result = {"Message": "Dublicate orders not allowed!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
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
            result = {"Message": self.orders.update_orders(order_id,status)}
            response = jsonify(result)
            response.status_code = 200 #OK
        return response
#
#     @token_required
    def delete(self, order_id):
        '''Delete an order'''
        if not self.validate(order_id):
            result = {"Message": "No order found for id %d" %(order_id)}
            response = jsonify(result)
            response.status_code = 404 #Not found
        else:
            result = {"Message": self.orders.delete_orders(order_id)}
            response = jsonify(result)
            response.status_code = 200 #OK
        return response
