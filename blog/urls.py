from django.contrib.staticfiles.urls import urlpatterns
from django.urls import path
from . import views


urlpatterns= [
    path("", views.index)
]