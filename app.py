# Importing the necessary libraries
from functools import wraps
from flask import Flask, abort, session


app = Flask(__name__)



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
