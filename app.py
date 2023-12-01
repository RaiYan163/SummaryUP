# Importing the necessary libraries
from functools import wraps
from flask import Flask, abort, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://xzlj0gufspd4pn0mbtnj:pscale_pw_QSVQJ5xWskVu2rCmDmwZYK2UYB90lE0l5Ypca1ddbRs@aws.connect.psdb.cloud/python-practice'


#Creating the database
db = SQLAlchemy(app)

#starting the login from here
login = LoginManager(app)




app.secret_key = "secret key"

def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'google_id' not in session:
            return abort(401)  # Authorization required
        else:
            return function(*args, **kwargs)  # Forward the arguments to the original function
    return wrapper


from controller import * #Need to import after the app and login_is_required is initialized. -Saugata

if __name__ == '__main__':
    app.run(debug=True)
