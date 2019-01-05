from django.urls import include, path

from .views import ws

urlpatterns = [path("ws/", ws)]
