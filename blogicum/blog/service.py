"""Небольшие помощники для выборок, чтобы views не пухли."""

from django.db.models import Count
from django.utils import timezone

from .models import Post


def get_posts(posts=Post.objects, filter_published=True, count_comments=True):
    """Готовим queryset постов с нужными фильтрами и счетчиками."""
    posts = posts.select_related('author', 'category', 'location')
    if count_comments:
        posts = posts.annotate(comment_count=Count('comments'))
    if filter_published:
        posts = posts.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
    return posts.order_by('-pub_date')
