#app/api/v2/models.py

import psycopg2
from .database import DB

'''Food order class with storage model and methods.'''

class FoodOrders():
    '''Food order with storage and methods.'''


    def add_user(self, user_id, email, uname, password):
        '''Add new users'''
        con = DB().create_con()
        cursor = con.cursor()
        try:
            query = """INSERT INTO Users(user_id, email, username, password) VALUES(%s, %s, %s, %s);"""
            cursor.execute(query, (user_id, email, uname, password))
            con.commit()
            cursor.close()
            con.close()
            return ("%s registered successfully" %uname)
        except (Exception, psycopg2.DatabaseError) as error:
            return ("A similar request is being processed, change the user ID!")

    def get_users(self):
        '''Return a dictionary of users'''
        con = DB().create_con()
        cursor = con.cursor()
        cur_users = []
        try:
            query = """SELECT user_id, email, username, role, password FROM Users;"""
            cursor.execute(query)
            users = cursor.fetchall()
            for user in users:
                my_user = {}
                my_user['user_id'] = user[0]
                my_user['email'] = user[1]
                my_user['username'] = user[2]
                my_user['role'] = user[3]
                my_user['password'] = user[4]
                cur_users.append(my_user)
            return cur_users
        except (Exception, psycopg2.DatabaseError) as error:
            return ("A similar request is being processed, change the user ID!")

    def create_menu(self, meal_id, name, description, unit_price):
        """Add new menu item"""
        con = DB().create_con()
        cursor = con.cursor()
        query = """INSERT INTO Meals(meal_id, meal_name, description, unit_price) VALUES(%s, %s, %s, %s)"""
        try:
            cursor.execute(query,(meal_id, name, description, unit_price))
            con.commit()
            con.close()
            return "Menu item added successfully"

        except (Exception, psycopg2.DatabaseError) as error:
            return ("A similar request is being processed, change the menu ID!")

    def get_menu(self):
        """Get available menu"""
        con = DB().create_con()
        cursor = con.cursor()
        menu = []
        try:
            query = """SELECT * FROM Meals;"""
            cursor.execute(query)
            orders = cursor.fetchall()
            if not orders:
                return "Sorry, we have no menu availlable for the moment."
            for item in orders:
                meal = {}
                meal['meal_id'] = item[0]
                meal['meal_name'] = item[1]
                meal['description'] = item[2]
                meal['unit_price'] = str(item[3])
                menu.append(meal)
            return menu
        except (Exception, psycopg2.DatabaseError) as error:
            return ("A similar request is being processed, change the menu ID!")

    def create_orders(self, order_id, user_id, item, addr, qty, order_date, status):
        '''Add new orders'''
        con = DB().create_con()
        cursor = con.cursor()
        try:
            id = """SELECT*FROM Meals WHERE meal_id = %s;"""
            user_order_id = """SELECT order_id FROM Orders WHERE order_id = %s;"""
            orders_id = """SELECT MAX(order_id) FROM Orders;"""
            cursor.execute(user_order_id, [order_id])
            if cursor.fetchall():
                order_id +=  1
            query = """INSERT INTO Orders(
                                            order_id, user_id, meal_id, address,
                                            quantity, order_date, status
                                        )
                       VALUES(%s, %s, %s, %s, %s, %s, %s);"""
            cursor.execute(id, [item])
            meals = cursor.fetchall()
            if not meals:
                return "No meal found for meal_id %s" %item
            cursor.execute(query,(order_id, user_id, item, addr, qty,
                                  order_date, status))
            con.commit()
            cursor.close()
            con.close()
            return "Order successfully placed"

        except (Exception, psycopg2.DatabaseError) as error:
            return ("A similar request is being processed, change the order ID!")

    def get_orders(self):
        '''Return a list of food orders'''
        con = DB().create_con()
        cursor = con.cursor()
        foods = []
        try:
            query = """SELECT * FROM Orders;"""
            cursor.execute(query)
            orders = cursor.fetchall()
            if not orders:
                return "No orders found"
            for item in orders:
                order = {}
                order['order_id'] = item[0]
                order['user_id'] = item[1]
                order['meal_id'] = item[2]
                order['address'] = item[3]
                order['quantity'] = item[4]
                order['order_date'] = item[5]
                order['status'] = item[6]
                foods.append(order)
            return foods
        except (Exception, psycopg2.DatabaseError) as error:
            return ("A similar request is being processed, change the order ID!")

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
            return ("A similar request is being processed, change the order ID!")

    def update_users(self, user_id, role):
        """Update order status"""
        con = DB().create_con()
        cursor = con.cursor()
        query = """UPDATE Users SET role = %s WHERE user_id = %s;"""
        try:
            cursor.execute(query,(role,user_id))
            con.commit()
            cursor.close()
            con.close()
            return "User role successfully changed to %s" %role
        except (Exception, psycopg2.DatabaseError) as error:
            return ("A similar request is being processed, change the user ID!")

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
            return ("A similar request is being processed, change the order ID!")

    def drop_tables(self):
        """Reset test db"""
        con = DB().create_con()
        cursor = con.cursor()
        drp_orders = """drop table orders cascade;"""
        drp_meals = """drop table meals cascade;"""
        drp_users = """drop table users cascade;"""
        queries = [drp_orders, drp_meals, drp_users]
        for query in queries:
            cursor.execute(query)
            con.commit()
        cursor.close()
        con.close()
