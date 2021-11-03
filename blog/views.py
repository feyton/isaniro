from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, View

from .forms import CommentForm
from .models import Category, Post, SearchTerms, Tag


class BlogListView(View):
    def get(self, *args, **kwargs):

        context = {
            'posts': Post.objects.filter(published=True).order_by('-published_date'),
            'tags': Tag.objects.all,
            'categories': Category.objects.all(),
            'tags': Tag.objects.all(),
            'featured': Post.objects.filter(published=True).order_by("-published_date")[0]
        }

        return render(self.request, 'pages/list.html', context)


list_view = BlogListView.as_view()


def post_view(request, pk, title):
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    posts = Post.objects.filter(
        published=True, category=post.category).exclude(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        context = {
            'post': post,
            'categories': categories,
            'tags': tags,
            'posts': posts
        }
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            n = {'new_comment': comment}
            context.update(n)
            messages.success(request, 'Thank you for the comment')
            return render(request, 'blog/detail.html', context)
        messages.error(request, 'Error in form')
        return render(request, 'blog/detail.html', context)

    context = {
        'form': CommentForm(),
        'post': post,
        'categories': categories,
        'tags': tags,
        'posts': posts
    }

    return render(request, 'pages/blog_details.html', context)


class DetailView(DetailView):
    template_name = 'pages/blog_details.html'
    model = Post
    context_object_name = 'post'


def category_view(request, pk, *args, **kwargs):
    cat = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(published=True, category=cat)
    context = {
        'posts': posts,
        'category': cat,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'category': cat,
        'all_posts': Post.objects.filter(published=True).order_by('-published_date')
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
    return render(request, 'blog/tag.html', context)


def search(request, *args, **kwargs):
    query_set = Post.objects.filter(published=True)
    query = request.GET.get('q')
    categories = Category.objects.all()
    if query:
        queryset = query_set.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query) | Q(category__title__icontains=query) | Q(author__name__icontains=query)).distinct()
    # else:
    #     messages.error(request, "Type a valid term")
    #     return redirect('blog')
    context = {
        'posts': queryset,
        'query': query,
        'categories': categories
    }
    terms = SearchTerms.objects.filter(Q(term__icontains=query))
    if terms:
        t = {'terms': terms}
        context.update(t)
    else:
        term = SearchTerms(term=query)
        term.save()
    return render(request, 'pages/search.html', context)


def register_hit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    session = request.session

    if post:
        post.visits += 1
        post.save()

        data = {
            'hits': post.visits
        }
        return JsonResponse(data)
