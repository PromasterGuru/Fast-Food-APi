#app/api/v1/models.py

'''Food order class with storage model and methods.'''

class FoodOrders():
    '''Food order with storage and methods.'''


    def __init__(self):
        '''Initialize food orders.'''
        self.food_orders = []
        self.users = []

    def set_users(self, user):
        '''Add new users'''
        self.users.append(user)

    def get_users(self):
        '''Return a list of all users'''
        return self.users

    def set_orders(self, orders):
        '''Add new orders'''
        self.food_orders.append(orders)

    def get_orders(self):
        '''Return a list of food orders'''
        return self.food_orders
