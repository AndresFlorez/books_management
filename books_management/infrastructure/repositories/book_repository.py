from logging import Logger

from bson import ObjectId
from books_management.entities.book import Book
from books_management.infrastructure.database.mongodb_client import MongoDBClient
from books_management.infrastructure.repositories.interfaces.book_repository_interface import BookRepositoryInterface


class BookRepository(BookRepositoryInterface):
    def __init__(self, db_client: MongoDBClient, logger: Logger):
        self.collection = db_client.get_database()["books"]
        self.logger = logger

    def find_all(self) -> list[Book]:
        return [Book.model_validate(book) for book in self.collection.find()]

    def get_by_id(self, book_id: ObjectId) -> Book:
        db_book = self.collection.find_one({"_id": book_id})
        if not db_book:
            self.logger.error(f"Book with id {book_id} not found")
            raise ValueError(f"Book with id {book_id} not found")
        return Book.model_validate(db_book)

    def create(self, book: Book) -> Book:
        book_id = self.collection.insert_one(book.model_dump(mode="json", exclude=["id"])).inserted_id
        return self.get_by_id(book_id)

    def update(self, book_id: ObjectId, book: Book) -> Book:
        self.collection.update_one({"_id": book_id}, {"$set": book.model_dump(mode="json", exclude=["id"])})
        return self.get_by_id(book_id)

    def delete(self, book_id: str):
        return self.collection.delete_one({"_id": book_id})
