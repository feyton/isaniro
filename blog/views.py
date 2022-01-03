from django.contrib import messages
from django.core import paginator
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, View
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CommentForm
from .models import Category, Comment, Post, SearchTerms, Tag
from .serializer import CommentSerializer


class BlogListView(View):
    def get(self, *args, **kwargs):
        posts = Post.objects.filter(
            published=True)
        paginator = Paginator(posts, 7)
        page_var = "page"
        page = self.request.GET.get(page_var, 1)
        try:
            paginated_data = paginator.page(page)
        except PageNotAnInteger:
            paginated_data = paginator.page(1)
        except EmptyPage:
            paginated_data = paginator.page(paginator.num_pages)

        context = {
            'posts': paginated_data,
            "recent_posts": posts[:5],
            'tags': Tag.objects.all(),
            'categories': Category.objects.all(),
            'tags': Tag.objects.all(),
            'featured': posts[0]
        }

        return render(self.request, 'blog.html', context)


list_view = BlogListView.as_view()


def post_view(request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    posts = Post.objects.filter(
        published=True).exclude(pk=pk)[:5]

    context = {
        'post': post,
        'categories': categories,
        'tags': tags,
        'posts': posts
    }

    return render(request, 'detail.html', context)


def load_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post, approved=True)
    serialized = CommentSerializer(comments, many=True)
    return Response(serialized.data)


class GetPostComments(APIView):

    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        print(post.title)
        comments = Comment.objects.filter(approved=True, post=post)
        serialized = CommentSerializer(comments, many=True)
        return Response(serialized.data)


comment_view = GetPostComments.as_view()


def add_comment(request, pk, *args, **kwargs):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        comment = Comment()
        comment.name = request.POST.get("name")
        comment.email = request.POST.get("email")
        comment.body = request.POST.get("body")
        comment.approved = True
        comment.post = post
        comment.save()
        data = {"created": "true"}
        return JsonResponse(data)
    else:
        data = {"created": "false"}
        return JsonResponse(data)


def category_view(request, pk, *args, **kwargs):
    cat = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(published=True, category=cat)
    context = {
        'posts': posts,
        'category': cat,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),

    }
    return render(request, 'pages/categories.html', context)


def tag_view(request, pk, *args, **kwargs):
    tag = get_object_or_404(Tag, pk=pk)
    posts = tag.posts.filter(published=True)
    cats = Category.objects.all()
    context = {'posts': posts,
               'tag': tag,
               'tags': Tag.objects.all(),
               'categories': cats}
    return render(request, 'pages/categories.html', context)


def search(request, *args, **kwargs):
    query_set = Post.objects.filter(published=True)
    query = request.GET.get('q')
    categories = Category.objects.all()
    if query:
        queryset = query_set.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__title__icontains=query) | Q(category__title__icontains=query) | Q(author__name__icontains=query)).distinct()

    context = {
        'posts': queryset,
        'query': query,
        'categories': categories
    }
    # terms = SearchTerms.objects.filter(Q(term__icontains=query))
    # if terms:
    #     t = {'terms': terms}
    #     context.update(t)
    # else:
    #     term = SearchTerms(term=query)
    #     term.save()
    return render(request, 'pages/search.html', context)


def record_post_like(request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    post.likes += 1
    post.save()
    return JsonResponse({'likes': post.likes})
