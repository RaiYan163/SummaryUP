from flask import Flask
import os

def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the secret key
    app.secret_key = 'your_secret_key'

    # This should be removed in production
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Register Blueprints
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app
