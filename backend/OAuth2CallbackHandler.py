from google.appengine.api import taskqueue
from apiclient.discovery import build
from oauth2client.client import FlowExchangeError
from SessionBasedHandler import SessionBasedHandler
from Constants import SIGNIN_FLOW, MobileJWTSecret
from UserModel import User
try:
    import json
except ImportError:
    import simplejson as json
import re
import logging
import httplib2
import jwt
import pdb
from services.GmailService import build_gmail_service_for_user
from RawEmailModel import RawEmailModel
import lxml.html as lh
from lxml import etree

class OAuth2CallbackHandler(SessionBasedHandler):
    def get(self):
        if self.request.get("error"):
            self.redirect("/")
            return
        auth_code = self.request.params["code"]
        try:
            credentials = SIGNIN_FLOW.step2_exchange(auth_code)
            user_id = credentials.id_token["sub"]
            user_email = credentials.id_token["email"]
            logging.debug("Got credentials %s for user %s", credentials.to_json(), user_email)
            if user_id:
                user = User.get_user_from_id(user_id)
                if not user:
                    User.create_user(user_id, user_email)
                    logging.debug("Adding to task queue for user email %s", user_email)
                    #taskqueue.add(url="/worker/fetchEmails", params={ 'user_id': user_id, 'user_email': user_email})
                self.session["user_id"] = user_id
                self.session["user_email"] = user_email
                User.store_credentials_for_user_id(user_id, credentials)
                gmail_service = build("gmail", "v1", http=credentials.authorize(httplib2.Http()))
                #gmail_service = build_gmail_service_for_user(user_id)
                response = gmail_service.users().messages().list(userId=user_id, q='from:orders@instacart.com subject:"Your order with Instacart"', pageToken='').execute()
                message_id = response['messages'][0]['id']
                response = gmail_service.users().messages().get(userId='me', id=message_id, format="full").execute()
                email = RawEmailModel(response)
                content = email.content()
                pdb.set_trace()
                # Parses the HTML
                tree   = etree.HTML(content)
                
                # Converts the DOM into a string        
                result = etree.tostring(tree, pretty_print=True, method="html")
                #xpath_result = tree.xpath(u'.//th[div[text()="Items Delivered"]]/following-sibling::td/text()')
                els = tree.xpath("//*[contains(@class, 'item-name')]")
                items = []
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
                                item_qty = m.group(1)
                                item_price = m.group(2)
                            else:
                                # This is each
                                pass
                    item = { 
                        'name': item_name,
                        'qty': item_qty,
                        'price': item_price
                    }
                    items += [item]
                            
                    
                #hparser = etree.HTMLParser(encoding='utf-8')
                #htree   = etree.parse(content, hparser)
                #html_content = lh.parse(content.encode('utf-8'))
                #response = gmail_service.get_page_of_messages(user_id)
                #self.response.headers['Content-Type'] = 'application/json'
                self.response.out.write(result)

                #token = jwt.encode({'user_id': user_id}, MobileJWTSecret)
                #self.redirect("/settings?token="+token)
                return
        except FlowExchangeError:
            self.send_error(401, 'Failed to exchange authorization code')
            return
        self.redirect("/settings")
