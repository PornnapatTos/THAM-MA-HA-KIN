from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index , name='index'),
    path('', views.about , name='about'),
    # path('login', views.login_view, name='login'),
    # path('logout', views.logout_view, name='logout'),
]