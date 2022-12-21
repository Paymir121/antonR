from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.utils import timezone


from .forms import PostForm, CommentForm
from .models import Group, Post, User, Follow, Like
from .paginator import page


@cache_page(20)
def index(request):
    posts = Post.objects.select_related('group', "author")
    template = 'posts/index.html'
    context = {
        'page_obj': page(request, posts),
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related("group", "author")
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': page(request, posts),
    }
    return render(request, template, context)




def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author_post = post.author.posts.count()
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'author_post': author_post,
    }
    return render(request, template, context)
