from django.contrib import admin

from .models import Author, Category, Comment, Post, SearchTerms, Service, Tag


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on', 'published')
    list_filter = ('author', 'published')
    search_fields = ('title', 'author', 'content')


admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Tag)
admin.site.register(SearchTerms)
admin.site.register(Author)
