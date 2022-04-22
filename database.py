from typing import List
from urllib.request import urlopen
from urllib import request, parse
import datastructures as ds

#URL of the API
API_URL = "http://52.40.140.242:80"
ENCODING = "utf-8"
class RequestError(Exception):
    pass

def decode_response(response_content, desired_data : str):
    """Decode response from server, and raise exceptions if necessary

    Args:
        response_content (Any): Object representation of response
        desired_data (str): name of variable to pull from the request

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
        return getattr(response, desired_data)
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
    body = parse.urlencode({"article_id":id}).encode()
    req = request.Request(API_URL + "/loadArticle", data=body)
    with urlopen(req) as response:
        response_content = response.read()
        return decode_response(response_content, "articles")
        