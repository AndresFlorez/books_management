from django.urls import path

from books_management.adapters.controllers.book_views import (
    BookRetrieveUpdateDestroyView,
    BookListCreateView,
    AveragePriceView,
)

urlpatterns = [
    path('book', BookListCreateView.as_view(), name='book-list'),
    path('book/<str:book_id>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
    path('book/average/<int:year>', AveragePriceView.as_view(), name='average-price'),
]
