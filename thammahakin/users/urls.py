from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('about_view', views.about_view , name='about_view'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('favorite_view', views.favorite_view, name='favo'),
    path('logout', views.logout_view, name='logout'),
    path('add_user', views.add_user, name='add_user'),
    path('add', views.add_view, name='add_view'),
    path('add_product', views.add_product, name='add_product'),
    path('thammart', views.thammart, name='thammart'),
    path('detail', views.detail, name='detail'),
    path('remove_product', views.remove_product, name='remove_product'),
]