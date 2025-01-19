from typing import List
from books_management.entities.book import Book
from books_management.infrastructure.repositories.interfaces.book_repository_interface import BookRepositoryInterface


class GetBooksUseCase:
    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self):
        books: List[Book] = self.book_repository.find_all()
        return [book.model_dump(mode="json") for book in books]
