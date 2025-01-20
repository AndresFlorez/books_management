from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dependency_injector.wiring import Provide
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from books_management.commons.logger import Logger
from books_management.container.container import Container
from books_management.usecases.books_price_average_usecases import AveragePriceUseCase

logger: Logger = Provide[Container.logger]
average_price_use_case: AveragePriceUseCase = Provide[Container.average_price_use_case]


class AveragePriceView(APIView):
    name = 'average-price'

    @swagger_auto_schema(
        operation_description="Retrieve the average price of books published in a given year",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="The average price",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"average_price": openapi.Schema(type=openapi.TYPE_NUMBER)},
                ),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Errors in the request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
        parameters=[openapi.Parameter('year', openapi.IN_PATH, type=openapi.TYPE_INTEGER)],
    )
    def get(self, request, year):
        """Retrieve the average price of books published in a given year"""
        try:
            average_price = average_price_use_case.execute(year)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"average_price": average_price}, status=status.HTTP_200_OK)
