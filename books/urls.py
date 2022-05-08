from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('', views.bookView, name='books-list'),
    path('detail/<pk>/<slug>/', views.bookView, name='books-view'),
    path('download/<pk>/<slug>/', views.handleSampleRequest, name='sample-download'),
    path("add-to-cart/<pk>/", views.addToCart, name='add-to-cart'),
    path("cart/", views.cart_view, name='cart-view'),
    path('checkout/', views.checkout_view, name='checkout-view'),
    path("book-download/<token>/", views.book_download, name='book-download'),
    path("book/detail/<pk>/<slug>", views.bookDetail, name="book-view"),
    path('payment-check', views.payment_check, name='payment-check')


]
