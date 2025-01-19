from abc import ABC, abstractmethod
from typing import Dict, List

from books_management.entities.book import Book


class BookRepositoryInterface(ABC):
    @abstractmethod
    def find_all(self, filters: Dict) -> List[Book]:
        """
        Get all books from the database.
        :return: List of books.
        """

    @abstractmethod
    def get_by_id(self, book_id: str) -> Book:
        """
        Get a book by id from the database.
        :param book_id: Id of the book to get.
        :return: Book.
        """

    @abstractmethod
    def create(self, book: Book) -> Book:
        """
        Create a book in the database.
        :param book: Book to create.
        :return: Created book.
        """

    @abstractmethod
    def update(self, book_id: str, book: Book) -> Book:
        """
        Update a book in the database.
        :param book: Book to update.
        :return: Updated book.
        """

    @abstractmethod
    def delete(self, book_id: str):
        """
        Delete a book from the database.
        :param book_id: Id of the book to delete.
        """

    @abstractmethod
    def average_price(self, year: int) -> float:
        """
        Get the average price of books published in a given year.
        :param year: Year to filter books.
        :return: Average price of books.
        """
