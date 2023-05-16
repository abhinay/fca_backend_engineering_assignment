import os
import unittest

import ingest
from db import DB
from ingest import IngestPipeline

TEST_DATA_PATH = (
    os.path.dirname(os.path.abspath(__file__)) + "/test-resources/"
)


class IngestTest(unittest.TestCase):

    def setUp(self):
        self.db = DB(TEST_DATA_PATH + "ingest_test_warehouse.db")

    def tearDown(self):
        os.remove(TEST_DATA_PATH + "ingest_test_warehouse.db")

    def test_extract(self):
        expected_rows = [
            ["6148028", "439023491", "Suzanne Collins", "2009", "Catching Fire", "eng"],
            ["5", "043965548X", "J.K. Rowling, Mary GrandPré, Rufus Beck",
                "1999", "Harry Potter and the Prisoner of Azkaban", "eng"],
            ["18135", "743477111", "William Shakespeare, Robert           Jackson",
                "1595", "An Excellent conceited Tragedie of Romeo and Juliet", ""]
        ]

        rows = ingest.extract(TEST_DATA_PATH + 'sample-data.csv')

        self.assertEqual(rows, expected_rows)

    def test_transform(self):
        rows = [
            ["5", "043965548X", "J.K. Rowling, Mary GrandPré, Rufus Beck",
                "1999", "Harry Potter and the Prisoner of Azkaban", "eng"],
            ["18135", "743477111", "William Shakespeare, Robert           Jackson",
                "1595", "An Excellent conceited Tragedie of Romeo and Juliet", ""]
        ]

        actual_rows = ingest.transform(rows)

        expected_rows = [
            ["5", "043965548X", "J.K. Rowling, Mary GrandPré, Rufus Beck", "1999",
             "Harry Potter and the Prisoner of Azkaban", "eng", 1],
            ["18135", "743477111", "William Shakespeare, Robert Jackson", "1595",
             "An Excellent conceited Tragedie of Romeo and Juliet", "", 1]
        ]

        self.assertEqual(actual_rows, expected_rows)

    def test_load(self):
        rows = [
            ["5", "043965548X", "J.K. Rowling, Mary GrandPré, Rufus Beck", "1999",
             "Harry Potter and the Prisoner of Azkaban", "eng", 1],
            ["18135", "743477111", "William Shakespeare, Robert Jackson", "1595",
             "An Excellent conceited Tragedie of Romeo and Juliet", "", 1]
        ]

        ingest.load(self.db, rows)

        expected_rows = [
            {"id": 5, "isbn": "043965548X", "authors": "J.K. Rowling, Mary GrandPré, Rufus Beck",
                "year": 1999, "title": "Harry Potter and the Prisoner of Azkaban", "lang": "eng", "available": 1},
            {"id": 18135, "isbn": "743477111", "authors": "William Shakespeare, Robert Jackson",
                "year": 1595, "title": "An Excellent conceited Tragedie of Romeo and Juliet", "lang": "", "available": 1}
        ]

        self.assertEqual(self.db.fetch("SELECT * FROM books"), expected_rows)

    def test_pipeline_end_to_end(self):
        pipeline = IngestPipeline(TEST_DATA_PATH + 'sample-data.csv', self.db)
        pipeline.execute()

        self.assertEqual(self.db.fetch(
            "SELECT COUNT(*) AS count FROM books")[0]['count'], 3)
