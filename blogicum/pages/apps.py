"""Настройка маленького приложения со статичными страницами."""

from django.apps import AppConfig


class PagesConfig(AppConfig):
    """Подключаем страницы вроде "О проекте" и "Правила"."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
