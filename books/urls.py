from django.urls import path

from . import views

urlpatterns = [
    path('', views.bookView, name='books-list'),
    path('detail/<pk>/<slug>/', views.bookView, name='books-view'),
    path('download/<pk>/<slug>/', views.handleSampleRequest, name='sample-download'),


]
