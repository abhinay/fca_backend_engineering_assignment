import os

from flask import Flask, request
from flask_restx import Api, Resource, fields

import config
from db import DB
from service import BookService, WishlistService

application = Flask(__name__)

if os.environ.get('FLASK_ENV', 'development') != 'development':
    app_config = config.TestConfig
else:
    app_config = config.DevConfig

db = DB(app_config.DB_PATH)

book_service = BookService(db)
wishlist_service = WishlistService(db)

application.config.from_object(app_config)

api = Api(
    application,
    version='Beta',
    title='Book Loans',
    description='Book Loan API for Local Library',
    prefix='/api',
    doc='/docs'
)

book = api.model('Book', {
    'isbn': fields.String(
        required=True,
        description='Book ISBN'
    ),
    'title': fields.String(
        required=True,
        description='Book Title'
    ),
    'authors': fields.String(
        required=True,
        description='Book Author(s)'
    ),
    'year': fields.String(
        required=True,
        description='Publication Year'
    ),
    'lang': fields.String(
        required=True,
        description='Language'
    ),
    'available': fields.Boolean(
        required=True,
        description='Book Availability'
    )
})

status = api.model('BookStatus', {
    'status': fields.Integer(
        required=True,
        description='Availability status for book'
    )
})


#################################################
#                NER API                        #
#################################################
book_ns = api.namespace('books', description='Operations for Books')
wishlist_ns = api.namespace('wishlist', description='Operations for Wishlists')


@book_ns.route('/find')
class Books(Resource):
    @book_ns.param('title', 'Book Title')
    @book_ns.param('author', 'Book Author')
    @book_ns.doc('find_books')
    @book_ns.marshal_list_with(book, code=200)
    def get(self):
        return book_service.find(
            request.args.get('author'),
            request.args.get('title')
        ), 200


@book_ns.route('/<int:book_id>')
class Book(Resource):
    @book_ns.param('book_id', 'Book ID')
    @book_ns.doc('update_book_status')
    @book_ns.expect(status, validate=True)
    @wishlist_ns.marshal_with(book, code=200)
    def put(self, book_id):
        return book_service.update(book_id, api.payload['status']), 200


@wishlist_ns.route('/<string:email>/<int:book_id>')
class WishlistItem(Resource):
    @wishlist_ns.param('email', 'User Email')
    @wishlist_ns.param('book_id', 'Book ID')
    @wishlist_ns.doc('add_to_wishlist')
    @wishlist_ns.marshal_with(book, code=201)
    def post(self, email, book_id):
        return wishlist_service.add(email, book_id), 201

    @wishlist_ns.param('email', 'User Email')
    @wishlist_ns.param('book_id', 'Book ID')
    @wishlist_ns.doc('remove_from_wishlist')
    @wishlist_ns.response(204, 'Removed from wishlist')
    def delete(self, email, book_id):
        wishlist_service.remove(email, book_id)
        return '', 204


@wishlist_ns.route('/<string:email>')
class Wishlist(Resource):
    @wishlist_ns.param('email', 'User Email')
    @wishlist_ns.doc('list_wishlist')
    @wishlist_ns.marshal_list_with(book, code=200)
    def get(self, email):
        return wishlist_service.find(email), 200
