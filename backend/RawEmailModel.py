from email.utils import parsedate_tz, mktime_tz
from datetime import datetime
import logging
import base64
from utils.quotetail import quote
try:
    import json
except ImportError:
    import simplejson as json
from google.appengine.ext import ndb
import re
import pdb

class RawEmailModel:
    email = None
    threadId = None
    messageId = None
    fetched = None
    userId = None

    def __init__(self, email):
        self.email = json.dumps(email)

    def is_email(self):
        email = json.loads(self.email)
        if "payload" in email:
            try:
                date = [ header["value"] for header in email["payload"]["headers"] if header["name"] == "Date"]
                if len(date) > 0:
                    return True
            except Exception as e:
                logging.error("Could not parse whether it's an email: %s", date)
        return False
    
    def to_address(self):
        email = json.loads(self.email)
        try:
            if self.is_email():
                to_address = [ header["value"] for header in email["payload"]["headers"] if header["name"] == "To"]
                return to_address[0] if to_address else None
            else:
                return None
        except Exception as e:
            logging.debug("Could not parse to address: %s", e)
    
    def from_address(self):
        email = json.loads(self.email)
        try:
            if self.is_email():
                from_address = [ header["value"] for header in email["payload"]["headers"] if header["name"] == "From"]
                return from_address[0] if from_address else None
            else:
                return None
        except Exception as e:
            logging.debug("Could not parse from address: %s", e)
        
    def subject(self):
        email = json.loads(self.email)
        try:
            if self.is_email():
                subject = [ header["value"] for header in email["payload"]["headers"] if header["name"] == "Subject"]
                return subject[0] if subject else None
            else:
                return None
        except Exception as e:
            logging.debug("Could not parse subject: %s", e)
    
    def received(self):
        email = json.loads(self.email)
        try:
            if self.is_email():
                received = [ header["value"] for header in email["payload"]["headers"] if header["name"] == "Received" or header["name"] == "X-Received"]
                return received[0] if received else None
            else:
                return None
        except Exception as e:
            logging.debug("Could not parse received: %s", e)
            
    def cc_address(self):
        email = json.loads(self.email)
        try:
            if self.is_email():
                cc_address = [ header["value"] for header in email["payload"]["headers"] if header["name"] == "Cc"]
                return cc_address[0] if cc_address else None
            else:
                return None
        except Exception as e:
            logging.debug("Could not parse CC: %s", e)
            
    def bcc_address(self):
        email = json.loads(self.email)
        try:
            if self.is_email():
                cc_address = [ header["value"] for header in email["payload"]["headers"] if header["name"] == "Bcc"]
                return cc_address[0] if cc_address else None
            else:
                return None
        except Exception as e:
            logging.debug("Could not parse Bcc: %s", e)
        
    def date(self):
        email = json.loads(self.email)
        try:
            if self.is_email():
                date = [ header["value"] for header in email["payload"]["headers"] if header["name"] == "Date"]
                date = date[0]
                tt = parsedate_tz(date)
                timestamp = mktime_tz(tt)
                return datetime.fromtimestamp(timestamp)
            else:
                # This is a chat message
                return None
        except Exception as e:
            logging.debug("Could not parse date: %s", e)
    
    def arrival_time(self):
        email = json.loads(self.email)
        try:
            if self.is_email():
                date = [ header["value"] for header in email["payload"]["headers"] if header["name"] == "X-OriginalArrivalTime"]
                date = date[0]
                tt = parsedate_tz(date)
                timestamp = mktime_tz(tt)
                return datetime.fromtimestamp(timestamp)
            else:
                return None
        except Exception as e:
            logging.debug("Could not parse arrival time: %s", e)
            
    def _parse_parts(self, parts):
        text_content = []
        html_content = []
        for part in parts:
            if part["mimeType"]=='text/plain':
                if "data" in part["body"]:
                    text_content += [base64.urlsafe_b64decode(part["body"]["data"].encode('ASCII'))]
            elif part["mimeType"] == "text/html":
                if "data" in part["body"]:
                    html_content += [base64.urlsafe_b64decode(part["body"]["data"].encode('ASCII'))]
            elif part["mimeType"] == "multipart/alternative" or part["mimeType"] == "multipart/related":
                text_content_parts = []
                html_content_parts = []
                text_content_parts, html_content_parts = self._parse_parts(part["parts"])
                text_content += text_content_parts
                html_content += html_content_parts
        if len(text_content) == 0 and len(html_content) == 0:
            print "This is bad"
        return text_content, html_content
            
    def content(self):
        email = json.loads(self.email)
        try:
            if self.is_email():
                content = []
                if 'parts' in email["payload"]:
                    text_content, html_content = self._parse_parts(email["payload"]["parts"])
                    content = html_content
                elif 'body' in email["payload"] and email["payload"]["body"]["size"] > 0:
                    content = base64.urlsafe_b64decode(email["payload"]["body"]["data"].encode('ASCII'))
                if not content:
                    print "This is bad!"
                content = "".join(content)
                #originalEmailContent = quote(content)[0][1]
                return content
        except Exception as e:
            logging.error("Could not parse content: %s", e)
            
