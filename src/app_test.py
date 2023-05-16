import json
import os

import pytest

from app import application
from db import DB

TEST_DB_PATH = (
    os.path.dirname(os.path.abspath(__file__)) + "/test-resources/web_test_warehouse.db"
)


@pytest.fixture
def client():
    """A test client for the app."""
    db = DB(TEST_DB_PATH)

    db.insert_many('INSERT INTO books VALUES(:id, :isbn, :authors, :year, :title, :lang, :available)', [
        ["5", "043965548X", "J.K. Rowling, Mary GrandPré, Rufus Beck", "1999",
         "Harry Potter and the Prisoner of Azkaban", "eng", 1],
        ["18135", "743477111", "William Shakespeare, Robert Jackson", "1595",
         "An Excellent conceited Tragedie of Romeo and Juliet", "", 1]
    ])

    yield application.test_client()

    os.remove(TEST_DB_PATH)


def test_find_books_by_author(client):
    response = client.get(
        "api/books/find?author=Rowling",
        content_type='application/json'
    )
    books = response.json
    assert response.status_code == 200
    assert 1 == len(books)
    assert 'Harry Potter and the Prisoner of Azkaban' == books[0]['title']
    assert 'J.K. Rowling, Mary GrandPré, Rufus Beck' == books[0]['authors']


def test_find_books_by_title(client):
    response = client.get(
        "api/books/find?title=Harry",
        content_type='application/json'
    )
    books = response.json
    assert response.status_code == 200
    assert 1 == len(books)
    assert 'Harry Potter and the Prisoner of Azkaban' == books[0]['title']
    assert 'J.K. Rowling, Mary GrandPré, Rufus Beck' == books[0]['authors']


def test_find_books_by_title_and_authors(client):
    response = client.get(
        "api/books/find?title=Harry&author=Rowling",
        content_type='application/json'
    )
    books = response.json
    assert response.status_code == 200
    assert 1 == len(books)
    assert 'Harry Potter and the Prisoner of Azkaban' == books[0]['title']
    assert 'J.K. Rowling, Mary GrandPré, Rufus Beck' == books[0]['authors']


def test_wishlist_add(client):
    response = client.post(
        "api/wishlist/abhinay@gmail.com/5",
        content_type='application/json'
    )
    assert response.status_code == 201


def test_wishlist_remove(client):
    response = client.delete(
        "api/wishlist/abhinay@gmail.com/5",
        content_type='application/json'
    )
    assert response.status_code == 204


def test_wishlist_list(client):
    client.post(
        "api/wishlist/abhinay@gmail.com/5",
        content_type='application/json'
    )

    response = client.get(
        "api/wishlist/abhinay@gmail.com",
        content_type='application/json'
    )

    books = response.json
    assert response.status_code == 200
    assert 1 == len(books)
    assert 'Harry Potter and the Prisoner of Azkaban' == books[0]['title']
    assert 'J.K. Rowling, Mary GrandPré, Rufus Beck' == books[0]['authors']


def test_make_book_available(client):
    response = client.put(
        "api/books/5",
        data=json.dumps(dict(status=1)),
        content_type='application/json'
    )
    book = response.json
    assert response.status_code == 200
    assert 1 == book['available']


def test_make_book_unavailable(client):
    response = client.put(
        "api/books/5",
        data=json.dumps(dict(status=0)),
        content_type='application/json'
    )
    book = response.json
    assert response.status_code == 200
    assert 0 == book['available']
