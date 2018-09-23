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
            password varchar(100) NOT NULL
        );"""

        # meals = """CREATE TABLE IF NOT EXISTS Meals(
        #     meal_id serial PRIMARY KEY,
        #     name varchar(25) NOT NULL,
        #     description varchar(250) NOT NULL,
        #     unit_price numeric(3,2) NOT NULL
        # );"""

        orders = """CREATE TABLE IF NOT EXISTS Orders(
            order_id serial PRIMARY KEY,
            user_id integer NOT NULL,
            /*meal_id integer NOT NULL,*/
            order_item varchar(50) NOT NULL,
            description varchar(250),
            quantity int NOT NULL,
            order_date date NOT NULL,
            status varchar(15),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
            /*FOREIGN KEY (meal_id) REFERENCES meals(meal_id)*/
        );"""
        return [users, orders]

    def init_db(self):
        """Execute the DML scripts to create entities"""

        con = self.create_con()
        cursor = con.cursor()
        try:
            for query in self.create_tables():
                cursor.execute(query)
            cursor.close()
            con.commit()
            result = {"Message": "Database connection established"}
            response = jsonify(result)
            response.status_code = 200 #OK

        except (Exception, psycopg2.DatabaseError) as error:
            result = {"Message": error}
            response = jsonify(result)
            response.status_code = 404 #Not found

        finally:
            if con is not None:
                con.close()
        return response
