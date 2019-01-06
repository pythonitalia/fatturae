from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import dispatcher

urlpatterns = [path("ws/", csrf_exempt(dispatcher))]
