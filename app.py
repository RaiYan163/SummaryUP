# Importing the necessary libraries
from functools import wraps
from flask import Flask, abort, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_login import LoginManager

import os
load_dotenv()



app = Flask(__name__)

database_uri = os.getenv("DATABASE_URI")

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")

# # SSL configuration in JSON format
# ssl_config = {
#     "ca": "/etc/ssl/cert.pem"
# }

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# Database Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'connect_args': ssl_config}

# # Convert SSL configuration to a query string
# ssl_query_string = "&".join([f"{key}={value}" for key, value in ssl_config["ssl"].items()])

# # Append SSL query string to the URI
# app.config['SQLALCHEMY_DATABASE_URI'] += f"?{ssl_query_string}"

#create the database
db = SQLAlchemy(app)



from models import*

login_manager = LoginManager()
login_manager.login_view = '/'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))





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
