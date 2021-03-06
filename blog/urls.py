from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_view, name='blog'),
    path('post/<pk>/<title>/', views.post_view, name='blog-detail'),
    path('category/<pk>/<title>/', views.category_view, name='category-view'),
    path('tag/<pk>/<name>/', views.tag_view, name='tag-view'),
    path('search/', views.search, name='search-result'),
    path('view/<pk>/', views.comment_view, name="comments-view"),
    path('add-comment/<pk>/', views.add_comment, name="add-comment"),
    path('add-like/<pk>/', views.record_post_like, name="add-post-like"),
]
