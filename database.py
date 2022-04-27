import json
import datastructures as ds

from typing import Any, List
from urllib.request import urlopen
from urllib import request, parse, response
import datastructures as ds

import asyncio
import time
#URL of the API
API_URL = "http://52.40.140.242:3000"
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
        article = decode_response(response_content)
        new_article = ds.Article(article.article_name, article.article_id)
        if(not hasattr(new_article, "chapters")):
            new_article.chapters = []
        #new_article.chapters = article.chapters
        return new_article


"""Article-related calls"""
def new_article(article_name : str) -> ds.Article:
    """Creates a new article and returns it

    Args:
        article_name (str): Name of the new article

    Returns:
        ds.Article: new article
    """
    body = json.dumps({"article_name" : article_name}).encode()
    req = request.Request(API_URL + "/newArticle", data = body, headers=HEADERS, method="POST")
    with urlopen(req) as response:
        response_content = response.read()
        return load_article(decode_response(response_content, "article_id"))

def delete_article(article : ds.Article) -> Any:
    """Delete an article from the server

    Args:
        article (ds.Article): article to delete

    Returns:
        Any: response from server
    """
    body = json.dumps({"article_id" : article.article_id}).encode()
    req = request.Request(API_URL + "/deleteArticle", data = body, headers=HEADERS, method="DELETE")
    with urlopen(req) as response:
        response_content = response.read()
        return decode_response(response_content)

def save_article(article : ds.Article) -> Any:
    """Save article on server. Recursively calls save on chapters as well.

    Args:
        article (ds.Article): Article to save

    Returns:
        Any: Response from server
    """
    body = json.dumps({
        "article_id" : article.article_id,
        "new_name" : article.article_name
        }).encode()
    req = request.Request(API_URL + "/editArticle", data = body, headers=HEADERS, method="PUT")
    
    #Recursively call on children
    for c in article.chapters:
        save_chapter(article, c)

    with urlopen(req) as response:
        response_content = response.read()
        return decode_response(response_content)

"""Chapter-related calls"""
def new_chapter(article : ds.Article, name : str, page : int) -> ds.Chapter:
    """Create a new chapter both locally and on the server

    Args:
        article (ds.Article): Article to associate with
        name (str): Name of chapter
        page (int): Page of chapter

    Returns:
        ds.Chapter: New chapter 
    """
    body = json.dumps({
        "article_id" : article.article_id,
        "chapter_name" : name,
        "chapter_order" : page
        }).encode()

    req = request.Request(API_URL + "/newChapter", data = body, headers=HEADERS, method="POST")

    with urlopen(req) as response:
        response_content = response.read()
        new_chap = ds.Chapter(page, name, decode_response(response_content, "chapter_id"))
        article.chapters.append(new_chap)
        return new_chap

def delete_chapter(article : ds.Article, chapter : ds.Chapter) -> Any:
    """Delete a chapter both locally and from the server

    Args:
        article (ds.Article): Article to delete chapter from
        chapter (ds.Chapter): Chapter to delete

    Returns:
        Any: Response from server
    """
    body = json.dumps({
        "article_id" : article.article_id,
        "chapter_id" : chapter.article_id
        }).encode()
    req = request.Request(API_URL + "/deleteChapter", data = body, headers=HEADERS, method="DELETE")
    with urlopen(req) as response:
        response_content = response.read()
        article.chapters.remove(chapter)
        return decode_response(response_content)


def save_chapter(article : ds.Article, chapter : ds.Chapter) -> Any:
    """Save chapter on server. Recursively calls on children.

    Args:
        article (ds.Article): Article the question is in
        chapter (ds.Chapter): Chapter to save

    Returns:
        Any: Response from server
    """
    print(chapter)
    body = json.dumps({
        "article_id" : article.article_id,
        "chapter_id" : chapter.get("chapter_id"),
        "new_name" : chapter.get("title")
        }).encode()
    req = request.Request(API_URL + "/editChapter", data = body, headers=HEADERS, method="PUT")
    
    #Recursively call on children
    for n in chapter.get("notes"):
        save_note(article, n)
    for q in chapter.get("questions"):
        save_question(article, q)

    with urlopen(req) as response:
        response_content = response.read()
        return decode_response(response_content)

"""Quiz-related calls"""
def new_question(article : ds.Article, chapter: ds.Chapter, question : str, answer : str) -> ds.Question:
    """Create new question both locally and on the server

    Args:
        article (ds.Article): Article to add the question to
        chapter (ds.Chapter): Chapter to add the question to
        question (str): Question text
        answer (str): Answer to the question

    Returns:
        ds.Question: The new question
    """
    body = json.dumps({
        "article_id" : article.article_id,
        "chapter_id" : chapter.chapter_id,
        "question" : question,
        "answer" : answer
        }).encode()

    req = request.Request(API_URL + "/newQuestion", data = body, headers=HEADERS, method="POST")

    with urlopen(req) as response:
        response_content = response.read()
        new_question = ds.Question(question, answer, decode_response(response_content, "question_id"))
        chapter.questions.append(new_question)
        return new_question

