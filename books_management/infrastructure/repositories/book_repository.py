from datetime import datetime
from logging import Logger
from typing import Dict

from books_management.commons.custom_exceptions import RecordNotFoundException
from books_management.commons.object_id import validate_object_id
from books_management.entities.book import Book
from books_management.infrastructure.database.mongodb_client import MongoDBClient
from books_management.infrastructure.repositories.interfaces.book_repository_interface import BookRepositoryInterface


class BookRepository(BookRepositoryInterface):
    def __init__(self, db_client: MongoDBClient, logger: Logger, collection_name: str = "books"):
        self.collection = db_client.database[collection_name]
        self.collection_name = collection_name
        self.logger = logger

    def find_all(self, filters: Dict) -> list[Book]:
        books = self.collection.find(filters)
        return [Book.model_validate(book) for book in books]

    def get_by_id(self, book_id: str) -> Book:
        book_id = validate_object_id(book_id)
        db_book = self.collection.find_one({"_id": book_id})
        if not db_book:
            self.logger.error(f"Book with id {book_id} not found")
            raise RecordNotFoundException(f"Book with id {book_id} not found")
        return Book.model_validate(db_book)

    def create(self, book: Book) -> Book:
        book_id = self.collection.insert_one(book.model_dump(mode="python", exclude=["id"])).inserted_id
        return self.get_by_id(book_id)

    def update(self, book_id: str, book: Book) -> Book:
        book_id = validate_object_id(book_id)
        self.collection.update_one({"_id": book_id}, {"$set": book.model_dump(mode="python", exclude=["id"])})
        return self.get_by_id(book_id)

    def delete(self, book_id: str):
        book_id = validate_object_id(book_id)
        delete_result = self.collection.delete_one({"_id": book_id})
        if delete_result.deleted_count == 0:
            self.logger.error(f"Book with id {book_id} not found")
            raise ValueError(f"Book with id {book_id} not found")
        return True

    def average_price(self, year: int) -> float:
        pipe_line = [
            {
                "$match": {
                    "published_date": {
                        "$gte": datetime(year, 1, 1),
                        "$lt": datetime(year + 1, 1, 1),
                    }
                },
            },
            {"$group": {"_id": None, "average_price": {"$avg": "$price"}}},
        ]
        result = list(self.collection.aggregate(pipe_line))
        if result:
            return result[0]["average_price"]
        return 0.0
