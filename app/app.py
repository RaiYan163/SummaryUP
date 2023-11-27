# app.py
from flask import Flask
from routes import routes_blueprint
from auth import auth_blueprint

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(routes_blueprint)
app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
