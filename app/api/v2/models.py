#app/api/v2/models.py

import os
import psycopg2
from flask import json,jsonify
from .database import DB

'''Food order class with storage model and methods.'''

class FoodOrders():
    '''Food order with storage and methods.'''


    def add_user(self, uname, password):
        '''Add new users'''
        con = DB().create_con()
        cursor = con.cursor()
        try:
            query = """INSERT INTO Users(username,password) VALUES(%s, %s);"""
            cursor.execute(query,(uname,password))
            con.commit()
            cursor.close()
            con.close()
            return ("%s registered successfully"%(uname))
        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error %s"%(error))

    def get_users(self):
        '''Return a dictionary of users'''
        con = DB().create_con()
        cursor = con.cursor()
        cur_users = []
        try:
            query = """SELECT user_id, username, password FROM Users;"""
            cursor.execute(query)
            users = cursor.fetchall()
            for user in users:
                my_user = {}
                my_user['user_id'] = user[0]
                my_user['username'] = user[1]
                my_user['password'] = user[2]
                cur_users.append(my_user)
            return cur_users
        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error %s"%(error))

    def create_menu(self, name, description, unit_price):
        """Add new menu item"""
        con = DB().create_con()
        cursor = con.cursor()
        query = """INSERT INTO Meals(meal_name, description, unit_price) VALUES(%s, %s, %s)"""
        try:
            cursor.execute(query,(name, description, unit_price))
            con.commit()
            con.close()
            return "Menu item added successfully"

        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error! %s"%(error))

    def get_menu(self):
        """Get available menu"""
        con = DB().create_con()
        cursor = con.cursor()
        menu = []
        try:
            query = """SELECT * FROM Meals;"""
            cursor.execute(query)
            orders = cursor.fetchall()
            for item in orders:
                meal = {}
                meal['meal_id'] = item[0]
                meal['meal_name'] = item[1]
                meal['description'] = item[2]
                meal['unit_price'] = item[3]
                menu.append(meal)
            return menu
        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error %s"%(error))

    def create_orders(self, order_id, user_id, item, desc, qty, order_date, status):
        '''Add new orders'''
        con = DB().create_con()
        cursor = con.cursor()
        try:
            id = """SELECT*FROM Meals WHERE meal_id = %s;"""
            meal = """SELECT*FROM Orders WHERE user_id = (%s)
                                            and meal_id = (%s)
                                            and description = (%s)
                                            and quantity = (%s)
                                            """
            query = """INSERT INTO Orders(
                                            order_id, user_id, meal_id, description,
                                            quantity, order_date, status
                                        )
                       VALUES(%s, %s, %s, %s, %s, %s, %s);"""
            cursor.execute(id, [item])
            if cursor.fetchall():
                cursor.execute(meal,(user_id, item, desc, qty))
                if not cursor.fetchall() :
                    cursor.execute(query,(order_id, user_id, item, desc, qty, order_date, status))
                    con.commit()
                    cursor.close()
                    con.close()
                    return "Order successfully placed"
                return "Dublicate order not allowed!"
            return "No meal found for meal_id %s"%(item)

        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error! Request denied, please contact admin")

    def get_orders(self):
        '''Return a list of food orders'''
        con = DB().create_con()
        cursor = con.cursor()
        foods = []
        try:
            query = """SELECT * FROM Orders;"""
            cursor.execute(query)
            orders = cursor.fetchall()
            for item in orders:
                order = {}
                order['order_id'] = item[0]
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
        con = DB().create_con()
        cursor = con.cursor()
        query = """UPDATE Orders SET status = %s WHERE order_id = %s;"""
        try:
            cursor.execute(query,(status,id))
            con.commit()
            cursor.close()
            con.close()
            return ("Order successfully updated")
        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error! %s"%(error))

    def delete_orders(self, order_id):
        """Delete an order"""
        con = DB().create_con()
        cursor = con.cursor()
        query = """DELETE FROM Orders WHERE order_id = %s;"""
        try:
            cursor.execute(query,(order_id,))
            con.commit()
            cursor.close()
            con.close()
            return ("Order successfully deleted")
        except (Exception, psycopg2.DatabaseError) as error:
            return ("Error! %s"%(error))
