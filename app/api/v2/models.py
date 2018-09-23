#app/api/v2/models.py

import os
import psycopg2
from flask import json,jsonify
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

    def set_orders(self, user_id, item, desc, qty, order_date, status):
        '''Add new orders'''
        try:
            query = """INSERT INTO Orders(
                                            user_id, order_item, description,
                                            quantity, order_date, status
                                        )
                       VALUES(%s, %s, %s, %s, %s, %s);"""
            self.cursor.execute(query,(user_id, item, desc, qty, order_date, status))
            self.con.commit()
            return ("Order successfully placed")
        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error! %s"%(error))

    def get_orders(self):
        '''Return a list of food orders'''
        foods = []
        try:
            query = """SELECT * FROM Orders;"""
            self.cursor.execute(query)
            orders = self.cursor.fetchall()
            for item in orders:
                order = {}
                order['id'] = item[0]
                order['user_id'] = item[1]
                order['order_item'] = item[2]
                order['description'] = item[3]
                order['quantity'] = item[4]
                order['order_date'] = item[5]
                order['status'] = item[6]
                foods.append(order)
            return foods
        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error %s"%(error))

    def update_orders(self, id, status):
        """Update order status"""
        query = """UPDATE Orders SET status = %s WHERE order_id = %s;"""
        try:
            self.cursor.execute(query,(status,id))
            self.con.commit()
            return ("Order successfully updated")
        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error! %s"%(error))

    def delete_orders(self, order_id):
        """Delete an order"""
        query = """DELETE FROM Orders WHERE order_id = %s;"""
        try:
            self.cursor.execute(query,(order_id,))
            self.con.commit()
            return ("Order successfully deleted")
        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error! %s"%(error))
