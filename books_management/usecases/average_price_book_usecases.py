from books_management.infrastructure.repositories.interfaces.book_repository_interface import BookRepositoryInterface


class AveragePriceUseCase:
    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def execute(self, year: int):
        return self.book_repository.average_price(year)
