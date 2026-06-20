"""Админка блога, чтобы удобно смотреть и править записи."""

from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории в админке, с поиском и быстрым снятием с публикации."""

    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('title', 'description', 'slug')
    list_filter = ('is_published', 'created_at')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Места публикаций в админке, без особых наворотов."""

    list_display = ('name', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published', 'created_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Посты в админке: видно автора, дату и статус публикации."""

    list_display = (
        'title',
        'author',
        'category',
        'location',
        'pub_date',
        'is_published',
    )
    list_editable = ('is_published',)
    search_fields = ('title', 'text', 'author__username')
    list_filter = ('is_published', 'pub_date', 'category')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Комментарии в админке, чтобы быстро найти текст или автора."""

    list_display = ('post', 'author', 'created_at')
    search_fields = ('text', 'author__username', 'post__title')
    list_filter = ('created_at',)
