[![Build Status](https://travis-ci.org/PromasterGuru/Fast-Food-API-Endpoints.svg?branch=bg-updates-160539838)](https://travis-ci.org/PromasterGuru/Fast-Food-API-Endpoints)  [![Coverage Status](https://coveralls.io/repos/github/PromasterGuru/Fast-Food-API-Endpoints/badge.svg?branch=bg-updates-160539838)](https://coveralls.io/github/PromasterGuru/Fast-Food-API-Endpoints?branch=bg-updates-160539838)   [![Maintainability](https://api.codeclimate.com/v1/badges/997b349df6f552d352b5/maintainability)](https://codeclimate.com/github/PromasterGuru/Fast-Food-API-Endpoints/maintainability)    [![GitHub license](https://img.shields.io/github/license/PromasterGuru/Fast-Food-APi.svg)](https://github.com/PromasterGuru/Fast-Food-APi/blob/master/LICENSE)


# Fast-Food-APi
Creates a set of API endpoints already defined below and use data structures to store data in memory.
<h2>Tools</h2>
1. Server-Side Framework: <a href ="http://flask.pocoo.org/">Flask Python Framework</a><br>
2. Linting Library: <a href ="https://www.pylint.org/">Pylint, a Python Linting Library</a><br>
3. Style Guide: <a href ="https://www.python.org/dev/peps/pep-0008/">PEP8 Style Guide</a><br>
4. Testing Framework: <a href ="https://docs.pytest.org/en/latest/">PyTest, a Python Testing Framework</a><br>

<h2>Endpoints</h2>
<table>
  <tr>
    <th>Functionality</th>
    <th>Method</th>
    <th>Endpoint</th>
  </tr>
  <tr>
    <td>Get all the orders</td>
    <td>GET</td>
    <td>/api/v1/orders</td>
  </tr>
  </tr>
  <tr>
    <td>Fetch a specific order</td>
    <td>GET</td>
    <td>/api/v1/orders/order_id<order_id></td>
  </tr>
  <tr>
    <td>Place a new order</td>
    <td>POST</td>
    <td>/api/v1/orders</td>
  </tr>
  <tr>
    <td>Update the status of an order</td>
    <td>PUT</td>
    <td>/api/v1/orders/order_id</td>
  </tr>
  <tr>
    <td>Delete a specific order</td>
    <td>DELETE</td>
    <td>/api/v1/orders/order_id</td>
  </tr>
  <tr>
    <td>Register for a new account</td>
    <td>POST</td>
    <td>/api/v1/register</td>
  </tr>
  <tr>
    <td>Login to an account</td>
    <td>GET</td>
    <td>/api/v1/login></td>
  </tr>
</table>

<h2> How to compile and test it locally </h2>
1. Clone the project:<br>git clone <a href ="https://github.com/PromasterGuru/Fast-Food-APi.git"></a></i><br>
2. cd to project directory: <br>```cd Fast-Food-API-Endpoints```<br>
3. Install virtual environment(if not installed):<br> ```pip install virtualenv```<br>
4. Create and activate virtual environment:```virtualenv venv```<br>```source venv/bin/activate```<br>
5. Install project dependencies :<b>```pip install -r requirements.txt```<br>
6. Start postgres and create a database by the name <i>fastfoodfast</i><br>
<i>Having started Challenge 3, creating the database will help to solve some error that might occur<br> due to missing database.</i>
```sudo service postgresql start```<br>
```sudo -su postgres```<br>
```create database fastfoodfast```

<h5>Start Flask server on terminal using the following command</h5>
<i>The following commands can also be included in a .env file tongether with the secret key</i><br>
```export FLASK_APP=run.py```<br>
```export FLASK_ENV='testing'```<br>
```export DATABASE_URL='postgresql://postgres:postgres@localhost/fastfoodfast'```<br>
```flask run```
<h2>Test the app on postman (Challenge 2)</h2>
<i>Use the url provided in the first table with each endpoint starting from</i><br>
a. Register to get an account
b. Login to generate a 'x-access-token'
c. Use this token to access any other endpoint
