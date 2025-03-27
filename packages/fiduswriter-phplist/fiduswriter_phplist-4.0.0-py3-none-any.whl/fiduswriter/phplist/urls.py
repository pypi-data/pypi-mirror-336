from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        "^subscribe_email/$",
        views.subscribe_email,
        name="phplist_subscribe_email",
    ),
]
