from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Thammart, Profile
from django.contrib import admin as admin_r
from django.contrib.auth.models import User
from googleapiclient.http import MediaFileUpload
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

# Connect google drive api

from Google import Create_Service
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPE = ['https://www.googleapis.com/auth/drive']

floder_id = '1gBM6Rs4wWwnEcZroAyFLDfLcvTkLf5id'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPE)

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

        if user_id and name and sname and password and c_password :
            user = Profile.objects.filter(p_user=user_id)
            print(user)
            if not user:
                if password == c_password :
                    User.objects.create_user(username=user_id, password=password,)
                    Profile.objects.create(p_user=user_id,p_name=name,p_sname=sname)
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
        products = Thammart.objects.all()
        if request.method == "POST" :
            if 'intro' in request.POST: products = Thammart.objects.filter(t_cat='food')
            elif 'food' in request.POST: products = Thammart.objects.filter(t_cat='food')
            elif 'closet' in request.POST: products = Thammart.objects.filter(t_cat='closet')
            elif 'accessary' in request.POST: products = Thammart.objects.filter(t_cat='accessary')
            elif 'beauty' in request.POST: products = Thammart.objects.filter(t_cat='beauty')
            elif 'electronic' in request.POST: products = Thammart.objects.filter(t_cat='electronic')
            elif 'others' in request.POST: products = Thammart.objects.filter(t_cat='others')
        paths = []
        for product in products :
            paths.append(f'https://drive.google.com/uc?id={product.t_image}')
        return render(request, "users/index.html", {
            "products" : zip(products,paths),
            # "images" : path_image,
            })

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

def image(request):
    image_file = request.FILES['image_file'].file.read()
    MyModel.objects.create(image=image_file)

def add(request):
    return render(request, "Thamahakinview/add.html")

def add_product(request):
    if request.method == 'POST':
            product =  request.POST["product"]
            price = request.POST["price"]
            cat = request.POST["type"]
            detail = request.POST["detail"]
            line = request.POST["line"]
            instagram = request.POST["instagram"]
            facebook = request.POST["facebook"]
            tel = request.POST["tel"]
            fileToUpload = request.FILES["fileToUpload"]
            path = default_storage.save(
                f"/home/ubuntu/THAMMAHAKIN/thammahakin/users/templates/temporaryfile/{fileToUpload.name}",
                ContentFile(fileToUpload.read()))
            typefile = fileToUpload.name
            typefile = typefile[(typefile.rfind('.')+1):len(typefile)]
            mime_type = 'image/jpeg'
            file_medate = {
                'name': fileToUpload.name,
                'parents':  [floder_id]
            }
            media = MediaFileUpload(path, mimetype = mime_type)
            results = service.files().create(
                body=file_medate,
                media_body=media,
                fields='id'
                ).execute()
            items = results.get('id')
            os.remove(path)
            Thammart.objects.create(t_user=request.user.username,t_name=product,t_detail=detail,t_cat=cat,t_count=0,t_price=price,t_image=items)
            products = Thammart.objects.all()
            paths = []
            for product in products :
                paths.append(f'https://drive.google.com/uc?id={product.t_image}')
            return render(request, "users/index.html", {
            "products" : zip(products,paths),
            })