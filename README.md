[![Build Status](https://travis-ci.org/PromasterGuru/Fast-Food-API-Endpoints.svg?branch=dev)](https://travis-ci.org/PromasterGuru/Fast-Food-API-Endpoints)  [![Coverage Status](https://coveralls.io/repos/github/PromasterGuru/Fast-Food-API-Endpoints/badge.svg?branch=dev)](https://coveralls.io/github/PromasterGuru/Fast-Food-API-Endpoints?branch=dev)   [![Maintainability](https://api.codeclimate.com/v1/badges/997b349df6f552d352b5/maintainability)](https://codeclimate.com/github/PromasterGuru/Fast-Food-API-Endpoints/maintainability)    [![GitHub license](https://img.shields.io/github/license/PromasterGuru/Fast-Food-APi.svg)](https://github.com/PromasterGuru/Fast-Food-APi/blob/master/LICENSE)


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
    <td>Register a user</td>
    <td>POST</td>
    <td>/auth/signup</td>
  </tr>
  <tr>
    <td>Login a user</td>
    <td>POST</td>
    <td>/auth/login</td>
  </tr>
  <tr>
    <td>Place an order for food.</td>
    <td>POST</td>
    <td>/users/orders</td>
  </tr>
  <tr>
    <td>Get the order history for a particular user.</td>
    <td>GET</td>
    <td>/users/orders</td>
  </tr>
  <tr>
    <td>Get all orders</td>
    <td>GET</td>
    <td>/orders/</td>
  </tr>
  <tr>
    <td>Add a specific order</td>
    <td>POST</td>
    <td>/orders/orderId</td>
  </tr>
  <tr>
    <td>Update the status  of an order</td>
    <td>PUT</td>
    <td>orders/orderId</td>
  </tr>
  <tr>
    <td>Get available menu</td>
    <td>GET</td>
    <td>/menu</td>
  </tr>
  <tr>
    <td>Add a meal option to the menu.</td>
    <td>POST</td>
    <td>/menu</td>
  </tr>
  <tr>
    <td>Delete order.</td>
    <td>DELETE</td>
    <td>/menu</td>
  </tr>
  <tr>
    <td>Add a meal option to the menu.</td>
    <td>POST</td>
    <td>/orders/orderId</td>
  </tr>
  <tr>
    <td>Update user</td>
    <td>PUT</td>
    <td>/users/userId</td>
  </tr>
</table>

### How to compile and test it locally
1. Clone the project: `git clone https://github.com/PromasterGuru/Fast-Food-APi.git">`
2. cd to project directory: `cd Fast-Food-API-Endpoints`
3. Install virtual environment(if not installed): `pip install virtualenv`
4. Create and activate virtual environment: `virtualenv venv` then `source venv/bin/activate`
5. Install project dependencies :`pip install -r requirements.txt`
6. Start postgres and create a database by the name fastfoodfast: <br>
  `sudo -su postgres psql postgres`<br>
  `psql -c 'create database fastfoodfast;' -U postgres`

### Test the app on postman
a. Register to get an account<br>
b. Login to generate a  token<br>
c. Use this token to access the endpoints endpoint where necessary
