import webapp2
import json
import jinja2
import os
import jwt
from oauth2client.client import OAuth2WebServerFlow
from OAuth2CallbackHandler import OAuth2CallbackHandler
from Constants import SIGNIN_FLOW
from Constants import JINJA_ENV
from Constants import MobileJWTSecret
from Constants import IS_DEV_APPSERVER
from SessionBasedHandler import SessionBasedHandler
import pdb

class MainPage(webapp2.RequestHandler):
    def get(self):
        token = jwt.encode({'a':'1'}, MobileJWTSecret)
        if IS_DEV_APPSERVER:
            template_values = { 'login_url' : '/api/login'}
        else:
            template_values = { 'login_url' : 'https://www.cosight.io/api/login'}
        template = JINJA_ENV.get_template("index.html")
        self.response.write(template.render(template_values))

class LoginHandler(SessionBasedHandler):
    def get(self):
        email = self.request.get("login_email")
        SIGNIN_FLOW.params.update({ 'login_hint': email})
        auth_url = SIGNIN_FLOW.step1_get_authorize_url()
        return self.redirect(auth_url)            

class DishPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        json_data = open("sample.json").read()
        data = json.loads(json_data)
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps(data))

routes = [ ('/', MainPage),
           (r'/api/login', LoginHandler),
           (r'/oauth2callback', OAuth2CallbackHandler),
           ('/dishes', DishPage)
       ]


config = {}
config['webapp2_extras.sessions'] = {
                                     'secret_key' : 'eatright',
                                     'cookie_name': 'eatrightsession'
                                     }
def app():
    from google.appengine.ext.appstats import recording
    app = webapp2.WSGIApplication(routes, config = config, debug=True)
    app = recording.appstats_wsgi_middleware(app)
    return app

application = app()

def main():
    # Set the logging level in the main function
    # See the section on Requests and App Caching for information on how
    # App Engine reuses your request handlers when you specify a main function
    logging.getLogger().setLevel(logging.DEBUG)

if __name__ == '__main__':
    main()
