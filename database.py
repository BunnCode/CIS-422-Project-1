import json
import datastructures as ds

from typing import List
from urllib.request import urlopen
from urllib import request, parse, response
import datastructures as ds

import asyncio
import time
#URL of the API
API_URL = "http://52.40.140.242:80"
ENCODING = "utf-8"
HEADERS = {
         "Content-Type" : "application/json"
    }
    
#Error class representing an error with the JSON request
class RequestError(Exception):
    pass

def decode_response(response_content, desired_data = ""):
    """Decode response from server, and raise exceptions if necessary

    Args:
        response_content (Any): Object representation of response
        desired_data (str): name of variable to pull from the request. Leave blank if none.

    Raises:
        RequestError: Raised if the success flag is set to false
        RequestError: Raised if the desired data cannot be found on the object

    Returns:
        (Any): the desired data from the object
    """
    response_text = response_content.decode(ENCODING)
    response = ds.Serializable.from_json(response_text)
    if(response.success != True):
        raise RequestError(response.message)
    try:
        if(len(desired_data) > 0):
            return getattr(response, desired_data)
        else:
            return response
    except:
        raise RequestError("Invalid data requested! Could not find {}".format(desired_data))

def get_articles() -> List:
    """Return a list of articles from the server

    Returns:
        List(Article): A list of all the articles currently on the server
    """
    
    with urlopen(API_URL + "/getArticles") as response:
        response_content = response.read()
        return decode_response(response_content, "articles")

def load_article(id : int) -> ds.Article:
    """Returns a specific article from the server

    Args:
        id (int): article ID

    Returns:
        ds.Article: Article returned from server
    """
    #Body is a dict converted to json and then encoded
    body = json.dumps({"article_id":id}).encode()
    #Don't forget to set headers to type JSON

    #Build out the request
    req = request.Request(API_URL + "/loadArticle", data = body, headers=HEADERS, method="GET")
    #Execute the request and get the result
    with urlopen(req) as response:
        response_content = response.read()
        return decode_response(response_content)

class ArticleValidator:
    _ArticlesToTrack = set() #Set of all tracked articles
    _KillUpdater = False #Internal flag used when closing out the updater to prevent collisions
    
    def __update_article(article : ds.Article):
        """Private method not to be called from outside the class. Updates an article 
        on the server from the local copy.

        Args:
            article (ds.Article): article to update
        """


    async def __update_articles_on_server(delay):
        """Private coroutine that keeps articles updated server-side.
        """
        while(not ArticleValidator._KillUpdater):
            await asyncio.sleep(delay)
            #ArticleValidator.__update_article()
            print("update called \n")

    def initialize_tracking(update_delay : int):
        """Call to initialize tracking of articles to the server

        Args:
            update_delay (int): Delay in seconds between tracking updates
        """
        #Initialize the coroutine
        asyncio.create_task(
            ArticleValidator.__update_articles_on_server(update_delay))

    def track_article_to_server(article : ds.Article):
        """Set an article to track with the server

        Args:
            article (ds.Article): Article to track
        """
        ArticleValidator._ArticlesToTrack.add(article)
    
    def untrack_article(article : ds.Article):
        """Stop tracking an article (always call this before destroying the article)

        Args:
            article (ds.Article): Article to stop tracking
        """
        ArticleValidator._ArticlesToTrack.remove(article)
        #await asyncio.sleep(delay)
        