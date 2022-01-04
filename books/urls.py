from django.urls import path

from . import views

urlpatterns = [
    path('', views.bookView, name='books-list'),
   
]
