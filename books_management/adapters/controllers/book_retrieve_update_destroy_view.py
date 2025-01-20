import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from dependency_injector.wiring import Provide
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from books_management.commons.custom_exceptions import RecordNotFoundException
from books_management.commons.logger import Logger
from books_management.container.container import Container
from books_management.commons.swagger_schemas import book_schema
from books_management.usecases.get_book_use_case import GetBookUseCase
from books_management.usecases.update_book_use_case import UpdateBookUseCase
from books_management.usecases.delete_book_use_case import DeleteBookUseCase

logger: Logger = Provide[Container.logger]
get_book_use_case: GetBookUseCase = Provide[Container.get_book_use_case]
update_book_use_case: UpdateBookUseCase = Provide[Container.update_book_use_case]
delete_book_use_case: DeleteBookUseCase = Provide[Container.delete_book_use_case]


class BookRetrieveUpdateDestroyView(APIView):
    name = 'book-detail'
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Retrieve a book",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="The book",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=book_schema,
                ),
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Errors in the request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
        parameters=[openapi.Parameter('book_id', openapi.IN_PATH, type=openapi.TYPE_STRING)],
    )
    def get(self, request, book_id):
        """Retrieve a book"""
        try:
            book = get_book_use_case.execute(book_id)
        except ValueError as e:
            logger.error(f"Error getting book: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except RecordNotFoundException as e:
            logger.error(f"Error getting book: {e}")
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(book, status=status.HTTP_200_OK)

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
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Errors in the request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT),
                        )
                    },
                ),
            ),
        },
        parameters=[openapi.Parameter('book_id', openapi.IN_PATH, type=openapi.TYPE_STRING)],
    )
    def put(self, request, book_id):
        """Update a book"""
        try:
            book = update_book_use_case.execute(book_id, request.data)
        except ValueError as e:
            logger.error(f"Error updating book: {e}")
            if hasattr(e, 'json'):
                return Response({"errors": json.loads(e.json())}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(book, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete a book",
        responses={status.HTTP_200_OK: openapi.Response(description="No content")},
        parameters=[openapi.Parameter('book_id', openapi.IN_PATH, type=openapi.TYPE_STRING)],
    )
    def delete(self, request, book_id):
        """Delete a book"""
        delete_book_use_case.execute(book_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
