from django.urls import path

from books_management.adapters.controllers.book_list_create_views import BookListCreateView
from books_management.adapters.controllers.book_retrieve_update_destroy_view import BookRetrieveUpdateDestroyView
from books_management.adapters.controllers.average_price_view import AveragePriceView

urlpatterns = [
    path('book', BookListCreateView.as_view(), name=BookListCreateView.name),
    path('book/<str:book_id>/', BookRetrieveUpdateDestroyView.as_view(), name=BookRetrieveUpdateDestroyView.name),
    path('book/average/<int:year>', AveragePriceView.as_view(), name=AveragePriceView.name),
]
