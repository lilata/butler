from django.contrib import admin
from django.urls import include, path

from core import views as core_views

from . import views

toplevel_urlpatterns = [
    path("ping/", views.PingView.as_view(), name="ping"),
]
app_name = "butler"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("_/", include(toplevel_urlpatterns)),
    path("core/", include("core.urls", namespace="core")),
    path(
        "s/<str:alias>/",
        core_views.ShortenerRedirectView.as_view(),
        name="shortener_redirect",
    ),
]