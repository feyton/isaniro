from blog.models import Category, Post, Tag
from django.shortcuts import redirect, render


# Create your views here.
def home(request):
    posts = Post.objects.filter(published=True).order_by("-published_date")
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
