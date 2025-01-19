from books_management.infrastructure.repositories.interfaces.book_repository_interface import BookRepositoryInterface


class DeleteBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, book_id: str):
        return self.book_repository.delete(book_id)
