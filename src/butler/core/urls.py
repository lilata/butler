from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("shorten/", views.ShortenerView.as_view(), name="shorten"),
    path("comments/", views.CommentsView.as_view(), name="comments"),
]
