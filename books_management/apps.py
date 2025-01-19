from django.apps import AppConfig
from books_management.container.container import container


class BookManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books_management'

    def ready(self):
        """Wire the container when the app is ready."""
        container.wire(
            packages=[
                'books_management.adapters.controllers',
            ]
        )
