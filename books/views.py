import json
from django.conf import settings
from django.core import signing
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import strip_tags
from books.forms import AddressForm, AnonymousAddressForm

from books.models import Address, AnonymousAddress, AnonymousOrder, AnonymousPayedBook, AnonymousPayment, Book, Customer, Order, OrderItem, PayedBook, Payment
from books.utils import cookieCart, handle_payment, notify_email, ref_code_generator, sign_book_token, verifyTransaction

# Create your views here.


def bookView(request, *args, **kwargs):
    books = Book.objects.filter(published=True)
    return render(request, 'pages/book.html', {'books': books})


def bookDetail(request, pk, *args, **kwargs):
    book = Book.objects.get(id=pk)
    return render(request, 'book-detail.html', {'book': book})


def send_sample(email, book, user, request):
    from django.template.loader import render_to_string
    html = render_to_string("email/sample_book.html", {'book': book, "user": user, "request": request}
                            )
    plain = strip_tags(html)
    EmailFrom = "'Isaniro Books'<books@isaniro.com>"
    mail = EmailMultiAlternatives("Incamake y'igitabo '%s'" %
                                  book.title, html, EmailFrom, [email])
    mail.attach_alternative(html, "text/html")
    # mail.subject = "Incamake y'igitabo '%s'" % book.title
    # mail.body = html
    mail.attach_file(book.sample.path)
    # mail.to([email])
    mail.send(fail_silently=True)


def handleSampleRequest(request, pk, *args, **kwargs):
    book = get_object_or_404(Book, pk=pk)
    name = request.GET.get('name')
    email = request.GET.get('email')
    user = {"name": name, 'email': email}

    send_sample(email, book, user, request)
    return JsonResponse({"sent": True, "title": book.title})


def book_download(request, token, *args, **kwargs):
    signer = signing.TimestampSigner(
        key=settings.BOOK_SIGNATURE, salt="isaniro")
    try:
        data = signer.unsign_object(token)
        book = Book.objects.get(id=data['book'])
        return redirect(book.download_link)
    except Exception:
        print(Exception)
        return HttpResponseForbidden("Expired link")


