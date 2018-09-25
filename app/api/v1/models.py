#app/api/v1models.py

'''Food order class with storage model and methods.'''

class FoodOrders():
    '''Food order with storage and methods.'''


    def __init__(self):
        '''Initialize food orders.'''
        self.food_orders = []
        self.users = []

    def set_users(self, uname, password):
        '''Add new users'''
        self.users[uname] = password

    def get_users(self):
        '''Return a dictionary of users'''
        return self.users

    def set_orders(self, orders):
        '''Add new orders'''
        self.food_orders.append(orders)

    def get_orders(self):
        '''Return a list of food orders'''
        return self.food_orders
