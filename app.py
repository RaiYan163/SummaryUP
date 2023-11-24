# Importing the necessary libraries
import os
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from functools import wraps
import google.auth.transport.requests

from flask import Flask, abort, render_template, redirect, url_for, session, request, jsonify


app = Flask(__name__)
app.secret_key = "secret key"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" #This is for bypassing HTTPS. Contact with me in case of deployment. -Saugata

GOOGLE_CLIENT_ID = "662083614675-hj166l9f1hr0m7bd2ktsbt534q7g0he0.apps.googleusercontent.com"

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secrets.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback")#Huge Careful with this one. Call me if you have any questions, Raiyan. -Saugata



def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'google_id' not in session:
            return abort(401)  # Authorization required
        else:
            return function(*args, **kwargs)  # Forward the arguments to the original function
    return wrapper


@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
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
    

@app.route('/')
def index():
    #return render_template('index.html')
    return render_template('index.html')

@app.route('/dashboard')
@login_is_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard2')
@login_is_required
def dashboard2():
    return render_template('dashboard_saved_summaries.html')

@app.route('/summary')
@login_is_required
def summary():
    return render_template('summary.html')

@app.route('/user')
@login_is_required
def user():
    return "user page"

@app.route('/settings')
@login_is_required
def settings():
    return render_template('settings.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")



@app.route('/protected_area')
@login_is_required
def protected_area():
    return "<a href = '/logout'>Logout</a> <br><h4> Hello, your email is {} and <br> your name is {}.<\h4>".format(session['email'], session['name']) #This is just a test. You can delete or use this. -Saugata
#The protected area is not done yet. I will do it later. Let me know the info from the gmail. -Saugata
if __name__ == '__main__':
    app.run(debug=True)
