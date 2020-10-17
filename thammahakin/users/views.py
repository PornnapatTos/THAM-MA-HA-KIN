from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Thammart, Profile
from django.contrib import admin as admin_r
from django.contrib.auth.models import User

# Create your views here.

def register_view(request):
    return render(request, "users/register.html")

def add_user(request) :
    if request.method == "POST" :
        user_id =  request.POST["username"]
        name = request.POST["name"]
        sname = request.POST["sname"]
        password = request.POST["password"]
        c_password = request.POST["cpassword"]
        mail = request.POST["mail"]
        phone = request.POST["phone"]
        line = request.POST["line"]
        ig = request.POST["ig"]
        face = request.POST["face"]

        if user_id and name and sname and password and c_password and mail and line and phone and ig and face :
            user = Profile.objects.filter(p_user=user_id)
            print(user)
            if not user:
                if password == c_password :
                    User.objects.create_user(username=user_id, password=password, email=mail)
                    Profile.objects.create(p_user=user_id,p_name=name,p_sname=sname,p_mail=mail,p_line=line,p_facebook=face,p_phone=phone,p_instragram=ig)
                    return render(request, "users/login.html", {
                        "message": "register success!"
                    })
                else :
                    return render(request, "users/register.html", {
                        "message": "fail to register!"
                    })
            else :
                return render(request, "users/register.html", {
                        "message": "you are already in website!"
                    })
        else :
            return render(request, "users/register.html", {
                        "message": "Please complete this registration form!"
                    })

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
    favourite = Profile.objects.get(p_user = request.user.username)
    print(favourite.p_fav.all())
    return  render(request, "Thamahakinview/favo.html", {"favos": favourite.p_fav.all()})

# def trending_now

def about(request):
    return render(request, "users/about.html")