from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# from .models import Course, Student
from django.contrib import admin as admin_r

# Create your views here.
# def index(request):
#     if not request.user.is_authenticated :
#         return HttpResponseRedirect(reverse("login"))
#     else :
#         if not request.user.is_staff :
#             return render(request, "users/index.html")
#         else :
#             return HttpResponseRedirect(reverse("admin"))

# def login_view(request):
#     if request.user.is_authenticated :
#         if not request.user.is_staff :
#             return HttpResponseRedirect(reverse("index"))
#         else :
#             return HttpResponseRedirect(reverse("admin"))
#     if request.method == "POST" :
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)
#         if user is not None :
#             login(request , user)
#             if not user.is_staff :
#                 return HttpResponseRedirect(reverse("index"))
#             else :
#                 return HttpResponseRedirect(reverse("admin"))
#         return render(request, "users/login.html", {
#             "message": "Invalid Credential."
#         })
#     return render(request, "users/login.html")

# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("index"))

def about(request):
    return render(request, "users/about.html")