#app/api/v2/models.py

import os
import psycopg2
from flask import json
from .database import DB

'''Food order class with storage model and methods.'''

class FoodOrders():
    '''Food order with storage and methods.'''


    def __init__(self):
        '''Initialize variables'''
        self.con = DB().create_con()
        self.cursor = self.con.cursor()

    def set_users(self, uname, password):
        '''Add new users'''
        try:
            query = """INSERT INTO Users(username,password) VALUES(%s, %s);"""
            self.cursor.execute(query,(uname,password))
            self.con.commit()
            return ("%s registered successfully"%(uname))
        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error %s"%(error))

    def get_users(self):
        '''Return a dictionary of users'''
        try:
            query = """SELECT username,password FROM Users;"""
            self.cursor.execute(query)
            resp = self.cursor.fetchall()
            return dict(resp)
        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error %s"%(error))

    def set_orders(self, orders):
        '''Add new orders'''
        pass#self.food_orders.append(orders)

    def get_orders(self):
        '''Return a list of food orders'''
        pass#return self.food_orders
