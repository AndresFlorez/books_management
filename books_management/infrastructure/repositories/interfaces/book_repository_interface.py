from abc import ABC, abstractmethod
from typing import List

from bson import ObjectId

from books_management.entities.book import Book


class BookRepositoryInterface(ABC):
    @abstractmethod
    def find_all(self) -> List[Book]:
        """
        Get all books from the database.
        :return: List of books.
        """

    @abstractmethod
    def get_by_id(self, book_id: ObjectId) -> Book:
        pass

    @abstractmethod
    def create(self, book: Book) -> Book:
        pass

    @abstractmethod
    def update(self, book: Book) -> Book:
        pass

    @abstractmethod
    def delete(self, book_id: int):
        pass
