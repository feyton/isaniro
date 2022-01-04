from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',  'published')
    list_filter = ('author', 'published')
    search_fields = ('title', 'author', 'summary')
