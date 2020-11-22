from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('about_view', views.about_view , name='about_view'),
    path('favorite_view', views.favorite_view, name='favo'),
    path('add_favorite', views.add_favorite, name='favorite'),
    path('remove_favorite', views.remove_favorite, name='remove_favorite'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('add_user', views.add_user, name='add_user'),
    path('add', views.add_view, name='add_view'),
    path('add_product', views.add_product, name='add_product'),
    path('thammart', views.thammart, name='thammart'),
    path('detail/<int:product_id>', views.detail, name='detail'),
    path('remove_product', views.remove_product, name='remove_product'),
    path('search', views.search, name='search'),
    path('edit', views.edit, name='edit'),
    path('edit_product', views.edit_product, name='edit_product'),
    path('reset_view', views.reset_view, name='reset_view'),
    path('reset', views.reset, name='reset'),
    path('forgot_view', views.forgot_view, name='forgot_view'),
    path('forgot', views.forgot, name='forgot'),
    # path('verify', views.verify, name='verify'),
    # path('check_verify', views.check_verify, name='check_verify'),
]