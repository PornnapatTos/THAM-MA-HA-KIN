from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Thammart, Profile
from django.contrib import admin as admin_r

# Create your views here.

def register_view(request):
    if request.method == "POST" :
        user_id =  request.POST["username"]
        name = request.POST["name"]
        sname = request.POST["sname"]
        password = request.POST[""]

def index(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        return render(request, "users/index.html")

def login_view(request):
    if request.user.is_authenticated :
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST" :
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request , user)
            return HttpResponseRedirect(reverse("index"))
        return render(request, "users/login.html", {
            "message": "Invalid Credential."
        })
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def favorite_view(request):
    favourite = Profile.objects.filter(idStudent = request.user.user)
    return {"favo": favourite.values_list('p_fav' , flat = True)}

def about(request):
    return render(request, "users/about.html")