
from django.urls import path
from pages import views
from .views import success
from django.contrib import admin
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path("upload", views.test, name='upload'),
    path("success", success, name='success')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

