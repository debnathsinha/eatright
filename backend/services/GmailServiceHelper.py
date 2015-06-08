import logging
from google.appengine.api.taskqueue.taskqueue import DuplicateTaskNameError
from admin.AdminStatsModel import IncrementalJob
from services.GmailService import process_message
from gmailytics.UserModel import User
try:
    import json
except ImportError:
    import simplejson as json
from google.appengine.ext import deferred, ndb
from GmailService import build_gmail_service_for_user

def get_and_store_all_new_messages_async(user_id='me', query='', page_token=None):
    ndb.get_context().clear_cache()
    gmail_service = build_gmail_service_for_user(user_id)
    response = gmail_service.get_page_of_messages(user_id, query, page_token)
    all_messages_from_page = response['messages']
    next_page_token = response.get("nextPageToken")
    new_messages = gmail_service.get_new_messages_from_messages(user_id, all_messages_from_page)
    if not page_token and new_messages and len(new_messages)>0:
        #This is the start of the job, start the stats counter and log
        logging.debug("Starting incremental fetch job for user %s", User.get_user_email_from_id(user_id))
    if not new_messages or len(new_messages)==0:
        logging.debug("Did not see any more new messages for user: %s", User.get_user_email_from_id(user_id))
        cached_stats = IncrementalJob.query(IncrementalJob.user_id==user_id).get()
        if cached_stats:
            cached_stats.started = False
            cached_stats.put()
        return 
    gmail_service.fetch_messages(user_id, new_messages)
#     store_messages(user_id, new_message_contents)
    if next_page_token:
        try:
            logging.debug("Enqueuing next page for %s with new page token: %s", user_id, next_page_token)
            deferred.defer(get_and_store_all_new_messages_async, user_id, query, next_page_token, _queue="emailFetch")
        except DuplicateTaskNameError:
            logging.error("Duplicate task name exception")
    else:
        #This is the end of the job, end the stats counter
        cached_stats = IncrementalJob.query(IncrementalJob.user_id==user_id).get()
        cached_stats.started = False
        cached_stats.put()
        logging.debug("Ending incremental fetch job for user %s", User.get_user_email_from_id(user_id))
        
def get_and_store_all_messages_async(user_id='me', query='', page_token=None):
    ndb.get_context().clear_cache()
    gmail_service = build_gmail_service_for_user(user_id)
    response = gmail_service.get_page_of_messages(user_id, query, page_token)
    all_messages_from_page = response['messages']
    next_page_token = response.get("nextPageToken")
    gmail_service.fetch_messages(user_id, all_messages_from_page)
#     store_messages(user_id, message_contents)
    if next_page_token:
        try:
            deferred.defer(get_and_store_all_messages_async, user_id, query, next_page_token, _queue="emailFetch")
        except DuplicateTaskNameError:
            logging.error("Duplicate task name exception")

def store_messages(user_id, message_contents):
    for message_content in message_contents:
        process_message(user_id, message_content)

def get_message_list_async(user_id, new_messages_only=True):
    try:
        if new_messages_only:
            get_and_store_all_new_messages_async(user_id)
#             cached_stats = IncrementalJob.query(IncrementalJob.user_id==user_id).get()
#             if not cached_stats:
#                 cached_stats = IncrementalJob(user_id = user_id, started = False)
#                 cached_stats.put()
#             if not cached_stats.started:
#                 cached_stats.started = True
#                 cached_stats.put()
#                 
#                 logging.debug("Starting off a new incremental fetch task %s", cached_stats.started)
#             else:
#                 logging.debug("Not starting off another incremental fetch since one is already in progress")
        else:
            get_and_store_all_messages_async(user_id)
    except Exception as e:
        logging.error(e)