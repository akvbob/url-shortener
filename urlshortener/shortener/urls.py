from django.contrib import admin
from django.urls import path

from .views import ShortURLView
from .views import LocateToLongURLView


app_name = 'shortener'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ShortURLView.as_view(), name='index'),
    path('<str:short_url>', LocateToLongURLView.as_view(), name='long_url'),
]