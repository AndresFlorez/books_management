from dependency_injector import containers, providers
from books_management.commons.logger import Logger

from books_management.usecases.get_books_use_case import GetBooksUseCase
from books_management.usecases.create_book_use_case import CreateBookUseCase
from books_management.usecases.get_book_use_case import GetBookUseCase
from books_management.usecases.update_book_use_case import UpdateBookUseCase
from books_management.usecases.delete_book_use_case import DeleteBookUseCase
from books_management.usecases.average_price_book_usecases import AveragePriceUseCase
from config.settings import mongo_settings
from books_management.infrastructure.database.mongodb_client import MongoDBClient
from books_management.infrastructure.repositories.book_repository import BookRepository
from books_management.infrastructure.database.mongodb_filters import proccess_filters


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logger = providers.Factory(Logger)

    db_client = providers.Singleton(
        MongoDBClient,
        host=mongo_settings.db_host,
        port=mongo_settings.db_port,
        user=mongo_settings.db_user,
        password=mongo_settings.db_password,
        database=mongo_settings.db_name,
    )

    book_repository = providers.Factory(
        BookRepository,
        db_client=db_client,
        logger=logger,
    )

    get_books_use_case = providers.Factory(
        GetBooksUseCase,
        book_repository=book_repository,
        proccess_filters=proccess_filters,
    )

    create_book_use_case = providers.Factory(
        CreateBookUseCase,
        book_repository=book_repository,
    )

    get_book_use_case = providers.Factory(
        GetBookUseCase,
        book_repository=book_repository,
    )

    update_book_use_case = providers.Factory(
        UpdateBookUseCase,
        book_repository=book_repository,
    )

    delete_book_use_case = providers.Factory(
        DeleteBookUseCase,
        book_repository=book_repository,
    )

    average_price_use_case = providers.Factory(
        AveragePriceUseCase,
        book_repository=book_repository,
    )


container = Container()
