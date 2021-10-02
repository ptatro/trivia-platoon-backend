from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from trivia import settings
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
import environ
from pathlib import Path
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SWAGGER_VALUE = env("SWAGGER")

if SWAGGER_VALUE == "True":
    urlpatterns = [
        path("admin/", admin.site.urls),
        path("api/", include("game.urls")),
        path("auth/", include("accounts.urls")),
        path(
            "openapi/",
            get_schema_view(
                title="trivia",
                description="API for all things …",
                version="1.0.0",
                public=True,
                permission_classes=[AllowAny],
            ),
            name="openapi-schema",
        ),
        path(
            "swagger-ui/",
            TemplateView.as_view(
                template_name="swagger-ui.html",
                extra_context={"schema_url": "openapi-schema"},
            ),
            name="swagger-ui",
        ),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("game.urls")),
    path("auth/", include("accounts.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)