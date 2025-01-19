from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dependency_injector.wiring import Provide
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from books_management.container.container import Container
from books_management.usecases.book_usecases import (
    GetBookUseCase,
    GetBooksUseCase,
    CreateBookUseCase,
    UpdateBookUseCase,
)
from books_management.commons.swagger_schemas import book_schema

get_books_use_case: GetBooksUseCase = Provide[Container.get_books_use_case]
create_book_use_case: CreateBookUseCase = Provide[Container.create_book_use_case]
get_book_use_case: GetBookUseCase = Provide[Container.get_book_use_case]
update_book_use_case: UpdateBookUseCase = Provide[Container.update_book_use_case]
delete_book_use_case = Provide[Container.delete_book_use_case]


class BookListCreate(APIView):
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
        return Response(book, status=201)


class BookRetrieveUpdateDestroy(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a book",
        responses={
            200: openapi.Response(
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
            200: openapi.Response(
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
        responses={204: openapi.Response(description="No content")},
        parameters=[openapi.Parameter('book_id', openapi.IN_PATH, type=openapi.TYPE_STRING)],
    )
    def delete(self, request, book_id):
        delete_book_use_case.execute(book_id)
        return Response(status=204)
