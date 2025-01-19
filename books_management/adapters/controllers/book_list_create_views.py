import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from dependency_injector.wiring import Provide
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from books_management.commons.logger import Logger
from books_management.container.container import Container
from books_management.commons.swagger_schemas import book_schema
from books_management.usecases.get_books_use_case import GetBooksUseCase
from books_management.usecases.create_book_use_case import CreateBookUseCase


logger: Logger = Provide[Container.logger]
get_books_use_case: GetBooksUseCase = Provide[Container.get_books_use_case]
create_book_use_case: CreateBookUseCase = Provide[Container.create_book_use_case]


class BookListCreateView(APIView):
    name = 'book-list'
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Retrieve a list of books, you can use __lte, __gte, __lt, __gt in the query parameters",
        manual_parameters=[
            openapi.Parameter('author', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('genre', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('price', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter(
                'published_date',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
                default="2025-01-01T00:00:00.000Z",
            ),
        ],
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
        books = get_books_use_case.execute(request.GET.dict())
        return Response(books, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new book",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=book_schema,
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="The created book",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=book_schema,
                ),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Errors in the request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"errors": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT),
                    )},
                ),
            ),
        },
    )
    def post(self, request):
        try:
            book = create_book_use_case.execute(request.data)
        except ValueError as e:
            logger.error(f"Error creating book: {e}")
            return Response({"errors": json.loads(e.json())}, status=status.HTTP_400_BAD_REQUEST)

        return Response(book, status=status.HTTP_201_CREATED)
