import urllib2
try:
    import json
except ImportError:
    import simplejson as json
from apiclient.discovery import build

class SearchService():
    @staticmethod
    def custom_search(credential):
        # Build a service object for interacting with the API. Visit
        # the Google APIs Console <http://code.google.com/apis/console>
        # to get an API key for your own application.
        service = build("customsearch", "v1", developerKey='AIzaSyB1vXOme3730POiT9VfAQj-Iugn5o9MowY')

        res = service.cse().list(
                                 q='capillary',
                                 cx='004706753218302906364:hhwxuphtvf8',
                                 ).execute()
        print json.dumps(res)
        
    @staticmethod
    def bing_search(query, search_type):
        #search_type: Web, Image, News, Video
        key= 'YOUR_API_KEY'
        query = urllib2.quote(query)
        # create credential for authentication
        user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
        credentials = (':%s' % key).encode('base64')[:-1]
        auth = 'Basic %s' % credentials
        url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=5&$format=json'
        request = urllib2.Request(url)
        request.add_header('Authorization', auth)
        request.add_header('User-Agent', user_agent)
        request_opener = urllib2.build_opener()
        response = request_opener.open(request) 
        response_data = response.read()
        json_result = json.loads(response_data)
        result_list = json_result['d']['results']
        print result_list
        return result_list