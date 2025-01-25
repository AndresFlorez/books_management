from django.http import HttpResponse
from django.views import View
from rest_framework import status
from rest_framework import permissions


class HealthCheckView(View):
    status_code_ok = status.HTTP_200_OK
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        """The health check endpoints will respond with a 200 status code if the service is up and running."""
        return HttpResponse("ok", status=self.status_code_ok)
