# auth.py
import os
import pathlib
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from flask import Flask, redirect, Blueprint, session, request, abort
from functools import wraps
import requests
from pip._vendor import cachecontrol

# Initialize Flask app
auth_blueprint = Blueprint('auth_blueprint', __name__)
auth_blueprint.secret_key = "secret_key"



os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" #This is for bypassing HTTPS. Contact with me in case of deployment. -Saugata

# Google OAuth Configuration
GOOGLE_CLIENT_ID = "662083614675-hj166l9f1hr0m7bd2ktsbt534q7g0he0.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secrets.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback")#Huge Careful with this one. Call me if you have any questions, Raiyan. -Saugata

# Decorator for routes that require login
def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'google_id' not in session:
            return abort(401)  # Authorization required
        else:
            return function(*args, **kwargs)# Forward the arguments to the original function
    return wrapper

# OAuth routes
@auth_blueprint.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@auth_blueprint.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session['state'] == request.args['state']: #for defence against CSRF
        abort(500)  # State does not match!
    
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    #The name and email of the user is stored in the session
    session['google_id'] = id_info.get('sub')
    session['name'] = id_info.get('name')
    session['email'] = id_info.get('email')
    return redirect("/dashboard")


@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect("/")

