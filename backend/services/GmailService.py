""" Building out the different Google services
"""

from apiclient.discovery import build
from apiclient.errors import HttpError
import httplib2
import logging
import json
from oauth2client.appengine import StorageByKeyName, CredentialsModel
from apiclient import errors
from UserModel import User
import Constants
from oauth2client.client import OAuth2Credentials
from apiclient.http import BatchHttpRequest

def build_gmail_service_for_user(userId):
    if not Constants.TEST_CONTEXT:
        storage = StorageByKeyName(CredentialsModel, userId, "credentials")
        credentials = storage.get()
        return GmailService(credentials)
    else:
        with open("gmailytics/test/credentials.json") as f:
            data = f.read()
            credentials = OAuth2Credentials.from_json(data)
        return GmailService(credentials)

'''    
def process_message(request_id, response, exception):
    user_id = request_id.split(":")[0]
    logging.debug("Processing message for user: %s", user_id)
    raw_email_model = RawEmailModel.store_message(user_id, response["id"], response["threadId"], response)
    email_date = raw_email_model.date()
    if email_date:
        IndexManager.put_message_into_index(User.query(User.google_user_id==user_id).get(), raw_email_model)
        incremental_fetch_stats = IncrementalJob.query(IncrementalJob.user_id==user_id).get()
        if incremental_fetch_stats:
            if incremental_fetch_stats.oldest_email is None or email_date < incremental_fetch_stats.oldest_email:
                incremental_fetch_stats.oldest_email = email_date
            if incremental_fetch_stats.newest_email is None or email_date > incremental_fetch_stats.newest_email:
                incremental_fetch_stats.newest_email = email_date
            incremental_fetch_stats.email_fetches += 1
            incremental_fetch_stats.put()

class GmailService:
    def __init__(self, credential):
        # Build the service
        self.credential = credential
        self.service = build("gmail", "v1", http=credential.authorize(httplib2.Http()))
    
    def get_message(self, user_id, message_id):
        cached_email = RawEmailModel.get_message(user_id, message_id)
        if not cached_email or not cached_email.email:
            try:
                email_message = self.service.users().messages().get(userId='me', id=message_id, format="full").execute()
                incremental_job_stats = IncrementalJob.query(IncrementalJob.user_id==user_id).get()
                incremental_job_stats.email_fetches += 1
                incremental_job_stats.put()
                return email_message
            except HttpError as error:
                logging.error("%s::%s", self.__class__.__name__, error)
        else:
            return json.loads(cached_email.email)
    
    def get_page_of_messages(self, user_id, query='', page_token=None):
        try:
            response = self.service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            return response
        except HttpError as error:
            print 'An error occurred: %s' % error
            if error.resp.status == 401:
                # Credentials have been revoked.
                # TODO: Redirect the user to the authorization URL.
                raise NotImplementedError()
            
    def send_message(self, user_id, message):
        try:
            message = (self.service.users().messages().send(userId=user_id, body=message)
                       .execute())
            return message
        except errors.HttpError, error:
            print "An error occurred: %s", error
            
    def get_new_messages_from_messages(self, user_id, messages):
        new_messages = []
        for message in messages:
            cached_message = RawEmailModel.get_message(user_id, message["id"])
            if not cached_message:
                new_messages += [message]
        return new_messages
    
    def fetch_messages(self, user_id, messages):
        logging.debug("Fetching messages for: %s", User.get_user_email_from_id(user_id))
        batch = BatchHttpRequest()
        for message in messages:
            batch.add(self.service.users().messages().get(userId='me', id=message["id"], format="full"), callback=process_message, request_id=user_id+ ":" + message["id"])
        batch.execute()
        logging.debug("Enqueued fetched messages for execution for user %s", user_id)
        
    def get_messages_for_thread(self, user_id, thread_id):
        try:
            thread = self.service.users().threads().get(userId=user_id, id=thread_id).execute()
            messages = thread['messages']
            messages = [RawEmailModel(email=json.dumps(message), messageId=message["id"], threadId=message["threadId"], fetched=True, userId=user_id) for message in messages]
            print ('thread id: %s - number of messages '
                   'in this thread: %d') % (thread['id'], len(messages))
            return messages
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
        
    def list_new_messages(self, user_id='me', query=''):
        response = self.get_page_of_messages(user_id, query)
        all_messages_from_page = response['messages']
        next_page_token = response.get("nextPageToken")
        new_messages = self.get_new_messages_from_messages(user_id, all_messages_from_page)
        self.fetch_messages(user_id, new_messages)
        while next_page_token:
            self.get_page_of_messages(user_id, query, next_page_token)
            new_messages += self.get_new_messages_from_messages(user_id, all_messages_from_page)
        return new_messages
    
'''
