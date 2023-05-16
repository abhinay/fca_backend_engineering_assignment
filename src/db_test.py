import os
import sqlite3
import unittest

from db import DB

TEST_DB_PATH = (
    os.path.dirname(os.path.abspath(__file__)) + "/test-resources/db_test_warehouse.db"
)


class DbTest(unittest.TestCase):

    def setUp(self):
        self.db = DB(TEST_DB_PATH)

    def tearDown(self):
        os.remove(TEST_DB_PATH)

    def test_migrate(self):
        self.assertEqual(self.db.fetch(
            'SELECT COUNT(*) count FROM books')[0]['count'], 0)
        self.assertEqual(self.db.fetch(
            'SELECT COUNT(*) count FROM loans')[0]['count'], 0)
        self.assertEqual(self.db.fetch(
            'SELECT COUNT(*) count FROM wishlist')[0]['count'], 0)

    def test_execute(self):
        self.db.execute(
            'INSERT INTO books VALUES(1, 2, "Kalidasa", 1999, "Shakuntala", "en", 1)')

        with sqlite3.connect(TEST_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM books')
            self.assertEqual(cursor.fetchone()[0], 1)

            rows = cursor.execute(
                "SELECT id, isbn, authors, year, title, lang FROM books")
            self.assertEqual(
                rows.fetchone(), (1, "2", "Kalidasa", 1999, "Shakuntala", "en"))

    def test_fetch(self):
        self.db.execute(
            'INSERT INTO books VALUES(1, 2, "Kalidasa", 1999, "Shakuntala", "en", 1)')

        actual = self.db.fetch('SELECT * FROM books')

        expected = [
            {"id": 1, "isbn": "2", "authors": "Kalidasa",
                "year": 1999, "title": "Shakuntala", "lang": "en", "available": 1},
        ]

        self.assertEqual(actual, expected)
