from django.core.mail import EmailMessage
from django.shortcuts import render

# Create your views here.


def bookView(request, *args, **kwargs):
    return render(request, 'pages/book.html')


def send_sample(email, book, user):
    from django.template.loader import render_to_string
    html = render_to_string("email/sample_book.html", {'book': book, "user": user}
                            )
    plain = render_to_string("email/sample_book.html",
                             {'book': book, "user": user})

    mail = EmailMessage()
    mail.subject = "Book sample for %s" % book.title
    mail.body = html
    mail.attach_file(book.sample)
    mail.to([email])
