import sqlite3

DB_PATH = "warehouse.db"


def migrate(db_path=DB_PATH):
    book_columns = '(id integer, isbn text, authors text, year integer, title text, lang text, available boolean)'
    loan_columns = '(email text, book_id integer, status text, date text)'
    wishlist_columns = '(email text, book_id integer)'
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS books ' + book_columns)
        cursor.execute('CREATE TABLE IF NOT EXISTS loans ' + loan_columns)
        cursor.execute('CREATE TABLE IF NOT EXISTS wishlist ' + wishlist_columns)


class DB:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        migrate(db_path)

    def execute(self, sql):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.close()

    def insert_many(self, sql, rows):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany(sql, rows)
            cursor.close()

    def fetch(self, sql):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql)
            results = [dict(row) for row in cursor.fetchall()]
        return results
