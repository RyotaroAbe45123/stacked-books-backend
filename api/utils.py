import os
from typing import Union

from auth0.v3.authentication import Users
from auth0.v3.exceptions import Auth0Error
from fastapi import HTTPException
import requests
import xml.etree.ElementTree as ET

import api.schemas.book as book_schema


DOMAIN = os.getenv("DOMAIN")
assert DOMAIN is not None, "Domain Not Found"

BOOK_ENDPOINT = 'https://iss.ndl.go.jp/api/sru'
BOOK_ENDPOINT = "https://iss.ndl.go.jp/api/opensearch"


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


def _search_book_info(isbn: int):
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

def search_book_info(isbn: int):
    params = {
        "isbn": isbn
    }
    response = requests.get(BOOK_ENDPOINT, params=params)

    root = ET.fromstring(response.text)

    ns = {
        "dcndl": "http://ndl.go.jp/dcndl/terms/"
    }
    price = None
    for i in root.findall(".//dcndl:price", ns):
        price = search_price(i.text)
        if price is not None:
            break
    assert price is not None, "price is not found."
    print(price)

    ns = {
        "dc": "http://purl.org/dc/elements/1.1/"
    }
    pages = None
    for i in root.findall(".//dc:extent", ns):
        pages = search_pages(i.text)
        if pages is not None:
            break
    assert pages is not None, "pages is not found."

    author = None
    for i in root.iter("author"):
        author = i.text
        if author is not None:
            break
    assert author is not None, "author is not found."

    title = root.find(".//dc:title", ns)
    assert title is not None, "title is not found."
    title = title.text
    publisher = root.find(".//dc:publisher", ns)
    assert publisher is not None, "publisher is not found."
    publisher = publisher.text

    return book_schema.BookCreate(
        isbn=isbn,
        price=price,
        pages=pages,
        author=author,
        title=title,
        publisher=publisher
        )

def search_pages(text: str) -> Union[str, None]:
    if not "p" in text: return None
    if " " not in text.split("p")[0]: return text.split("p")[0]
    else: return text.split("p")[0].split(" ")[-1]


def search_price(text: str) -> Union[str, None]:
    print(text)
    # textは、数字のみ or 数字+円
    try:
        price = int(text)
        return price
    except ValueError:
        if not "円" in text: return None
        else: return text.replace("円", "").replace("+税", "")

