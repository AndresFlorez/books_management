from drf_yasg import openapi


book_schema = {
    'id': openapi.Schema(type=openapi.TYPE_STRING, read_only=True),
    'title': openapi.Schema(type=openapi.TYPE_STRING),
    'author': openapi.Schema(type=openapi.TYPE_STRING),
    'published_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
    'genre': openapi.Schema(type=openapi.TYPE_STRING),
    'description': openapi.Schema(type=openapi.TYPE_STRING),
    'price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
}
