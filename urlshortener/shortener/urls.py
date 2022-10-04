from django.contrib import admin
from django.urls import path

from .views import ShortURLView
from .views import RedirectToLongURLView


app_name = 'shortener'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ShortURLView.as_view(), name='index'),
    path('redirect/<str:short_url>', RedirectToLongURLView.as_view(), name='long_url'),
]