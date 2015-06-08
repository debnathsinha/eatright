from apiclient.discovery import build
from apiclient.errors import HttpError
import httplib2
import logging

class UserInfoService:
    def __init__(self, credential):
        self.service = build("oauth2", "v2", http=credential.authorize(httplib2.Http()))
    def get_user_info(self):
        """Get user info
    
        Args:
        Returns:
            User information as a dict
        """
        
        user_info = None
        try:
            user_info = self.service.userinfo().get().execute()
        except HttpError as e:
            logging.error('Error: %s', e)
        if user_info and user_info.get('id'):
            return user_info
        else:
            raise self.NoUserIdException()
        
    class NoUserIdException(Exception):
        """Error raised when no user id has been found"""