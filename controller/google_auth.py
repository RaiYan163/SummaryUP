import os
import requests
import pathlib
import google.auth.transport.requests
import json
import google.oauth2.credentials
from flask import session, redirect
from google.oauth2 import id_token
from flask import abort
from pip._vendor import cachecontrol
from flask import request
from google_auth_oauthlib.flow import Flow


client_secrets_file = os.path.join(pathlib.Path(__file__).parent.parent, "client_secrets.json")

def get_client_id():
    with open(client_secrets_file) as json_file:
        data = json.load(json_file)
        client_id = data['web']['client_id']
        return client_id
    
GOOGLE_CLIENT_ID = get_client_id()




os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" #This is for bypassing HTTPS. Contact with me in case of deployment. -Saugata


def setup_google_auth():
    flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback")
    return flow


def google_login(flow):
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)


def google_callback(flow):
    flow.fetch_token(authorization_response=request.url)
    if not session['state'] == request.args['state']:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session['google_id'] = id_info.get('sub')
    session['name'] = id_info.get('name')
    session['email'] = id_info.get('email')
    session['picture'] = id_info.get('picture')
