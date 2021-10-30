from blog.models import Post
from django.shortcuts import redirect, render


# Create your views here.
def home(request):
    posts = Post.objects.filter(published=True).order_by("-published_date")
    return render(request, "index.html", {"posts": posts})


def add_subscriber(request):
    if request.method == "POST":
        return redirect('home')

    return redirect('home')
