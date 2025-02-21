"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from books_management.adapters.routers.book_router import urlpatterns as book_router
from books_management.adapters.routers.health_check_router import urlpatterns as health_check_router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title='Mi API',
        default_version='v1',
        description='API',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        'books-management/',
        include(
            [
                path('admin/', admin.site.urls),
                path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
                path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
                path('', include(health_check_router)),
                path('', include(book_router)),
                re_path(
                    r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'
                ),
                path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            ]
        ),
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
