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
from django.utils import timezone
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
            if 'intro' in request.POST: products = Thammart.objects.all()
            elif 'food' in request.POST: products = Thammart.objects.filter(t_cat='food')
            elif 'closet' in request.POST: products = Thammart.objects.filter(t_cat='closet')
            elif 'accessary' in request.POST: products = Thammart.objects.filter(t_cat='accessary')
            elif 'beauty' in request.POST: products = Thammart.objects.filter(t_cat='beauty')
            elif 'electronic' in request.POST: products = Thammart.objects.filter(t_cat='electronic')
            elif 'others' in request.POST: products = Thammart.objects.filter(t_cat='others')
        return render(request, "users/index.html", {
        "products" : zip(products,image(products)),
        })

def image(products) :
    paths = []
    for product in products :
        images = product.t_image.split()
        path = []
        for image in images:
            image = image.replace("[","")
            image = image.replace("]","")
            image = image.replace("'","")
            image = image.replace(",","")
            path.append(f'https://drive.google.com/uc?id={image}')
        paths.append(path)
    return paths

def login_view(request):
    if request.user.is_authenticated :
        if not request.user.is_staff :
            print("in")
            return HttpResponseRedirect(reverse("index"))
        else :
            return render(request, "users/login.html", {
                "message": "admin cannot login like user."
            })
    if request.method == "POST" :
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request , user)
            if not user.is_staff :
                return HttpResponseRedirect(reverse("index"))
            else :
                return HttpResponseRedirect(reverse("logout"))
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

def about_view(request):
    return render(request, "users/about.html")

def add_view(request):
    return render(request, "Thamahakinview/add.html")

def add_product(request):
    profile = Profile.objects.get(p_user=request.user)
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
        mime_type = ''
        items = []
        for file in request.FILES.getlist('fileToUpload'):
            path = default_storage.save(
                f"/home/ubuntu/THAMMAHAKIN/thammahakin/users/templates/temporaryfile/{file.name}",
                ContentFile(fileToUpload.read()))
            typefile = file.name
            typefile = typefile[(typefile.rfind('.')+1):len(typefile)]
            # if typefile not 'png' and not 'jpg' and not 'jpeg':
            #     return
            file_medate = {
                'name': file.name,
                'parents':  [floder_id]
            }
            if(typefile == 'png'):
                mime_type = 'image/png'
            elif(typefile == 'jpg' or 'jpeg'):
                mime_type = 'image/jpeg'
            media = MediaFileUpload(path, mimetype = mime_type)
            results = service.files().create(
                body=file_medate,
                media_body=media,
                fields='id'
                ).execute()
            item = results.get('id')
            items.append(item)
            print(items)
            os.remove(path)
        Thammart.objects.create(t_user=request.user,t_name=product,t_detail=detail,t_cat=cat,t_count=0,t_price=price,t_image=items)
        product_new = Thammart.objects.get(t_user=request.user,t_name=product,t_detail=detail,t_cat=cat,t_price=price,t_image=items)
        print(product_new)
        products = Thammart.objects.all()
        return render(request, "users/index.html", {
        "products" : zip(products,image(products)),
        })

def remove_product(request):
    profile = Profile.objects.get(p_user=request.user)
    if request.method == "POST" :
        r_product = request.POST["remove"]
        product = Thammart.objects.filter(t_detail=r_product)
        product.delete()
        products = Thammart.objects.filter(t_user=request.user)
    return render(request, "Thamahakinview/thammart.html",{
        "message" : "Successful Remove Product.",
        "mymart" : zip(products,image(products)),
    })

def thammart(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if not request.user.is_staff :
            products = Thammart.objects.filter(t_user=request.user)
            return render(request, "Thamahakinview/thammart.html", {
                "mymart" : zip(products,image(products)),
            })

def detail(request):
    if request.method == "POST" :
        d_product = request.POST["detail"]
        print(d_product)
        product = Thammart.objects.get(t_detail=d_product)
        images = product.t_image.split()
        path = []
        for image in images:
            image = image.replace("[","")
            image = image.replace("]","")
            image = image.replace("'","")
            image = image.replace(",","")
            path.append(f'https://drive.google.com/uc?id={image}')
        return render(request, "Thamahakinview/detail.html",{
            "product" : product,
            "images" : path,
        })


