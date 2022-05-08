from django.core import signing
import json
import os
import random
from datetime import datetime
from io import BytesIO

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template, render_to_string
import requests


def ref_code_generator():
    chars = "1234567890ABCDEFGHJKLMNOPQRSTYXW"
    randomstr = ''.join((random.choice(chars)) for x in range(6))
    date = datetime.now().date()
    return '%s-%s' % (date, randomstr)


def notify_email(template, email, data, message="Order completed"):
    from django.template.loader import render_to_string
    html = render_to_string(template, data)
    plain = render_to_string(template, data)
    send_mail(
        message,
        plain,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=html,
        fail_silently=True
    )


def cookieCart(request):
    from books.models import Book
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    cart_total = 0
    cart_quantity = 0
    for i in cart:
        try:
            product = Book.objects.get(id=i)
            total = product.price * cart[i]["quantity"]
            cart_total += total
            cart_quantity += cart[i]["quantity"]
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imgURL': product.imgURL
                },
                "quantity": cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)
        except:
            pass
    return {'items': items, 'cart_total': cart_total, 'cart_quantity': cart_quantity}


def handle_payment(order, redirect_link, option="mobilemoneyrwanda"):
    headers = {
        "Authorization": "Bearer %s" % settings.FLUTTER_SECRET
    }
    data = {
        "tx_ref": order['transaction_id'],
        "amount": order['get_cart_total'],
        "currency": "RWF",
        "redirect_url": redirect_link,

        "meta": {
            " consumer_id": order['customer_id']
        },
        "customer": {
            "email": order['customer_email'],
            "phoneNumber": "078724157",
            "name": order['name']},
        "customizations": {
            "title": "Isaniro Group",
            "logo": "https://res.cloudinary.com/feyton/image/upload/v1649609854/index_s5pfk0.png",
            "description": "Books That Change Lives"
        },
        "payment_options": "%s" % (option)
    }
    r = requests.post("https://api.flutterwave.com/v3/payments",
                      json=data, headers=headers)
    return r.json()['data']['link'] or None


def verifyTransaction(tx_ref):
    headers = {
        "Authorization": "Bearer %s" % settings.FLUTTER_SECRET
    }
    r = requests.get("https://api.flutterwave.com/v3/transactions/%s/verify" % tx_ref,
                     headers=headers)

    info = r.json()
    return info


def sign_book_token(data):
    signer = signing.TimestampSigner(
        key=settings.BOOK_SIGNATURE, salt="isaniro")
    token = signer.sign_object(data)
    return token
