#app/api/v2/views.py

'''
Implementation of API EndPoint
'''


import re
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, make_response, abort
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)


#local import
from .models import FoodOrders


class Role(FoodOrders):
    """Get user role"""


    def user_auth(self, id):
        """"Authorize user based on their roles"""
        users = self.get_users()
        user_id = [user_id for user_id in users if user_id['user_id'] == id]
        if not user_id:
            result = {"Message": "No user found for the requested user id"}
            response = jsonify(result)
            response.status_code = 401 #Un authorized
            return response
        else:
            role = user_id[0]['role']
            if role != "Admin":
                abort(401, "Access Denied : The requested URL requires Admin privilege")


class Register(Resource):
    """Resigsters new users"""


    users = FoodOrders()

    def post(self):
        '''Register new users'''
        if (not request.json
                or "email" not in request.json
                or "username" not in request.json
                or "password" not in request.json
           ):
            result = {"Message": "Some very important fields are missing, "
                                 +"please confirm and fill them"}
            response = jsonify(result)
            response.status_code = 400 #Bad request
        else:
            email = request.json['email']
            uname = request.json['username']
            password = request.json['password']

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                result = {"Message": "Your email address is invalid!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
            elif len(uname) < 6:
                result = {"Message": "Username must contain atleast 6 characters!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
            elif len(password) < 8:
                result = {"Message": "password must have more than 8 characters!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
            elif re.search('[0-9]', password) is None:
                result = {"Message": "password must contain a at least one number!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
            elif re.search('[A-Z]', password) is None:
                result = {"Message": "password must contain a capital letter!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
            else:
                users = self.users.get_users()
                user = [user for user in users
                        if user['username'] == uname
                        or user['email'] == email
                        ]

                if not user:
                    user_id = len(users) + 1
                    password_hash = generate_password_hash(password, method='sha256')
                    result = {"Message":self.users.add_user(user_id, email, uname, password_hash)}
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
                or "username" not in request.json
                or "password" not in request.json):
            result = {"Message": "Username or password not found in the request!"}
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
                if check_password_hash(user[0]['password'], password):
                    user = [user for user in users if user['username'] == uname]
                    access_token = create_access_token(identity=user[0]['user_id'])
                    refresh_token = create_refresh_token(identity=user[0]['user_id'])

                    # token = jwt.encode({'user_id': user[0]['user_id'],
                    #                     'exp': datetime.datetime.utcnow()
                    #                     + datetime.timedelta(minutes=15)
                    #                     },os.getenv('SECRET')).decode('UTF-8')
                    result = {"Message": "Login successful, Welcome %s" %uname
                                                           , 'access_token': access_token
                                                           # , 'refresh_token': refresh_token
                                                           }
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
        result = {"Message": self.menu.get_menu()}
        response = jsonify(result)
        response.status_code = 200 #OK
        return response

    @jwt_required
    def post(self):
        """Add a meal option to the menu."""
        cur_user_id = get_jwt_identity()
        self.roles.user_auth(cur_user_id)
        if (not request.json
                or "name" not in request.json
                or 'description' not in request.json
                or 'unit_price' not in request.json
           ):
            result = {"Message": "Please recheck your menu fieds and try again"}
            response = jsonify(result)
            response.status_code = 400 #Bad request
            return response
        else:
            menu_id  = len(self.menu.get_menu())+1
            meal_name = request.json['name']
            meal_desc = request.json['description']
            meal_price = request.json['unit_price']
            meals = self.menu.get_menu()
            meal = [meal for meal in meals if meal['meal_name'] == meal_name]
            if not meal:
                result = {"Message": self.menu.create_menu(menu_id, meal_name, meal_desc, meal_price)}
                response = jsonify(result)
                response.status_code = 201 #Created
                return response
            else:
                result = {"Message": "Meal name already exists, please use"
                                     +" another meal name"}
                response = jsonify(result)
                response.status_code = 403 #Request denied
        return response

class Users(Login):
    """Users role managment"""

    @jwt_required
    def put(self, user_id):
        """Update user role"""
        cur_user_id = get_jwt_identity()
        if(not request.json
           or 'role' not  in request.json
           ):
            result = {"Message": "Please enter all the required fields"}
            response = jsonify(result)
            response.status_code = 400 #Bad request
            return response
        else:
            role = request.json['role']
            users = self.users.get_users()
            user_ids = [user_ids for user_ids in users
                        if user_ids['user_id'] == user_id
                        ]
            if not user_ids:
                result = {"Message": "User not found!"}
                response = jsonify(result)
                response.status_code = 404 #Not found request
                return response
            else:
                result = {"Message": self.users.update_users(user_id, role)}
                response = jsonify(result)
                response.status_code = 200 #Ok
                return response


class UserOrders(Resource):
    """Class that holds the API endpoints that deals with multiple orders"""


    orders = FoodOrders()

    @jwt_required
    def get(self):
        '''Users can view their order history.'''
        cur_user_id = get_jwt_identity()
        order = self.orders.get_orders()
        if order:
            user_order = [user_order for user_order in
                          order if user_order['user_id'] == cur_user_id]
            if not user_order:
                result = {"Message": "No order history found."}
                response = jsonify(result)
                response.status_code = 404 #OK
            else:
                result = {"Message": user_order}
                response = jsonify(result)
                response.status_code = 200 #OK
        else:
            result = {"Message": "No orders found"}
            response = jsonify(result)
            response.status_code = 404 #OK
        return response

    @jwt_required
    def post(self):
        '''Use can place a new order'''
        cur_user_id = get_jwt_identity()
        if (not request.json
                or  "meal_id"  not in request.json
                or "address" not in request.json
                or "quantity" not in request.json
           ):
            result = {"Message": "Unknown request! some fields missing!"}
            response = jsonify(result)
            response.status_code = 400 #Bad request
        else:
            user_id = cur_user_id
            item = request.json['meal_id']
            address = request.json['address']
            qty = request.json['quantity']
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
                         order['address'] == address and
                         order['status'] == 'New'
                         )
                     ]
            if not order:
                order_id = len(orders) + 1
                order_date = str(datetime.datetime.now())[:19]
                status = "New"
                result = self.orders.create_orders(order_id, user_id, item,
                                                   address, qty, order_date, status)
                response = jsonify({"Message": result})
                response.status_code = 201 #Created
            else:
                result = {"Message": "Dublicate orders not allowed!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
        return response


class AdminOrder(Resource):
    '''Holds API endpoints with admin specific orders'''


    orders = FoodOrders()
    roles = Role()

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

    @jwt_required
    def get(self, order_id):
        """Get specific order by order id"""
        cur_user_id = get_jwt_identity()
        self.roles.user_auth(cur_user_id)
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

    @jwt_required
    def post(self, order_id):
        '''Admin user can place a new order'''
        cur_user_id = get_jwt_identity()
        self.roles.user_auth(cur_user_id)
        if (not request.json
                or "meal_id" not in request.json
                or "address" not in request.json
                or "quantity" not in request.json
           ):
            result = {"Message": "Invalid request, bad request format!"}
            response = jsonify(result)
            response.status_code = 400 #Bad request
            return response
        else:
            user_id = cur_user_id,
            item = request.json['meal_id']
            address = request.json['address']
            qty = request.json['quantity']
            order = [order for order in self.orders.get_orders()
                     if(
                         order['user_id'] == user_id and
                         order['meal_id'] == item and
                         order['quantity'] == qty and
                         order['status'] == 'New'
                         )
                     ]
            if not order:
                order_date = str(datetime.datetime.now())[:19]
                status = "New"
                result = self.orders.create_orders(order_id, user_id, item,
                                                   address, qty, order_date, status)
                response = jsonify({"Message": result})
                if result == "Order successfully placed":
                    response.status_code = 201 #Created
                elif (result == "No meal found for meal_id %s"%order_id):
                    response.status_code = 404 #Not found
                else:

                    response.status_code = 400 #Bad request
                return response
            else:
                result = {"Message": "Dublicate orders not allowed!!"}
                response = jsonify(result)
                response.status_code = 400 #Bad request
                return response

    @jwt_required
    def put(self, order_id):
        '''Update the status of an order'''
        cur_user_id = get_jwt_identity()
        self.roles.user_auth(cur_user_id)
        if not self.validate(order_id):
            result = {"Message": "No order found for id %d" %order_id}
            response = jsonify(result)
            response.status_code = 404 #Not found
        else:
            order_status = ["New", "Processing", "Cancelled", "Complete"]
            if request.json['status'] in order_status:
                status = request.json['status']
                result = {"Message": self.orders.update_orders(order_id, status)}
                response = jsonify(result)
            else:
                result = {"Message": "Unkown order status. Availlable status are"
                          +" " +str(order_status)}
                response = jsonify(result)
                response.status_code = 200 #OK
        return response

    @jwt_required
    def delete(self, order_id):
        '''Delete an order'''
        cur_user_id = get_jwt_identity()
        self.roles.user_auth(cur_user_id)
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


    @jwt_required
    def get(self):
        '''Fetch all orders'''
        cur_user_id = get_jwt_identity()
        self.roles.user_auth(cur_user_id)
        orders = self.orders.get_orders()
        result = {"Message": orders}
        response = jsonify(result)
        response.status_code = 200 #OK
        return response
