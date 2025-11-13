from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    re_path(r'^(?P<path>.*)/?$', views.dynamic_page, name='dynamic_page'),
]