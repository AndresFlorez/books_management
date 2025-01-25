from django.urls import path

from books_management.adapters.controllers.health_check_view import HealthCheckView


urlpatterns = [
    path("health_check", HealthCheckView.as_view(), name="health_check"),
]
