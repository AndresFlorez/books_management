from books_management.commons.object_id import validate_object_id
from books_management.entities.book import Book
from books_management.infrastructure.repositories.interfaces.book_repository_interface import BookRepositoryInterface


class GetBooksUseCase:
    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self):
        books = self.book_repository.find_all()
        return [book.model_dump(mode="json") for book in books]


class CreateBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, book: dict):
        book = Book.model_validate(book)
        created_book = self.book_repository.create(book)
        return created_book.model_dump(mode="json")


class GetBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, book_id: str):
        book_id = validate_object_id(book_id)
        book = self.book_repository.get_by_id(book_id)
        return book.model_dump(mode="json")


class UpdateBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, book_id: str, book_data: dict):
        book_id = validate_object_id(book_id)
        book = Book.model_validate(book_data)
        updated_book = self.book_repository.update(book_id, book)
        return updated_book.model_dump(mode="json")


class DeleteBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, book_id: str):
        book_id = validate_object_id(book_id)
        return self.book_repository.delete(book_id)
