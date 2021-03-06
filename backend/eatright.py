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
from services.GmailService import build_gmail_service_for_user
from RawEmailModel import RawEmailModel
import lxml.html as lh
from lxml import etree
from UserModel import User
import re
import logging
import httplib2
from apiclient.discovery import build
from google.appengine.ext import ndb

class ItemModel(ndb.Model):
    user_id = ndb.StringProperty()
    item_name = ndb.StringProperty()
    item_qty = ndb.StringProperty()
    item_price = ndb.StringProperty()

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

class FetchEmailHandler(SessionBasedHandler):
    def post(self):
        user_id = self.request.get("user_id")
        credentials = User.get_credentials_from_user_id(user_id)
        if user_id:
            gmail_service = build("gmail", "v1", http=credentials.authorize(httplib2.Http()))
            #gmail_service = build_gmail_service_for_user(user_id)
            response = gmail_service.users().messages().list(userId=user_id, q='from:orders@instacart.com subject:"Your order with Instacart"', pageToken='').execute()
            for message in response['messages']:
            	message_id = response['messages'][0]['id']
            	response = gmail_service.users().messages().get(userId='me', id=message_id, format="full").execute()
            	email = RawEmailModel(response)
            	content = email.content()
            	# Parses the HTML
            	tree   = etree.HTML(content)
            	
            	# Converts the DOM into a string        
            	result = etree.tostring(tree, pretty_print=True, method="html")
            	#xpath_result = tree.xpath(u'.//th[div[text()="Items Delivered"]]/following-sibling::td/text()')
                els = tree.xpath("//*[contains(@class, 'msg-delivered')]")
                tree_string = els[0].xpath("string()").strip()
                m = re.match(r'Your order was delivered\r\non\r\n([0-9]+/[0-9]+)\r\n@\r\n([0-9]+:[0-9]+ [AP]M)', tree_string)
                if m:
                    date =  m.group(1)
                    day = date.strip('/')[0]
                    month = date.strip('/')[2]
                    time =  m.group(2)
                pdb.set_trace()
            	els = tree.xpath("//*[contains(@class, 'item-name')]")
            	for el in els:
            	    item_name = el.text.strip()
            	    for child in el.getchildren():
            	        if child.tag == 'br':
            	            continue
            	        if child.tag == 'small':
            	            if u'\xd7' in child.text:
            	                # This is a 2 x 2.50 kind of entry
            	                price_qty = child.text.strip()
            	                m = re.match(ur'([0-9]+) \xd7 (.[0-9]+\.[0-9]+)', price_qty, re.UNICODE)
            	                print m
            	                if m:
            	                    item_qty = m.group(1)
            	                    item_price = m.group(2)
            	                else:
            	                    print "Price: " + price_qty
            	            else:
            	                # This is each
            	                pass
                    item = ItemModel(user_id=user_id, item_name=item_name, item_qty=item_qty, item_price=item_price)
                    item.put()
            logging.debug("Fetching emails for: " + User.get_user_email_from_id(user_id))
            #deferred.defer(get_message_list_async,user_id, _queue="emailFetch")

class DishPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        json_data = open("sample.json").read()
        data = json.loads(json_data)
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.write(json.dumps(data))

routes = [ ('/', MainPage),
           (r'/api/login', LoginHandler),
           (r'/worker/fetchEmails', FetchEmailHandler),
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
