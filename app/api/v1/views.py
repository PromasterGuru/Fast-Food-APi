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
    """Class that holds the API endpoints"""

    orders = FoodOrders()

    def get(self):
        '''Get all the orders.'''
        result = {"Orders": self.orders.get_orders()}
        response = jsonify(result)
        response.status_code = 200 #OK
        return response

api.add_resource(Orders,'/api/v1/orders')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
