#app/api/v1models.py

'''Food order class with storage model and methods.'''

class FoodOrders():
    '''Food order with storage and methods.'''


    def __init__(self):
        '''Initialize food orders.'''
        self.food_orders = []

    def get_orders(self):
        '''Return all the food orders'''
        return self.food_orders
