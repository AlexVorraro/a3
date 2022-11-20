
from flask import Blueprint, render_template, request, flash
import boto3
from boto3.dynamodb.conditions import Key
from werkzeug.utils import redirect
from zenora import APIClient
from config import TOKEN, CLIENT_SECRET, OAUTH_URL, REDIRECT_URI

import requests
import requests.auth
import urllib.parse
from uuid import uuid4
from flask import abort
#tokens removed on github
REDDIT_CLIENT_ID = ''
REDDIT_CLIENT_SECRET = ''
REDDIT_REDIRECT_URI = "http://ec2-44-211-133-5.compute-1.amazonaws.com/reddit_callback"


client = APIClient(TOKEN, client_secret=CLIENT_SECRET)
TABLE_NAME = "Users"
region = 'us-east-1'
logged=''
email=''


dynamodb = boto3.resource('dynamodb',aws_access_key_id='',
                          aws_secret_access_key='',
                          aws_session_token='',
                          region_name=region)
table = dynamodb.Table(TABLE_NAME)
auth = Blueprint('auth', __name__)

def passingEmail():
    try:
        print("passing"+auth.email)
        return auth.email
    except:
        return ''

def passing():

    try:
        print("passing"+auth.logged)
        return auth.logged
    except:
        return ''

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form.get('email')

        password = request.form.get('password')
        response = table.query(
            KeyConditionExpression=Key('Email').eq(email)
        )

        print(response)

        try:
            response["Items"][0]['Email']

            if response["Items"][0]['password'] == password:
                print("sto uaa")
                auth.logged=response["Items"][0]['user_name']
                auth.email=response["Items"][0]['Email']
                print("wee"+auth.logged)
                return redirect('/fortnite')
            flash("Email or password invalid", category='error')
        except:
            flash("Email or password invalid", category='error')

    return render_template("login.html",OAUTH_URL=OAUTH_URL,reddit_url=make_authorization_url())


@auth.route('/logout')
def logout():

    auth.logged=''
    auth.email=''
    return redirect("/")


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        response = table.query(
            KeyConditionExpression=Key('Email').eq(email)
        )
        try:
            response["Items"][0]['Email']
            flash("Email already exists", category='error')
        except:
            response = table.put_item(
                Item={
                    'Email': email,
                    'password': password,
                    'user_name': name,
                }
            )

            return redirect('/')



    return render_template("sign_up.html")

@auth.route('oauth/callback')
def callback():
    code = request.args['code']
    access_token = client.oauth.get_access_token(code, REDIRECT_URI).access_token
    bearer_client = APIClient(access_token, bearer=True)
    current_user = bearer_client.users.get_current_user()
    email = current_user.email
    name = current_user.username
    password = 'passwordNotAvailable-CanLoginOnlyWithDiscordCredentials'
    response = table.query(
        KeyConditionExpression=Key('Email').eq(email)
    )
    try:
        response["Items"][0]['Email']
        auth.logged = name
        auth.email = email
        return redirect('/fortnite')
    except:
        response = table.put_item(
            Item={
                'Email': email,
                'password': password,
                'user_name': name,
            }
        )

        return redirect('/fortnite')

    return redirect('/fortnite')

def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    state = str(uuid4())
    params = {"client_id": REDDIT_CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDDIT_REDIRECT_URI,
              "duration": "temporary",
              "scope": "identity"}
    url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params)
    return url

@auth.route('/reddit_callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    email='NoValidEmailFor'+str(get_username(access_token))
    name = get_username(access_token)
    password = 'passwordNotAvailable-CanLoginOnlyWithRedditCredentials'
    response = table.query(
        KeyConditionExpression=Key('Email').eq(email)
    )
    try:
        response["Items"][0]['Email']
        auth.logged = name
        auth.email = email
        return redirect('/fortnite')
    except:
        response = table.put_item(
            Item={
                'Email': email,
                'password': password,
                'user_name': name,
            }
        )

        return redirect('/fortnite')

def is_valid_state(state):
    return True


def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDDIT_REDIRECT_URI}
    headers = base_headers()
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]

def get_username(access_token):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    me_json = response.json()
    print(me_json)
    return me_json['name']

def base_headers():
    return {"User-Agent": user_agent()}


def user_agent():
    return "app by /u/AngruDuck552"
