"""Формы, через которые пользователь меняет данные на сайте."""

from django import forms
from django.contrib.auth import get_user_model

from .models import Comment, Post

User = get_user_model()


class PostForm(forms.ModelForm):
    """Форма для поста, одна и для создания, и для редактирования."""

    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    """Короткая форма, чтобы написать или поправить комментарий."""

    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):
    """Форма для профиля, где пользователь правит свои данные."""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
