from books_management.commons.object_id import validate_object_id
from books_management.infrastructure.repositories.interfaces.book_repository_interface import BookRepositoryInterface


class GetBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, book_id: str):
        book_id = validate_object_id(book_id)
        book = self.book_repository.get_by_id(book_id)
        return book.model_dump(mode="json")