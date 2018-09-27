#app/api/v2/models.py

"""
Create database entities
"""

import os
from urllib.parse import urlparse
import psycopg2
from flask import jsonify



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
        users = """CREATE TABLE IF NOT EXISTS Users(
            user_id serial PRIMARY KEY,
            username varchar(15) NOT NULL,
            password varchar(100) NOT NULL,
            role varchar(10) DEFAULT 'User'
        );"""

        meals = """CREATE TABLE IF NOT EXISTS Meals(
            meal_id serial PRIMARY KEY,
            meal_name varchar(25) NOT NULL,
            description varchar(250) NOT NULL,
            unit_price decimal(5,2) NOT NULL
        );"""

        orders = """CREATE TABLE IF NOT EXISTS Orders(
            order_id serial PRIMARY KEY,
            user_id integer NOT NULL,
            meal_id integer NOT NULL,
            description varchar(250),
            quantity int NOT NULL,
            order_date date NOT NULL,
            status varchar(15),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
        );"""
        return [users, meals, orders]

    def init_db(self):
        """Execute the DML scripts to create entities"""

        con = self.create_con()
        cursor = con.cursor()
        try:
            for query in self.create_tables():
                cursor.execute(query)
            cursor.close()
            con.commit()
            result = {"Message": "Database connection established successfully"}
            print(result)

        except (Exception, psycopg2.DatabaseError) as error:
            result = {"Message": error}
            print(result)

        finally:
            if con is not None:
                con.close()
