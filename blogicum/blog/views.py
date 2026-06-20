"""Вьюхи блога: собираем данные и отдаем нужные шаблоны."""

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .constants import POSTS_ON_PAGE
from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post

User = get_user_model()


def get_published_posts(posts=Post.objects):
    """Берем только те посты, которые уже можно показывать всем."""
    return posts.annotate(
        comment_count=Count('comments')
    ).select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    ).order_by('-pub_date')


def paginate(request, posts):
    """Разбиваем список постов на страницы по общему лимиту."""
    return Paginator(posts, POSTS_ON_PAGE).get_page(request.GET.get('page'))


def get_post_for_user(post_id, user):
    """Достаем пост: автору свой виден всегда, остальным только публичный."""
    post = get_object_or_404(
        Post.objects.annotate(comment_count=Count('comments')).select_related(
            'author', 'category', 'location'
        ),
        pk=post_id,
    )
    if post.author == user:
        return post
    return get_object_or_404(get_published_posts(), pk=post_id)


def index(request):
    """Показываем главную ленту с опубликованными постами."""
    context = {
        'page_obj': paginate(request, get_published_posts()),
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Показываем пост, форму комментария и сами комментарии."""
    post = get_post_for_user(post_id, request.user)
    context = {
        'post': post,
        'form': CommentForm(),
        'comments': post.comments.select_related('author'),
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Показываем посты из одной опубликованной категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    context = {
        'category': category,
        'page_obj': paginate(
            request,
            get_published_posts(category.posts.all()),
        ),
    }
    return render(request, 'blog/category.html', context)


def profile(request, username):
    """Показываем профиль и публикации конкретного пользователя."""
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).annotate(
        comment_count=Count('comments')
    ).select_related('author', 'category', 'location').order_by('-pub_date')
    if request.user != profile_user:
        posts = get_published_posts(posts)
    context = {
        'profile': profile_user,
        'page_obj': paginate(request, posts),
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    """Даем пользователю поменять свои данные профиля."""
    form = UserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})


@login_required
def create_post(request):
    """Создаем пост и сразу закрепляем текущего пользователя автором."""
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        form.save_m2m()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    """Разрешаем автору поправить свой пост."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post.id)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    """Удаляем пост после подтверждения автора."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', {'form': form})


@login_required
def add_comment(request, post_id):
    """Добавляем комментарий к публичному посту."""
    post = get_object_or_404(get_published_posts(), pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('blog:post_detail', post_id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Разрешаем автору комментария поправить текст."""
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
        post_id=post_id,
    )
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(
        request,
        'blog/comment.html',
        {'form': form, 'comment': comment},
    )


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаляем комментарий после подтверждения автора."""
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
        post_id=post_id,
    )
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})