def cart_view(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(
            customer=customer, completed=False)
        items = order.orderitem_set.all()
        cart_total = order.get_cart_total
        cart_quantity = order.get_cart_items
        context = {
            'items': items,
            'cart_total': cart_total,
            'cart_quantity': cart_quantity
        }

        return render(request, "cart.html", context)
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        cookie_cart = cookieCart(request)
        context = {
            'items': cookie_cart['items'],
            'cart_total': cookie_cart['cart_total'],
            'cart_quantity': cookie_cart['cart_quantity']
        }
        return render(request, "cart.html", context)


def addToCart(request, pk):
    book = Book.objects.get(id=pk)
    if not book.downloadable_copy:
        return HttpResponseForbidden("The book is not available")
    action = request.GET.get('action')
    if book:
        if request.user.is_authenticated:
            customer, created = Customer.objects.get_or_create(
                user=request.user)
            order, created = Order.objects.get_or_create(
                customer=customer, completed=False)
            orderItem, created = OrderItem.objects.get_or_create(
                order=order, product=book)
            if action == 'remove':
                orderItem.delete()
            else:
                orderItem.quantity = 1
                orderItem.save()
            return redirect("cart-view")
        else:
            return redirect("cart-view")
    return Http404("Not found")


def checkout_view(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(
            customer=customer, completed=False)
        if created:
            cookie_items = cookieCart(request)
            for item in cookie_items:
                try:
                    product = Book.objects.get(id=item['id'])
                    orderItem = OrderItem.objects.create(
                        product=product, order=order, quantity=item['quantity'])

                except:
                    pass

        items = order.orderitem_set.all()
        cart_total = order.get_cart_total
        cart_quantity = order.get_cart_items
        try:
            address = Address.objects.get(customer=customer)
            form = AddressForm(instance=address)
        except Exception:
            form = AddressForm()
        context = {
            'items': items,
            'cart_total': cart_total,
            'cart_quantity': cart_quantity,
            'form': form
        }

        if request.method == 'POST':
            try:
                address = Address.objects.get(customer=customer)
                form = AddressForm(request.POST, instance=address)
            except:
                form = AddressForm(request.POST)
            if not form.is_valid():
                context['form'] = form
                return render(request, 'checkout.html', context)
            if form.is_valid():
                print('Valid')

                address = form.save(commit=False)

                address.customer = customer
                address = address.save()
                print(address)
                host = request.get_host()
                protocol = request.scheme
                redirect_url = "%s://%s/book/payment-check" % (protocol, host)
                data = {
                    'transaction_id': order.order_id,
                    'get_cart_total': order.get_cart_total,
                    'customer_id': order.customer.user.id,
                    'customer_email': order.customer.user.email,
                    'name': order.customer.user.get_full_name(),
                }
                print(order.order_id)
                link = handle_payment(data, redirect_url)
                return JsonResponse({"link": link})

        return render(request, 'checkout.html', context)
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        cookie_cart = cookieCart(request)
        try:
            if not request.session.session_key:
                request.session.save()
            address = AnonymousAddress.objects.get(
                session_key=request.session.session_key)
        except:
            address = None
        form = AnonymousAddressForm(instance=address)
        context = {
            'items': cookie_cart['items'],
            'cart_total': cookie_cart['cart_total'],
            'cart_quantity': cookie_cart['cart_quantity'],
            'form': form
        }
        if request.method == 'POST':
            print(address)
            if address:
                form = AnonymousAddressForm(request.POST, instance=address)
            else:
                form = AnonymousAddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                if not request.session.session_key:
                    request.session.save()
                address.session_key = request.session.session_key
                address.save()
                order, created = AnonymousOrder.objects.get_or_create(
                    address=address, completed=False)
                if created:
                    for item in cookie_cart['items']:
                        try:
                            book = Book.objects.get(id=item.product.id)
                            order.products.add(book)
                            order.save()
                        except:
                            pass
                host = request.get_host()
                protocol = request.scheme
                print(address)
                redirect_url = "%s://%s/book/payment-check" % (protocol, host)
                data = {
                    'transaction_id': order.order_id,
                    'get_cart_total': cookie_cart['cart_total'],
                    'customer_id': ref_code_generator(),
                    'customer_email': address.email,
                    'name': address.full_name,
                    'telephone': address.telephone
                }
                print(order.order_id)
                link = handle_payment(data, redirect_url)
                return JsonResponse({"link": link})
            else:
                context['form'] = form
                return render(request, 'checkout-anonymous.html', context)
        return render(request, 'checkout-anonymous.html', context)


def provisionBooks(customer, payment, order):
    items = order.orderitem_set.all()
    for item in items:
        payedbook = PayedBook.objects.get_or_create(
            customer=customer, payment=payment, book=item.product)
    context = {

    }
    notify_email('email/download_book.html', customer.user.email, {})
    return True


def payment_check(request):
    status = request.GET.get('status', None)
    tx_ref = request.GET.get('tx_ref', None)
    tx_id = request.GET.get('transaction_id', None)
    info = verifyTransaction(tx_id)
    if info['data'] and info['data']['status'] == 'successful':
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(order_id=tx_ref)
                payment = Payment.objects.get(payment_id=tx_id)
            except:
                payment = Payment()
                payment.payment_id = tx_id
                payment.order = order
                payment.customer = order.customer
                payment.amount = info['data']['charged_amount']
                payment.currency = info['data']['currency']
                payment.amount_settled = info['data']['amount_settled']
                payment.status = info['data']['status']
                payment = payment.save()
            items = order.orderitem_set.all()
            cart_total = order.get_cart_total
            cart_quantity = order.get_cart_items
            order.notify_seller()
            order.notify_customer()
            order.completed = True
            for item in order.orderitem_set.all():
                item.ordered = True
                item.save()
                item.record_order()
                data = {
                    'book': item.product.id,
                    'payment': payment.id,
                    'customer': order.customer.id,
                    'payment_id': tx_id
                }

                try:
                    PayedBook.objects.get(
                        customer=order.customer, payment=payment, book=item.product)
                except:
                    token = sign_book_token(data)
                    PayedBook.objects.create(
                        customer=order.customer, payment=payment, book=item.product, token=token)
            order.save()
            context = {
                "order": order or None,
                "items": items or None,
                "total": cart_total or None,
                "quantity": cart_quantity or None
            }
            response = render(request, "payment-success.html", context)
            response.delete_cookie('cart')
            return response
        else:
            try:
                payment = AnonymousPayment.objects.get(payment_id=tx_id)
                address = AnonymousAddress.objects.get(
                    email=info['data']['customer']['email'])
                order = AnonymousOrder.objects.get(address=address)
                print("It exists")
            except:
                payment = AnonymousPayment()
                try:
                    address = AnonymousAddress.objects.get(
                        email=info['data']['customer']['email'])
                    order = AnonymousOrder.objects.get(address=address)
                except:
                    return HttpResponse("This one was not found")
                payment.payment_id = tx_id
                payment.order = order
                payment.session_key = address.session_key
                payment.amount = info['data']['charged_amount']
                payment.currency = info['data']['currency']
                payment.amount_settled = info['data']['amount_settled']
                payment.status = info['data']['status']
                payment.email = address.email
                payment = payment.save()
                print("Payment info generated")
                print(payment)
            items = order.products.all()
            cart_total = payment.amount
            cart_quantity = order.products.all().count()
            order.notify_seller()
            order.notify_customer()
            order.completed = True
            for item in items:
                data = {
                    'book': item.id,
                    'payment': payment.id,
                    'customer': address.email,
                    'payment_id': tx_id
                }

                try:
                    AnonymousPayedBook.objects.get(
                        session_key=address.session_key, payment=payment, book=item)
                except:
                    token = sign_book_token(data)
                    AnonymousPayedBook.objects.create(
                        session_key=address.session_key, payment=payment, book=item, token=token)
                    item.addOrder()
                order.save()
            context = {
                "order": order or None,
                "items": items or None,
                "total": cart_total or None,
                "quantity": cart_quantity or None,
                "address": address or None
            }

            response = render(
                request, "payment-success-anonymous.html", context)
            response.delete_cookie('cart')
            return response
    return Http404("Order not exist")


def validateEmail(request, token, *args, **kwargs):
    signer = signing.TimestampSigner(
        key=settings.BOOK_SIGNATURE, salt="isaniro")
    try:
        data = signer.unsign_object(token)
    except:
        return HttpResponseForbidden("Inavlid validation token")
    print(data)
    email = data['email']
    return HttpResponse("Thank you for validating your email. <br>. If your email match this <%s>, please continue Otherwise try again" % email)


def resetSession(request):
    try:
        request.session.flush()
    except:
        pass
    return redirect("/")
