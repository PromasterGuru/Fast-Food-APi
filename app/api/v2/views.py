#app/api/v2/views.py

'''
Implementation of API EndPoint
'''
import os
import re
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, make_response
from flask_restful import Resource
from functools import wraps

#local import
from .models import FoodOrders

def user_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        '''Validate user token'''
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        #token = request.args.get('token')

        if not token:
            result = {"Message": "Token is missing, please login."}
            response = jsonify(result)
            response.status_code = 404 #Not found
            return response

        try:
            data = jwt.decode(token,os.getenv('SECRET'))
            users = FoodOrders().get_users()
            user_id = [current_user for current_user in users
                 if current_user['user_id'] == data['user_id']
                 ]
            cur_user_id = user_id[0]['user_id']
        except Exception as error:
            result = {"Message": "Your token is Invalid, please login."}
            response = jsonify(result)
            response.status_code = 401 #Un authorized
            return response

        return f(*args, cur_user_id, **kwargs)

    return decorated


class Role():
    """Get user role"""


    users = FoodOrders()
    def get_role(self, id):
        """"Get user role using user id"""
        users = self.users.get_users()
        for user_id in users:
            if user_id['user_id'] == id:
                user_role = user_id['user_id']
        if (user_role != "Admin"):
            result = {"Message": "The requested URL requires Admin privilege"}
            response = jsonify(result)
            response.status_code = 401 #Un authorized
            return response


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
                    result = {"Message":self.users.add_user(uname, password_hash)}
                    response = jsonify(result)
                    response.status_code = 201 #Created
                else:
                    result = {"Message": "Account is already registered"}
                    response = jsonify(result)
                    response.status_code = 401 #An authorized
        return response


class Login(Resource):
    '''Authenticates users'''



    users = FoodOrders()

    def post(self):
        '''Login'''
        if (not request.json
            or not request.json['username']
            or not request.json['password']):
            result = {"Message": "User not verified, Please login again!"}
            response = jsonify(result)
            response.status_code = 401 #OK
        else:
            users = self.users.get_users()
            uname = request.json['username']
            password = request.json['password']
            user = [user for user in users if user['username'] == uname]
            if not user:
                result = {"Message": "Username not registered, please register!!!"}
                response = jsonify(result)
                response.status_code = 401  #An authorized
            else:
                if check_password_hash(user[0]['password'],password):
                    user = [user for user in users if user['username'] == uname]
                    token = jwt.encode({'user_id': user[0]['user_id'],
                                        'exp': datetime.datetime.utcnow()
                                        + datetime.timedelta(minutes=15)
                                        },os.getenv('SECRET'))
                    result = {"Message": "Login successful, Welcome %s" %(uname)
                            , "Token": token.decode('UTF-8')}
                    response = jsonify(result)
                    response.status_code = 200 #OK
                else:
                    result = {"Message": "Username or password was incorrect!"}
                    response = jsonify(result)
                    response.status_code = 401 #An authorized
        return response


