#app/api/v2/models.py

"""
Create database entities
"""

import os
from urllib.parse import urlparse
import psycopg2


class DB():
    """Create database tables"""


    def create_con(self):
        """Create database connection"""
        result = os.getenv('DATABASE_URL')
        url = urlparse(result)
        connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname
        )
        return connection

    def create_tables(self):
        """DML scripts for creating the tables"""
        users_tb = """CREATE TABLE IF NOT EXISTS Users(
            user_id serial PRIMARY KEY,
            email varchar(30) NOT NULL,
            username varchar(15) NOT NULL,
            password varchar(250) NOT NULL,
            role varchar(10) DEFAULT 'User'
        );"""

        meals_tb = """CREATE TABLE IF NOT EXISTS Meals(
            meal_id serial PRIMARY KEY,
            meal_name varchar(25) NOT NULL,
            description varchar(250) NOT NULL,
            unit_price decimal(5,2) NOT NULL
        );"""

        orders_tb = """CREATE TABLE IF NOT EXISTS Orders(
            order_id serial PRIMARY KEY,
            user_id integer NOT NULL,
            meal_id integer NOT NULL,
            description varchar(250),
            quantity int NOT NULL,
            order_date date NOT NULL,
            status varchar(15),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
            ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
            ON DELETE CASCADE ON UPDATE CASCADE
        );"""
        return [users_tb, meals_tb, orders_tb]

    def init_db(self):
        """Execute the DML scripts to create entities"""

        con = self.create_con()
        cursor = con.cursor()
        try:
            for query in self.create_tables():
                cursor.execute(query)
                con.commit()

            result = {"Message": "Database connection established successfully"}
            print(result)


            admin_user = """INSERT INTO Users(user_id, email, username, password, role)
                            VALUES(1, 'pmutondo12@gmail.com', 'Promaster',
                                   'sha256$2Um2FMvb$e61bf3f929321a777fb3d52b28f384b2a8c48c4810380279d1f933a767b14e62',
                                    'Admin');"""

            menu_option = """INSERT INTO Meals(meal_id, meal_name, description,
                                         unit_price)
                             VALUES(1, 'Pizza', 'Meat and veggie options to keep
                              the whole family smiling.', 2.55);"""

            order = """INSERT INTO Orders(order_id, user_id, meal_id, description,
                                          quantity, order_date, status) VALUES(1, 1,
                                          1, 'Grade 5 hot and pasted Pizza', 5,
                                          '2018-09-30 22:57:36','New');"""

            data = [admin_user, menu_option, order]

            query = """SELECT * FROM Users;"""
            query1 = """SELECT * FROM Meals;"""
            query2 = """SELECT * FROM Orders;"""
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.execute(query1)
            meals = cursor.fetchall()
            cursor.execute(query2)
            orders = cursor.fetchall()
            if not users and not meals and not orders:
                for each in data:
                    cursor.execute(each)
                    con.commit()
                con.close()
        except (Exception, psycopg2.DatabaseError) as error:
            result = {"Message": error}
            print(result)

        finally:
            if con is not None:
                con.close()
