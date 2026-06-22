"""Формы, через которые пользователь меняет данные на сайте."""

from django import forms
from django.contrib.auth import get_user_model

from .constants import (
    DATETIME_INPUT_FORMAT,
    TEXTAREA_COLS,
    TEXTAREA_ROWS,
)
from .models import Comment, Post

User = get_user_model()


class PostForm(forms.ModelForm):
    """Форма для поста, одна и для создания, и для редактирования."""

    pub_date = forms.DateTimeField(
        input_formats=(DATETIME_INPUT_FORMAT,),
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format=DATETIME_INPUT_FORMAT,
        ),
    )

    class Meta:
        model = Post
        exclude = ('author', 'created_at')
        widgets = {
            'text': forms.Textarea(
                attrs={'cols': TEXTAREA_COLS, 'rows': TEXTAREA_ROWS},
            ),
        }


class CommentForm(forms.ModelForm):
    """Короткая форма, чтобы написать или поправить комментарий."""

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={'cols': TEXTAREA_COLS, 'rows': TEXTAREA_ROWS},
            ),
        }


class UserForm(forms.ModelForm):
    """Форма для профиля, где пользователь правит свои данные."""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
