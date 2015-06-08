from oauth2client.appengine import CredentialsModel,\
    StorageByKeyName
import logging
from google.appengine.ext import ndb
import re
from __builtin__ import classmethod

class User(ndb.Model):
    email = ndb.StringProperty()
    google_user_id = ndb.StringProperty()
    google_display_email = ndb.StringProperty()
    version = ndb.IntegerProperty(default=1)
    
    @classmethod
    def create_user(cls, user_id, user_email):
        cached_user = cls.get_user_from_id(user_id)
        if not cached_user:
            user = cls(google_user_id=user_id, google_display_email=user_email)
            user.put()

    @classmethod
    def get_all_users(cls):
        return cls.query().fetch()
    
    @classmethod
    def get_all_users_and_credentials(cls):
        users = cls.query().fetch()
        user_credentials_dict = {}
        for user in users:
            credentials = cls.get_credentials_from_user_id(user.google_user_id)
            user_credentials_dict[user] = credentials
        return user_credentials_dict
    
    @classmethod
    def get_user_from_id(cls, user_id):
        return cls.query(cls.google_user_id == user_id).get()
    
    @classmethod
    def get_user_email_from_id(cls, user_id):
        return cls.query(cls.google_user_id == user_id).get().google_display_email
    
    @classmethod
    def get_user_from_email(cls, email_address):
        return cls.query(cls.google_display_email == email_address).get()
    
    @classmethod
    def get_credentials_from_user_id(cls, user_id):
        storage = StorageByKeyName(CredentialsModel, user_id, "credentials")
        return storage.get()
    
    @classmethod
    def get_sfdc_credentials_from_user_id(cls, user_id):
        storage = StorageByKeyName(CredentialsModel, user_id+"sfdc", "credentials")
        return storage.get()
    
    @classmethod
    def store_credentials_for_user_id(cls, user_id, credentials):
        storage = StorageByKeyName(CredentialsModel, user_id, "credentials")
        cached_credentials = storage.get()
        if credentials.refresh_token or not cached_credentials or cached_credentials and not cached_credentials.refresh_token:
            storage.put(credentials)
            
    @classmethod
    def store_sfdc_credentials_for_user_id(cls, user_id, credentials):
        storage = StorageByKeyName(CredentialsModel, user_id+"sfdc", "credentials")
        cached_credentials = storage.get()
        if credentials.refresh_token or not cached_credentials or cached_credentials and not cached_credentials.refresh_token:
            storage.put(credentials)                

    @classmethod
    def delete_user(cls, user_id):
        storage = StorageByKeyName(CredentialsModel, user_id, "credentials")
        storage.delete()
        user = cls.get_user_from_id(user_id)
        logging.debug("Deleting user: %s", user.google_display_email)
        user.key.delete()
        
    @classmethod
    def get_domain_from_email(cls, email):
        return re.search("@[\w.]+", str(email)).group()[1:]
    
    @classmethod
    def get_all_users_in_domain(cls, user_id):
        email = cls.get_user_email_from_id(user_id)
        users = cls.get_all_users()
        all_users_in_domain = []
        for user in users:
            if cls.get_domain_from_email(user.google_display_email) == cls.get_domain_from_email(email):
                all_users_in_domain += [user]
        return all_users_in_domain