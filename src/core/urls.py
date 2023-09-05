from django.contrib import admin
from django.contrib.staticfiles import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="OpenGram API",
        default_version="v0.1.0",
        description=(
            "Web-based Social network for "
            "communicating photos with open source"
        ),
        contact=openapi.Contact(email="Morbid6dead@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("api/user/", include("user.urls"), name="user"),
    path("api/data/", include("post.urls"), name="post"),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger",
    ),
    re_path(r"^static/(?P<path>.*)$", views.serve),
]
urlpatterns += staticfiles_urlpatterns()
