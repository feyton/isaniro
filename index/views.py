from blog.models import Category, Post, Tag, Service
from django.shortcuts import redirect, render


# Create your views here.
def home(request):
    posts = Post.objects.filter(published=True).order_by("-published_date")[:5]
    cats = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'posts': posts,
        'categories': cats,
        'tags': tags
    }
    return render(request, "index.html", context)


def add_subscriber(request):
    if request.method == "POST":
        return redirect('home')

    return redirect('home')


def service_view(request):
    services = Service.objects.filter(available=True)
    context = {'services': services}
    return render(request, "pages/services.html", context)
