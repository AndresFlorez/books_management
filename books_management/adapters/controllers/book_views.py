from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dependency_injector.wiring import Provide
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from books_management.container.container import Container
from books_management.commons.swagger_schemas import book_schema
from books_management.usecases.get_books_use_case import GetBooksUseCase
from books_management.usecases.create_book_use_case import CreateBookUseCase
from books_management.usecases.get_book_use_case import GetBookUseCase
from books_management.usecases.update_book_use_case import UpdateBookUseCase
from books_management.usecases.delete_book_use_case import DeleteBookUseCase
from books_management.usecases.average_price_book_usecases import AveragePriceUseCase

get_books_use_case: GetBooksUseCase = Provide[Container.get_books_use_case]
create_book_use_case: CreateBookUseCase = Provide[Container.create_book_use_case]
get_book_use_case: GetBookUseCase = Provide[Container.get_book_use_case]
update_book_use_case: UpdateBookUseCase = Provide[Container.update_book_use_case]
delete_book_use_case: DeleteBookUseCase = Provide[Container.delete_book_use_case]
average_price_use_case: AveragePriceUseCase = Provide[Container.average_price_use_case]


class BookListCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of books",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="A list of books",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties=book_schema,
                    ),
                ),
            )
        },
    )
    def get(self, request):
        books = get_books_use_case.execute()
        return Response(books, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new book",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=book_schema,
        ),
        responses={
            201: openapi.Response(
                description="The created book",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=book_schema,
                ),
            )
        },
    )
    def post(self, request):
        book = create_book_use_case.execute(request.data)
        return Response(book, status=status.HTTP_201_CREATED)


class BookRetrieveUpdateDestroyView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a book",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="The book",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=book_schema,
                ),
            )
        },
        parameters=[openapi.Parameter('book_id', openapi.IN_PATH, type=openapi.TYPE_STRING)],
    )
    def get(self, request, book_id):
        book = get_book_use_case.execute(book_id)
        return Response(book, status=200)

    @swagger_auto_schema(
        operation_description="Update a book",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=book_schema,
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="The updated book",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=book_schema,
                ),
            )
        },
        parameters=[openapi.Parameter('book_id', openapi.IN_PATH, type=openapi.TYPE_STRING)],
    )
    def put(self, request, book_id):
        book = update_book_use_case.execute(book_id, request.data)
        return Response(book, status=200)

    @swagger_auto_schema(
        operation_description="Delete a book",
        responses={status.HTTP_200_OK: openapi.Response(description="No content")},
        parameters=[openapi.Parameter('book_id', openapi.IN_PATH, type=openapi.TYPE_STRING)],
    )
    def delete(self, request, book_id):
        delete_book_use_case.execute(book_id)
        return Response(status=204)


class AveragePriceView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve the average price of books published in a given year",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="The average price",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"average_price": openapi.Schema(type=openapi.TYPE_NUMBER)},
                ),
            )
        },
        parameters=[openapi.Parameter('year', openapi.IN_PATH, type=openapi.TYPE_INTEGER)],
    )
    def get(self, request, year):
        try:
            average_price = average_price_use_case.execute(year)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"average_price": average_price}, status=status.HTTP_200_OK)
