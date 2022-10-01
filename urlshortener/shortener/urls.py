from django.contrib import admin
from django.urls import path

from .views import IndexView


app_name = 'shortener'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
]