import os

from auth0.v3.authentication import Users
from auth0.v3.exceptions import Auth0Error
from fastapi import HTTPException
import requests
import xml.etree.ElementTree as ET

import api.schemas.book as book_schema


DOMAIN = os.getenv("DOMAIN")
assert DOMAIN is not None, "Domain Not Found"

BOOK_ENDPOINT = 'https://iss.ndl.go.jp/api/sru'


def get_user_info(token: str):
    users = Users(DOMAIN)
    try:
        user = users.userinfo(token)
    except Auth0Error:
        raise HTTPException(status_code=401, detail='Invalid Token')
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

    response = requests.get(BOOK_ENDPOINT, params=params)
    
    root = ET.fromstring(response.text)
    ns = {
        "dc": "http://purl.org/dc/elements/1.1/"
    }
    author = validate_xml(root, "creator", ns)
    title = validate_xml(root, "title", ns)
    publisher = validate_xml(root, "publisher", ns)
    return book_schema.BookCreate(
        isbn=isbn,
        author=author,
        title=title,
        publisher=publisher
        )

def validate_xml(root: ET.Element, target: str, ns: dict):
    response = root.find(f".//dc:{target}", ns)
    if response is None:
        raise HTTPException(status_code=404, detail='Book Not Found From ISBN')
    return response.text