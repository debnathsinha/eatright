import httplib2
import pprint
import sys

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

SERVICE_ACCOUNT_EMAIL=""

SERVICE_PRIVATE_KEY_FILE = "gmail-sessionid-privatekey.p12"

def createReportService():
    """Build the Admin SDK Reports service object
    
        To get all the users in the domain: https://www.googleapis.com/admin/directory/v1/users?domain=cosight.io
    """
    f = file(SERVICE_PRIVATE_KEY_FILE, 'rb')
    key = f.read()
    f.close()
    
    credentials = SignedJwtAssertionCredentials(SERVICE_ACCOUNT_EMAIL, key, 
                                                scope='https://www.googleapis.com/auth/admin.directory.user.readonly')
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    return build('admin', 'reports_v1', http = http)

def createDirectoryService():
    """Create a directory service
    """
    f = file(SERVICE_PRIVATE_KEY_FILE, 'rb')
    key = f.read()
    f.close()
    
    credentials = SignedJwtAssertionCredentials(SERVICE_ACCOUNT_EMAIL, key,
                                                scope='https://www.googleapis.com/auth/admin.directory.user.readonly')
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    return build('admin', 'directory_v1', http = http)

def list_all_users(domain="cosight.io"):
    """Lists all the users in a domain
    """
    