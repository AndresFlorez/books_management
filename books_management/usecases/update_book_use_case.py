from books_management.entities.book import Book
from books_management.infrastructure.repositories.interfaces.book_repository_interface import BookRepositoryInterface


class UpdateBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, book_id: str, book_data: dict):
        book = Book.model_validate(book_data)
        updated_book: Book = self.book_repository.update(book_id, book)
        return updated_book.model_dump(mode="json")
