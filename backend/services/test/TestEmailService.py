from oauth2client.client import OAuth2Credentials
from services.GmailService import GmailService
from gmailytics.RawEmailModel import RawEmailModel
from services.GmailServiceHelper import get_and_store_all_new_messages_async,\
    get_and_store_all_messages_async, get_message_list_async
import os
from admin.AdminStatsModel import IncrementalJob
from gmailytics.UserModel import User
from test.BaseCoSightTest import BaseCoSightTest
from services.EmailService import EmailService
try:
    import json
except ImportError:
    import simplejson as json
import unittest
from google.appengine.ext import testbed, deferred

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from nose.tools import nottest
from gmailytics import Constants

class GmailServiceTest(BaseCoSightTest):
    
    def setUp(self):
        BaseCoSightTest.setUp(self)
        self.testbed.init_mail_stub()
    
    @nottest
    def test_email_send(self):
        EmailService.send_email()
        
if __name__ == "__main__":
    unittest.main()