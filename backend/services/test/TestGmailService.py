from oauth2client.client import OAuth2Credentials
from services.GmailService import GmailService, build_gmail_service_for_user
from gmailytics.RawEmailModel import RawEmailModel
from services.GmailServiceHelper import get_and_store_all_new_messages_async,\
    get_and_store_all_messages_async, get_message_list_async
import os
from admin.AdminStatsModel import IncrementalJob
from gmailytics.UserModel import User
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

class GmailServiceTest(unittest.TestCase):
    def setUp(self):
        Constants.TEST_CONTEXT = True
        #First create an instance of the Testbed class
        self.testbed = testbed.Testbed()
        #Then activate the testbed, which prepares the service stubs to use
        self.testbed.activate()
        #Next declare which service stubs you want to use
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_search_stub()
        self.testbed.init_taskqueue_stub(root_path=os.path.join(os.path.dirname(os.path.dirname( __file__ )),'..'))
        self.taskqueue_stub = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)
        with open("gmailytics/test/credentials.json") as f:
            data = f.read()
            credentials = OAuth2Credentials.from_json(data)
            self.credentials = credentials
        self.user = User(google_user_id=self.credentials.id_token["id"], 
                    google_display_email=self.credentials.id_token["email"])
        self.user.put()
        incremental_job_stats = IncrementalJob(user_id=self.user.google_user_id, started = False)
        incremental_job_stats.started = True
        incremental_job_stats.put()
        
         
    def tearDown(self):
        self.testbed.deactivate()
        
    def _more_tasks(self):
        # Get the task out of the queue
        return len(self.taskqueue_stub.get_filtered_tasks()) > 0
        
    def _execute_next_task(self):
        # Get the task out of the queue
        tasks = self.taskqueue_stub.get_filtered_tasks()
        # Run the task
        task = tasks[0]
        self.taskqueue_stub.FlushQueue('emailFetch')
        self.taskqueue_stub.FlushQueue('adminStats')
        deferred.run(task.payload)
        
    def _create_message(self, sender="test@cosight.io", to="test@cosight.io", 
                        subject="test email", message_text="test email text", num=0):
        message = MIMEText(message_text + str(num))
        message["to"] = to
        message["from"] = sender
        message["subject"] = subject + str(num)
        return { 'raw': base64.b64encode(message.as_string())}
    
    def _trash_message(self, gmail_service, user_id, message_id):
        """ Pass in the service because someone else should be calling the function,
            and they should have created the service as part of the test already.
        """
        gmail_service.service.users().messages().trash(userId=user_id, id=message_id).execute()
        
    def _message_page_invariants(self, result_size_estimate, messages, next_page_token=None):
        if result_size_estimate > 100:
            self.assertEqual(len(messages), 100)
            self.assertIsNotNone(next_page_token)
        else:
            self.assertIsNone(next_page_token)
            self.assertLessEqual(len(messages), 100)
         
    @nottest
    def test_fetch_message_list(self):
        gmail_service = GmailService(self.credentials)
        user_id = self.credentials.id_token["id"]
        response = gmail_service.get_page_of_messages(user_id, query='')
        self._message_page_invariants(response["resultSizeEstimate"], response["messages"],
                                      response.get("nextPageToken"))
        while "next_page_token" in response:
            response = gmail_service.get_page_of_messages(user_id)
            self._message_page_invariants(response["resultSizeEstimate"], response["messages"], 
                                          response.get("nextPageToken"))
    
    @nottest
    def test_fetch_message_page(self):
        gmail_service = GmailService(self.credentials)
        user_id = self.credentials.id_token["id"]
        response = gmail_service.get_page_of_messages(user_id, query='')
        self._message_page_invariants(response["resultSizeEstimate"], response["messages"], 
                                      response.get("nextPageToken"))
        
    def _send_n_messages(self, gmail_service, user_id,n):
        messages = []
        for i in range(1,n):
            created_message = self._create_message(num=i)
            message = gmail_service.send_message(user_id, created_message)
            messages += [message]
        return messages
    
    def _trash_messages(self, gmail_service, user_id, messages):
        for message in messages:
            self._trash_message(gmail_service, user_id, message["id"])
        
    @nottest
    def test_incremental_fetch(self):
        created_message = self._create_message()
        gmail_service = GmailService(self.credentials)
        user_id = self.credentials.id_token["id"]
        messages = gmail_service.list_new_messages(user_id)
        for message in messages:
            RawEmailModel.store_message(user_id, message["id"], message["threadId"])
        self.assertEqual(len(messages), 4)
        all_stored_messages = RawEmailModel.get_messages_for_user(user_id)
        self.assertEqual(len(all_stored_messages), 4)
        message = gmail_service.send_message(user_id, created_message)
        print "Message id: %s", message["id"]
        messages = gmail_service.list_new_messages(user_id)
        self.assertEqual(len(messages), 1)
        self._trash_message(gmail_service, user_id, message["id"])
        
    @nottest
    def test_fetch_previously_unfetched_messages(self):
        pass
    
    @nottest
    def test_get_message_content(self):
        gmail_service = GmailService(self.credentials)
        user_id = self.credentials.id_token["id"]
