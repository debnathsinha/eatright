import os
import jinja2
from oauth2client.client import OAuth2WebServerFlow
from google.appengine.api import urlfetch

urlfetch.set_default_fetch_deadline(60)

IS_DEV_APPSERVER = 'development' in os.environ.get('SERVER_SOFTWARE', '').lower()

# Duplicate from auth.py, delete at first chance!
OAUTH_SCOPE = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    # Add other requested scopes.
]

ROOT_PATH = os.path.dirname(__file__)
GMAILYTICS_TEMPLATE_PATH = os.path.join(ROOT_PATH,"templates") 
JINJA_ENV = jinja2.Environment(
                               loader=jinja2.FileSystemLoader(GMAILYTICS_TEMPLATE_PATH),
                                extensions=['jinja2.ext.autoescape'],
                                autoescape=True)
IS_DEV_APPSERVER = 'development' in os.environ.get('SERVER_SOFTWARE', '').lower()

# Duplicate from auth.py, delete at first chance!
OAUTH_SCOPE = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    # Add other requested scopes.
]

constructor_kwargs = {
                          'access_type' : 'offline',
                          'approval_prompt': 'auto',
                          'include_granted_scopes': 'true',
                    }

if IS_DEV_APPSERVER:
    constructor_kwargs = {
                          'access_type' : 'offline',
                          'approval_prompt': 'force',
                          'include_granted_scopes': 'true',
                          }
    SIGNIN_FLOW = OAuth2WebServerFlow(client_id='429823268566-ttujjigj6opvo30015nsq1179d9nakuv.apps.googleusercontent.com',
                                      client_secret='ZniaetP4Wv7dOujqiWaEGb9R',
                                      scope='https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/gmail.readonly',
                                      redirect_uri='http://localhost:8080/oauth2callback',
                                      **constructor_kwargs)
else:
    SIGNIN_FLOW = OAuth2WebServerFlow(client_id='1074396901150-3pp8nfc2e4ob2gna2o5qd5is2gfidev9.apps.googleusercontent.com',
                                      client_secret='Q0e6WQoc-RRYShbqiO2r4uqE',
                                      scope='https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/gmail.readonly',
                                      redirect_uri='https://www.cosight.io/oauth2callback',
                                      **constructor_kwargs)


MobileJWTSecret = "eatright"

TEST_CONTEXT = False
