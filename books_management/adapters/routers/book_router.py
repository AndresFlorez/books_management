from django.urls import path

from books_management.adapters.controllers.book_views import BookRetrieveUpdateDestroy, BookListCreate

urlpatterns = [
    path('book', BookListCreate.as_view(), name='book_list'),
    path('book/<str:book_id>/', BookRetrieveUpdateDestroy.as_view(), name='book_detail'),
]
