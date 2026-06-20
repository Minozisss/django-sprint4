"""Вьюхи для простых страниц и аккуратных ошибок."""

from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    """Показываем страницу с рассказом о проекте."""

    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Показываем страницу с правилами для пользователей."""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Отдаем свою 404, чтобы пользователь не видел голый Django."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Отдаем страницу 500, если что-то все-таки сломалось."""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    """Показываем понятную страницу, когда CSRF-защита ругается."""
    return render(request, 'pages/403csrf.html', status=403)
