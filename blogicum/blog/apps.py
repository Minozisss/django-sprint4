"""Настройка приложения с публикациями и комментариями."""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Подключаем блог в проект и задаем нормальное имя в админке."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Блог'
