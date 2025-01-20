from django.test import TestCase
from datetime import datetime
import mongomock
from books_management.usecases.books_price_average_usecases import AveragePriceUseCase
from books_management.infrastructure.repositories.book_repository import BookRepository
from books_management.infrastructure.database.mongodb_client import MongoDBClient


class BookManagementPriceAverageTestCase(TestCase):

    def setUp(self):
        self.mock_db = mongomock.MongoClient()
        self.mock_db.database = self.mock_db["books_management_test"]
        self.book_repository = BookRepository(self.mock_db, None, "books_test")

        collection = self.mock_db.database["books_test"]
        collection.insert_many(
            [
                {
                    'title': 'Test title',
                    'author': 'Test author',
                    'published_date': datetime(2025, 1, 1, 0, 0),
                    'genre': 'Test genre',
                    'description': 'Test description',
                    'price': 10.0,
                },
                {
                    'title': 'Test title',
                    'author': 'Test author',
                    'published_date': datetime(2025, 1, 1, 0, 0),
                    'genre': 'Test genre',
                    'description': 'Test description',
                    'price': 15.0,
                },
            ]
        )
        self.use_case = AveragePriceUseCase(self.book_repository)

    def test_average_price(self):
        """
        Test average price use case, should return average price
        """
        result = self.use_case.execute(2025)
        self.assertEqual(result, 12.5)

    def tearDown(self):
        self.mock_db.drop_database("books_management_test")