from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.html import strip_tags

from books.models import Book

# Create your views here.


def bookView(request, *args, **kwargs):
    books = Book.objects.filter(published=True)
    return render(request, 'pages/book.html', {'books': books})


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