class Menu(Resource):
    """Holds the food menu methods"""


    menu = FoodOrders()
    roles = Role()

    def get(self):
        """Get available menu"""
        menu = self.menu.get_menu()
        if not menu:
            result = {"Message": "Menu not availlable"}
            response = jsonify(result)
            response.status_code = 404 #Not found
            return response
        else:
            result = {"Message": self.menu.get_menu()}
            response = jsonify(result)
            response.status_code = 200 #OK
            return response

    @user_token
    def post(self, cur_user_id):
        """Add a meal option to the menu."""
        if (self.roles.get_role(cur_user_id) != "Admin"):
            result = {"Message": "The requested URL requires Admin privilege"}
            response = jsonify(result)
            response.status_code = 401 #Un authorized
            return response
        else:
            if (not request.json or "name" not in request.json
                or 'description' not in request.json or 'price' not in request.json
                ):
                result = {"Message": "Please recheck your menu fieds and try again"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
                return response
            else:
                meal_name = request.json['name']
                meal_desc = request.json['description']
                meal_price = request.json['price']
                result = {"Message": self.menu.create_menu(meal_name, meal_desc, meal_price)}
                response = jsonify(result)
                response.status_code = 201 #Created
                return response

class UserOrders(Resource):
    """Class that holds the API endpoints that deals with multiple orders"""


    orders = FoodOrders()
    roles = Role()

    @user_token
    def get(self, cur_user_id):
        '''Users can view their order history.'''
        order = self.orders.get_orders()
        if order:
            user_order = [user_order for user_order in
                          order if user_order['user_id'] == cur_user_id]
            result = {"Message": user_order}
            response = jsonify(result)
            response.status_code = 200 #OK
        else:
            result = {"Message": "No orders found"}
            response = jsonify(result)
            response.status_code = 404 #OK
        return response

    @user_token
    def post(self, cur_user_id):
        '''Use can place a new order'''
        if not request.json or  "meal_id"  not in request.json:
            result = {"Message": "Unknown request!!"}
            response = jsonify(result)
            response.status_code = 400 #Bad request
        else:
            user_id = cur_user_id
            item = request.json['meal_id']
            desc = request.json['description']
            meal = [meal for meal in self.orders.get_menu()
                    if meal['meal_id'] == item
                    ]
            if not meal:
                result = {"Message": "Meal not found"}
                response = jsonify(result)
                response.status_code = 404 #Not found
            orders = self.orders.get_orders()
            order = [order for order in orders
                     if(
                         order['user_id'] == user_id and
                         order['meal_id'] == item and
                         order['description'] == desc
                         )
                     ]
            if not order:
                order_id = len(orders) + 1
                qty = request.json['quantity']
                order_date = str(datetime.datetime.now())[:19]
                status = "New"
                result = self.orders.create_orders(order_id, user_id, item, desc, qty, order_date, status)
                response = jsonify({"Message": result})
                response.status_code = 201 #Created
            else:
                result = {"Message": "Dublicate orders not allowed!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
        return response


class AdminOrder(UserOrders):
    '''Holds API endpoints with admin specific orders'''


    orders = UserOrders().orders

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

    @user_token
    def get(self, cur_user_id, order_id):
        if (self.roles.get_role(cur_user_id) != "Admin"):
            result = {"Message": "The requested URL requires Admin privilege"}
            response = jsonify(result)
            response.status_code = 401 #Un authorized
            return response
        else:
            '''Fetch a specific order'''
            if not self.validate(order_id):
                result = {"Message": "No order found for order id %d" %(order_id)}
                response = jsonify(result)
                response.status_code = 404 #Not found
            else:
                order = self.check_order(order_id)
                result = {"Message": order}
                response = jsonify(result)
                response.status_code = 200 #OK
            return response

    @user_token
    def post(self, cur_user_id, order_id):
        '''Admin user can place a new order'''
        if (self.roles.get_role(cur_user_id) != "Admin"):
            result = {"Message": "The requested URL requires Admin privilege"}
            response = jsonify(result)
            response.status_code = 401 #Un authorized
            return response
        else:
            if (not request.json or "order_id" not in request.json
                or "meal_id" not in request.json
                or "quantity" not in request.json
                ):
                result = {"Message": "Unknown request!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
            else:
                user_id = cur_user_id,
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
                    status = "New"
                    result = self.orders.create_orders(order_id, user_id, item, desc, qty, order_date, status)
                    response = jsonify({"Message": result})
                    response.status_code = 201 #Created
                else:
                    result = {"Message": "Dublicate orders not allowed!!"}
                    response = jsonify(result)
                    response.status_code = 400 #Bad request
            return response

    @user_token
    def put(self, cur_user_id, order_id):
        '''Update the status of an order'''
        if (self.roles.get_role(cur_user_id) != "Admin"):
            result = {"Message": "The requested URL requires Admin privilege"}
            response = jsonify(result)
            response.status_code = 401 #Un authorized
            return response
        else:
            if not self.validate(order_id):
                result = {"Message": "No order found for id %d" %(order_id)}
                response = jsonify(result)
                response.status_code = 404 #Not found
            else:
                order = self.check_order(order_id)
                order_status = ["New", "Processing", "Cancelled", "Complete"]
                status = request.json['status']
                if status in order_status:
                    result = {"Message": self.orders.update_orders(order_id,status)}
                    response = jsonify(result)
                    response.status_code = 200 #OK
                else:
                    result = {"Message": "Unkown order status"}
                    response = jsonify(result)
                    response.status_code = 200 #OK
            return response

    @user_token
    def delete(self, cur_user_id, order_id):
        '''Delete an order'''
        if (self.roles.get_role(cur_user_id) != "Admin"):
            result = {"Message": "The requested URL requires Admin privilege"}
            response = jsonify(result)
            response.status_code = 401 #Un authorized
            return response
        else:
            if not self.validate(order_id):
                result = {"Message": "No order found for id %d" %(order_id)}
                response = jsonify(result)
                response.status_code = 404 #Not found
            else:
                result = {"Message": self.orders.delete_orders(order_id)}
                response = jsonify(result)
                response.status_code = 200 #OK
            return response


class AdminOrders(AdminOrder):
    '''Allow admin to get all orders'''


    @user_token
    def get(self, cur_user_id):
        '''Fetch all orders'''
        if (self.roles.get_role(cur_user_id) != "Admin"):
            result = {"Message": "The requested URL requires Admin privilege"}
            response = jsonify(result)
            response.status_code = 401 #Un authorized
            return response
        else:
            orders = self.orders.get_orders()
            if not orders:
                result = {"Message": "No orders found"}
                response = jsonify(result)
                response.status_code = 404 #Not found
            else:
                result = {"Message": orders}
                response = jsonify(result)
                response.status_code = 200 #OK
            return response