#         messages = gmail_service.list_new_messages(user_id)
#         message_contents = gmail_service.fetch_messages(user_id, messages)
#         for message_content in message_contents:
#             RawEmailModel.store_message(user_id, message_content["id"], message_content["threadId"], message_content)

#         messages = self._send_n_messages(gmail_service, user_id, 100)
        get_and_store_all_new_messages_async(user_id)
        # Get the task out of the queue
        tasks = self.taskqueue_stub.get_filtered_tasks()
        self.assertEqual(1, len(tasks))
        
        # Run the task
        task = tasks[0]
        deferred.run(task.payload)
        
#         self._trash_messages(gmail_service, user_id, messages)
        self.assertEqual(len(RawEmailModel.get_fetched_messages_for_user(user_id)), 103)
        
    @nottest
    def check_duplicates_in_multiple_test(self):
        get_and_store_all_messages_async(self.user.google_user_id)
        while self._more_tasks():
            self._execute_next_task()
        get_and_store_all_messages_async(self.user.google_user_id)
        while self._more_tasks():
            self._execute_next_task()
        self.assertEqual(len(RawEmailModel.query().fetch()), 1844)
        
    @nottest
    def test_no_duplicate_incremental_fetch_jobs(self):
        user_id = self.credentials.id_token["id"]
        get_message_list_async(user_id)
        get_message_list_async(user_id)
        
    @nottest
    def test_email_fetch_stats(self):
        user_id = self.credentials.id_token["id"]
        incremental_job_stats = IncrementalJob(user_id=user_id, started = False)
        incremental_job_stats.started = True
        incremental_job_stats.put()
        get_and_store_all_messages_async(user_id)
        self.assertEqual(IncrementalJob.query(IncrementalJob.user_id==user_id).get().email_fetches,100)
        if self._more_tasks():
            self._execute_next_task()
        self.assertEqual(len(RawEmailModel.query().fetch()), 200)
        
    @nottest
    def test_batch_get(self):
        user_id = self.credentials.id_token["id"]
        incremental_job_stats = IncrementalJob(user_id=user_id, started = False)
        incremental_job_stats.started = True
        incremental_job_stats.put()
        get_and_store_all_messages_async(user_id)
        
    @nottest
    def test_search_query(self):
        user_id = self.credentials.id_token["id"]
        gmail_service = build_gmail_service_for_user(user_id)
        search_query="srinath"
        response = gmail_service.service.users().messages().list(userId=user_id,q=search_query).execute()
        for message in response['messages']:
            response = gmail_service.get_message(user_id, message['id'])
        print response
        
if __name__ == "__main__":
    unittest.main()