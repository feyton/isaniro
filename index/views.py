from blog.models import Post
from django.shortcuts import render


# Create your views here.
def home(request):
    posts = Post.objects.filter(published=True).order_by("-published_date")
    return render(request, "index.html", {"posts": posts})
