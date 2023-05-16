class BookService(object):
    def __init__(self, db):
        self.db = db

    def update(self, book_id, status):
        query = "UPDATE books SET available = " + \
            str(status) + " WHERE id = " + str(book_id)

        self.db.execute(query)

        return self.db.fetch("SELECT isbn, authors, year, title, lang, available FROM books WHERE id = " + str(book_id))[0]

    def find(self, author, title):
        query = """
            SELECT isbn, authors, year, title, lang, available
            FROM books
            WHERE true
            """

        if author and len(author) > 0:
            query += " AND authors LIKE '%" + author + "%'"

        if title and len(title) > 0:
            query += " AND title LIKE '%" + title + "%'"

        return self.db.fetch(query)


class WishlistService(object):
    def __init__(self, db):
        self.db = db

    def find(self, email):
        query = """
            SELECT isbn, authors, year, title, lang, available
            FROM books
            JOIN wishlist ON wishlist.book_id = books.id
            """

        query += " WHERE email = '" + email + "'"

        return self.db.fetch(query)

    def add(self, email, book_id):
        self.db.execute(
            'INSERT INTO wishlist VALUES("' + email + '",' + str(book_id) + ')')

        return self.db.fetch("SELECT * FROM books WHERE id = " + str(book_id))[0]

    def remove(self, email, book_id):
        self.db.execute(
            'DELETE FROM wishlist WHERE email = "' + email + '" AND book_id = ' + str(book_id))
