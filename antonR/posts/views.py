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


@login_required
def author_index(request):
    posts = Post.objects.select_related('author').filter(author=request.user)
    template = 'posts/follow.html'
    context = {
        'page_obj': page(request, posts),
    }
    return render(request, template, context)


@login_required
def follow_index(request):
    posts_all = Post.objects.select_related('author')
    posts = posts_all.filter(author__following__user=request.user)
    template = 'posts/follow.html'
    context = {
        'page_obj': page(request, posts),
    }
    return render(request, template, context)


def best_index(request):
    variation = 3
    posts = Post.post_obj.post_liked()
    variation_max_like = posts[0].counter_like - variation
    best_post = posts.filter(liked__gt=variation_max_like)
    template = 'posts/best.html'
    context = {
        'page_obj': page(request, best_post),
    }
    return render(request, template, context)


def hot_index(request):
    posts = Post.post_obj.post_liked()
    posts = posts.filter(
        pub_date__year__gte=timezone.now().year)
    template = 'posts/hot.html'
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


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related("group", "author")
    post_count = posts.count
    template = 'posts/profile.html'
    following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user,
        author=author).exists()
    context = {
        'user': request.user,
        'author': author,
        'post_count': post_count,
        'page_obj': page(request, posts),
        'following': following,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author_post = post.author.posts.count()
    template = 'posts/post_detail.html'
    form = CommentForm()
    comment_all = post.comments.all()
    like_count = Like.objects.filter(
        post=post,
    ).count()
    context = {
        'post': post,
        'author_post': author_post,
        'comment_all': comment_all,
        'form': form,
        'like_count': like_count,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/post_create.html'
    form = PostForm(request.POST or None,
                    files=request.FILES or None,)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:profile", request.user)
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/post_create.html'
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect("posts:post_detail")
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.pk)
    context = {'form': form, 'is_edit': True, 'post': post}
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    template = 'include/comment.html'
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect("posts:post_detail", post_id=post_id)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    if request.user.username == username:
        return redirect('posts:profile', username=username)
    following = get_object_or_404(User, username=username)
    followed = Follow.objects.filter(
        user=request.user,
        author=following,
    ).exists()
    if not followed:
        Follow.objects.create(user=request.user, author=following)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    following = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=following).delete()
    return redirect('posts:profile', username)


@login_required
def add_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    admirer = Like.objects.filter(
        post=post,
        author=request.user
    ).exists()

    if not admirer:
        Like.objects.create(post=post, author=request.user)
    else:
        Like.objects.filter(post=post, author=request.user).delete()
    return redirect('posts:index')