def delete_question(article : ds.Article, chapter:ds.Chapter, question : ds.Question) -> Any:
    """Delete a question both locally and from the server

    Args:
        article (ds.Article): Article to delete question from
        chapter (ds.Chapter): Chapter to delete question from
        question (ds.Question): Question to delete

    Returns:
        Any: Response from server
    """

    body = json.dumps({
        "article_id" : article.article_id,
        "question_id" : question.question_id
        }).encode()
    req = request.Request(API_URL + "/deleteQuestion", data = body, headers=HEADERS, method="DELETE")
    with urlopen(req) as response:
        response_content = response.read()
        chapter.questions.remove(question)
        return decode_response(response_content)

def save_question(article : ds.Article, question : ds.Question) -> Any:
    """Save question on server.

    Args:
        article (ds.Article): Article the question is in
        question (ds.Question): Question to save

    Returns:
        Any: Response from server
    """
    body = json.dumps({
        "article_id" : article.article_id,
        "question_id" : question.get("question_id"),
        "new_question" : question.get("question_text"),
        "new_answer" : question.get("answer_text")
        }).encode()
    req = request.Request(API_URL + "/editQuestion", data = body, headers=HEADERS, method="PUT")
    with urlopen(req) as response:
        response_content = response.read()
        return decode_response(response_content)

def record_quiz_attempt(article : ds.Article, score : int, max_score : int) -> ds.QuizAttempt:
    """Record new quiz attempt to server.

    Args:
        article (ds.Article): Article associated with attempt
        score (int): score for this attempt
        max_score (int): max possible score for this attempt
        
    Returns:
        Any: Response from server
    """
    score = min(max_score, (max(score, max_score))) #normalize score between bounds
    body = json.dumps({
        "article_id" : article.article_id,
        "score" : score,
        "max_score" :  max_score
        }).encode()

    req = request.Request(API_URL + "/recordQuizAttempt", data = body, headers=HEADERS, method="POST")

    with urlopen(req) as response:
        response_content = response.read()
        new_attempt = ds.QuizAttempt(score, max_score, decode_response(response_content, "attempt_id"))
        article.quiz_attempts.append(new_attempt)
        return new_attempt

"""Note-related calls"""
def new_note(article : ds.Article, chapter: ds.Chapter, page : int) -> ds.Note:
    """Create a new note, both locally and on the server

    Args:
        article (ds.Article): Article to associate the note with
        chapter (ds.Chapter): Chapter the note is on
        page (int): Page the note is on

    Returns:
        ds.Note: New note 
    """
    body = json.dumps({
        "article_id" : article.article_id,
        "chapter_id" : chapter.chapter_id,
        "note" : "", #empty by default
        "page_num" : page
        }).encode()

    req = request.Request(API_URL + "/newNote", data = body, headers=HEADERS, method="POST")

    with urlopen(req) as response:
        response_content = response.read()
        new_note = ds.Note(page, "", decode_response(response_content, "note_id"))
        chapter.notes.append(new_note)
        return new_note

def delete_note(article : ds.Article, chapter:ds.Chapter, note : ds.Note) -> Any:
    """Delete a note both locally and on the server

    Args:
        article (ds.Article): Article to delete note from
        chapter (ds.Chapter): Chapter to delete note from
        note (ds.Note): Note to delete

    Returns:
        Any: Response from server
    """
    body = json.dumps({
        "article_id" : article.article_id,
        "note_id" : note.note_id
        }).encode()
    req = request.Request(API_URL + "/deleteNote", data = body, headers=HEADERS, method="DELETE")
    with urlopen(req) as response:
        response_content = response.read()
        chapter.notes.remove(note)
        return decode_response(response_content)

def save_note(article : ds.Article, note : ds.Note) -> Any:
    """Save note to server

    Args:
        article (ds.Article): Article associated with note
        note (ds.Note): Note to save

    Returns:
        Any: Response from server
    """

    body = json.dumps({
        "article_id" : article.article_id,
        "note_id" : note.get("note_id"),
        "new_text" : note.get("note_text"),
        "new_page_num" : note.get("page_num")
        }).encode()
    req = request.Request(API_URL + "/deleteNote", data = body, headers=HEADERS, method="DELETE")
    with urlopen(req) as response:
        response_content = response.read()
        return decode_response(response_content)