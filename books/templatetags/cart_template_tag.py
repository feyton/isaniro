import json

from django import template
from books.models import Customer, Order

register = template.Library()


@register.filter
def cart_item_count(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        qs = Order.objects.filter(customer=customer, completed=False)
        if qs.exists():
            return qs[0].orderitem_set.all().count()
        return 0
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        return len(cart) or 0
