from typing import Dict, List
from books_management.entities.book import Book

from books_management.infrastructure.repositories.interfaces.book_repository_interface import BookRepositoryInterface


class GetBooksUseCase:
    def __init__(self, book_repository: BookRepositoryInterface, proccess_filters: callable):
        self.book_repository = book_repository
        self.proccess_filters = proccess_filters

    def execute(self, filters: Dict) -> List[Dict]:
        proccessed_filters = self.proccess_filters(filters)
        books: List[Book] = self.book_repository.find_all(proccessed_filters)
        return [book.model_dump(mode="json") for book in books]
