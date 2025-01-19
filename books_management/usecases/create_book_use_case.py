

from books_management.entities.book import Book
from books_management.infrastructure.repositories.interfaces.book_repository_interface import BookRepositoryInterface


class CreateBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, book: dict):
        book = Book.model_validate(book)
        created_book = self.book_repository.create(book)
        return created_book.model_dump(mode="json")