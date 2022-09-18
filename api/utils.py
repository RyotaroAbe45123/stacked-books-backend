import os

from auth0.v3.authentication import Users
import requests
import xml.etree.ElementTree as ET

import api.schemas.book as book_schema


DOMAIN = os.getenv("DOMAIN")
assert DOMAIN is not None, "Domain Not Found"

BOOK_ENDPOINT = 'https://iss.ndl.go.jp/api/sru'


def get_user_info(token: str):
    users = Users(DOMAIN)
    user = users.userinfo(token)
    sub = user.get("sub")
    if sub is None:
        raise Exception("Not Found User Id")
    user_id = sub.split("|")[-1]
    return user_id


def search_book_info(isbn: int):
    params = {
        'operation': 'searchRetrieve',
        'query': f'isbn="{isbn}"',
        'recordPacking': 'xml'
    }

    response = requests.get(endpoint, params=params)
    
    root = ET.fromstring(response.text)
    ns = {
        "dc": "http://purl.org/dc/elements/1.1/"
    }
    author = root.find('.//dc:creator', ns).text
    title = root.find('.//dc:title', ns).text
    publisher = root.find('.//dc:publisher', ns).text
    # subject = root.find('.//dc:subject', ns).text
    return book_schema.BookCreate(
        isbn=isbn,
        author=author,
        title=title,
        publisher=publisher
        )
