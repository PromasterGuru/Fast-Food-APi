#app/api/v1/views.py

'''
Implementation of API EndPoint
'''
import os
import datetime
from flask import jsonify
from flask import request
from flask import abort
#from flask import Blueprint
from flask_restful import Resource
from flask_restful import Api
from .models import FoodOrders
from app import app

#api_url = Blueprint('api', __name__)
api = Api(app)

class Resource(Resource):
    """Throws a method not allowed error"""
    def get(self, *args, **kwargs):
        """Abort with error code 405"""
        abort(405)


class Orders(Resource):
    """Class that holds the API endpoints that deals with multiple orders"""



    orders = FoodOrders()

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
        self.orders.get_orders().append(new_order)
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
        self.validate_request(orderId)[0]['status'] = request.json['status']
        result = {"Order": self.validate_request(orderId)[0]}
        response = jsonify(result)
        response.status_code = 200 #OK

api.add_resource(Orders,'/api/v1/orders')
api.add_resource(Order,'/api/v1/orders/<int:orderId>')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
