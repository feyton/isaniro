from django.contrib import admin

from .models import Address, Book, Order, OrderItem, PayedBook, Payment


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',  'published')
    list_filter = ('author', 'published')
    search_fields = ('title', 'author', 'summary')


admin.site.register(Order)
admin.site.register(Address)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(PayedBook)
