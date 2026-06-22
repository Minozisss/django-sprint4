"""Главная карта адресов, откуда запросы расходятся по приложениям."""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path
from django.views.generic import CreateView

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'auth/registration/',
        CreateView.as_view(
            form_class=UserCreationForm,
            success_url='/auth/login/',
            template_name='registration/registration_form.html',
        ),
        name='registration',
    ),
    path('auth/', include('django.contrib.auth.urls')),
    path('pages/', include('pages.urls')),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
