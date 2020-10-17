from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('about', views.about , name='about'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('favorite_view', views.favorite_view, name='favo'),
    path('logout', views.logout_view, name='logout'),
]