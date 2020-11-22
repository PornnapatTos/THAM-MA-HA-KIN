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
import ast
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json
from random import randint
# Connect google drive api

from Google import Create_Service
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPE = ['https://www.googleapis.com/auth/drive']

floder_id = '18SCTkSPkw6Kiba2wgXkRfbd1mWnhIOTx'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPE)

# Path for temporaryfile image
PATH_IMAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/temporaryfile')
print(PATH_IMAGE)
# Create your views here.

def register_view(request):
    if not request.user.is_authenticated :
        return render(request, "users/register.html")
    else :
        return HttpResponseRedirect(reverse("index"))

def add_user(request) :
    if request.method == "POST" :
        user_id =  request.POST["username"]
        name = request.POST["name"]
        sname = request.POST["sname"]
        mail = request.POST["mail"]
        password = request.POST["password"]
        c_password = request.POST["cpassword"]
        if user_id and name and sname and password and c_password :
            if user_id.isnumeric() :
                user = Profile.objects.filter(p_user=user_id)
                # print(user)
                if not user:
                    if password == c_password :
                        User.objects.create_user(username=user_id, password=password,)
                        Profile.objects.create(p_user=user_id,p_name=name,p_sname=sname,p_mail=mail)
                        return render(request, "users/login.html", {
                            "message": "register success!"
                        })
                    else :
                        return render(request, "users/register.html", {
                            "message": "fail to register!"
                        })
                else :
                    return render(request, "users/login.html", {
                            "message": "you are already in website!"
                        })
            else :
                return render(request, "users/register.html", {
                    "message": "fail to register!"
                })

        else :
            return render(request, "users/register.html", {
                        "message": "Please complete this registration form."
                    })

def index(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if not request.user.is_staff :
            products = Thammart.objects.all()
            if request.method == "POST" :
                if 'intro' in request.POST: products = Thammart.objects.order_by('t_count').reverse()[:10]
                elif 'food' in request.POST: products = Thammart.objects.filter(t_cat='food')
                elif 'closet' in request.POST: products = Thammart.objects.filter(t_cat='closet')
                elif 'accessary' in request.POST: products = Thammart.objects.filter(t_cat='accessary')
                elif 'beauty' in request.POST: products = Thammart.objects.filter(t_cat='beauty')
                elif 'electronic' in request.POST: products = Thammart.objects.filter(t_cat='electronic')
                elif 'others' in request.POST: products = Thammart.objects.filter(t_cat='others')
            return render(request, "users/index.html", {
                "products" : list(zip(products,image(products))),
            })
        else :
            return HttpResponseRedirect(reverse("logout"))

def image(products) :
    paths = []
    for product in products :
        images = product.t_image.split()
        path = []
        for image in images:
            path.append(f'https://drive.google.com/uc?id={image}')
        paths.append(path)
    return paths

def login_view(request):
    if request.user.is_authenticated :
        if not request.user.is_staff :
            print("in")
            return HttpResponseRedirect(reverse("index"))
        else :
            return HttpResponseRedirect(reverse("logout"))
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
    return HttpResponseRedirect(reverse("login"))

def favorite_view(request):
    if request.user.is_authenticated :
        if not request.user.is_staff :
            favorite = Profile.objects.get(p_user = request.user.username)
            # print(favorite.p_fav.all())
            return  render(request, "Thamahakinview/favo.html", {
                "favos": list(zip(favorite.p_fav.all(),image(favorite.p_fav.all()))),
            })
        else :
            return HttpResponseRedirect(reverse("logout"))
    else :
        return HttpResponseRedirect(reverse("login"))
@csrf_exempt
def add_favorite(request):
    if request.user.is_authenticated :
        if not request.user.is_staff :
            if request.method == "POST" :
                profile = Profile.objects.get(p_user = request.user.username)
                product = Thammart.objects.get(id=request.POST["fav"])
                if product not in profile.p_fav.all() :
                    profile.p_fav.add(product)
                    product.t_count += 1
                    product.save()
                    # Thammart.objects.get(id=request.POST["fav"]).update(t_count=(product.t_count+1))
                    message = "Successful Add Favorite Product."
                else :
                    message = "Product has already in Your Favorite."
            products = Thammart.objects.all()
            return render(request, "users/index.html", {
                "products" : list(zip(products,image(products))),
                "messages" : message,
            })
            # return HttpResponse(message)
        else :
            return HttpResponseRedirect(reverse("logout"))
    else :
        return HttpResponseRedirect(reverse("login"))

def remove_favorite(request):
    if request.user.is_authenticated :
        if not request.user.is_staff :
            if request.method == "POST" :
                profile = Profile.objects.get(p_user = request.user.username)
                product = Thammart.objects.get(id=request.POST["remove_favo"])
                if product in profile.p_fav.all() :
                    profile.p_fav.remove(product)
                    message = "Successful Remove Favorite Product."
                    product.t_count -= 1
                    product.save()
                    # Thammart.objects.get(id=request.POST["remove_favo"]).update(t_count=(product.t_count-1))
                else :
                    message = "Product has not already in Your Favorite."
            favorite = Profile.objects.get(p_user = request.user.username)
            return render(request, "Thamahakinview/favo.html", {
                "favos" : list(zip(favorite.p_fav.all(),image(favorite.p_fav.all()))),
                "messages" : message,
            })
        else :
            return HttpResponseRedirect(reverse("logout"))
    else :
        return HttpResponseRedirect(reverse("login"))

def about_view(request):
    if request.user.is_authenticated :
        if not request.user.is_staff :
            return render(request, "users/about.html")
        else :
            return HttpResponseRedirect(reverse("logout"))
    else :
        return HttpResponseRedirect(reverse("login"))

def add_view(request):
    if request.user.is_authenticated :
        if not request.user.is_staff :
            return render(request, "Thamahakinview/add.html")
        else :
            return HttpResponseRedirect(reverse("logout"))
    else :
        return HttpResponseRedirect(reverse("login"))

def uploadImage(request, fileToUpload):
    mime_type = ''
    items = ''
    for file in request.FILES.getlist('fileToUpload'):
        typefile = file.name
        typefile = typefile[(typefile.rfind('.')+1):len(typefile)]
        file_medate = {
            'name': file.name,
            'parents':  [floder_id]
        }
        if(typefile == 'png'):
            mime_type = 'image/png'
        elif(typefile == 'jpg' or typefile == 'jpeg'):
            mime_type = 'image/jpeg'
        else:
            return False
        path = default_storage.save(
                os.path.join(PATH_IMAGE,file.name),
                ContentFile(file.read()))
        media = MediaFileUpload(path, mimetype = mime_type)
        results = service.files().create(
            body=file_medate,
            media_body=media,
            fields='id'
            ).execute()
        item = results.get('id')
        items += item + ' '
        os.remove(path)
    return items

def add_product(request):
    if request.user.is_authenticated :
        if not request.user.is_staff :
            profile = Profile.objects.get(p_user=request.user)
            if request.method == 'POST':
                error = {}
                if request.POST.get('product', False):
                    product =  request.POST["product"]
                else:
                    error['product'] = 'Product is required'
                if request.POST.get('price', False):
                    price = request.POST["price"]
                else:
                    error['price'] = 'Price is required'
                if request.POST.get('type', False):
                    cat = request.POST["type"]
                else:
                    error['category'] = 'category is required'
                if request.POST.get('detail', False):
                    detail = request.POST["detail"]
                else:
                    error['detail'] = 'Detail is required'
                tel = request.POST["tel"]
                t_channel = [request.POST["line"],request.POST["instagram"],request.POST["facebook"],tel]
                if request.POST.get('fileToUpload', True):
                    fileToUpload = request.FILES["fileToUpload"]
                    items = uploadImage(request, fileToUpload)
                    if items == False:
                        error['image'] = 'Type files only .png and .jpg/.jpge'
                        return render(request, "Thamahakinview/add.html",{
                            "error": error
                        })
                    else:
                        Thammart.objects.create(t_user=request.user,t_name=product,t_detail=detail,t_cat=cat,t_count=0,t_price=price,t_image=items,t_channel=t_channel)
                    # products = Thammart.objects.all()
                    # return render(request, "users/index.html", {
                    # "products" : list(zip(products,image(products))),
                    # })
                    return HttpResponseRedirect(reverse("thammart"))
                else:
                    error['image'] = 'At least 1 sample image is required.'
                if error:
                    return render(request, "Thamahakinview/add.html",{
                        "error": error
                    })
        else :
            return HttpResponseRedirect(reverse("logout"))
    else :
        return HttpResponseRedirect(reverse("login"))

def remove_product(request):
    if request.user.is_authenticated :
        if not request.user.is_staff :
            profile = Profile.objects.get(p_user=request.user)
            if request.method == "POST" :
                r_product = request.POST["remove"]
                product = Thammart.objects.get(id=r_product)
                productIm = Thammart.objects.get(id=r_product)
                imagess = productIm.t_image.split()
                for imagea in imagess:
                    if imagea == '1jOY4xYqxS26Yu4RX9FANs46PZOcpCkZ8':
                        pass
                    else:
                        service.files().delete(fileId=imagea).execute()
                product.delete()
                products = Thammart.objects.filter(t_user=request.user)
            return render(request, "Thamahakinview/thammart.html",{
                "messages" : "Successful Remove Product.",
                "mymart" : list(zip(products,image(products))),
            })
        else :
            return HttpResponseRedirect(reverse("logout"))
    else :
        return HttpResponseRedirect(reverse("login"))

def thammart(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if not request.user.is_staff :
            products = Thammart.objects.filter(t_user=request.user)
            return render(request, "Thamahakinview/thammart.html", {
                "mymart" : list(zip(products,image(products))),
            })
        else :
            return HttpResponseRedirect(reverse("logout"))

def detail(request,product_id):
    print(product_id)
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if not request.user.is_staff :
            product = Thammart.objects.get(id=product_id)
            images = product.t_image.split()
            path = []
            for image in images:
                path.append(f'https://drive.google.com/uc?id={image}')
            channel = ["Line","Instagram","facebook","Phone Number"]
            return render(request, "Thamahakinview/detail.html",{
                "product" : product,
                "images" : path,
                "channels" : list(zip(channel,ast.literal_eval(product.t_channel))),
            })
        else :
            return HttpResponseRedirect(reverse("logout"))

def edit(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if request.method == "POST" :
            if not request.user.is_staff :
                d_product = request.POST["edit"]
                product = Thammart.objects.get(id=d_product)
                images = product.t_image.split()
                path = []
                key=[]
                for image in images:
                    key.append(image)
                    path.append(f'https://drive.google.com/uc?id={image}')
                channel = ["Line","Instagram","facebook","Phone Number"]
                return render(request,"Thamahakinview/edit.html",{
                    "product" : product,
                    "images" : list(zip(path,key)),
                    "channels" : list(zip(channel,ast.literal_eval(product.t_channel))),
                })
            else :
                return HttpResponseRedirect(reverse("logout"))

def search(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if not request.user.is_staff :
            if request.method == "POST" :
                product = request.POST["product"]
                print(product)
                products = Thammart.objects.filter(t_name__contains=product)
                return render(request, "users/index.html", {
                    "products" : list(zip(products,image(products))),
                })
        else :
            return HttpResponseRedirect(reverse("logout"))

def edit_product(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if not request.user.is_staff :
            if request.method == "POST" :
                product = Thammart.objects.get(id=request.POST["edit"])
                product.t_name = request.POST["name"]
                product.t_detail = request.POST["detail"]
                product.t_cat = request.POST["type"]
                product.t_price = request.POST["price"]
                message = "Edit SuccessFul."
                product.save()
                product = Thammart.objects.get(id=request.POST["edit"])
                images = product.t_image.split()
                pathgoogle = []
                preitems = []
                items = ''
                for image in images:
                    preitems.append(image)
                if request.POST.get('imageToDelete', False):
                    print('imageToDelete')
                    imageToDelete = request.POST.getlist('imageToDelete')
                    for image in imageToDelete:
                        if image == '1jOY4xYqxS26Yu4RX9FANs46PZOcpCkZ8':
                            pass
                        else:
                            service.files().delete(fileId=image).execute()
                        if image in preitems:
                            preitems.remove(image)
                    for image in preitems:
                        items.append(image)
                        pathgoogle.append(f'https://drive.google.com/uc?id={image}')
                else:
                    print('else imageToDelete')
                    for image in preitems:
                        items += image + ' '
                        pathgoogle.append(f'https://drive.google.com/uc?id={image}')
                if request.POST.get('fileToUpload', True):
                    fileToUpload = request.FILES["fileToUpload"]
                    itemUpload = uploadImage(request, fileToUpload)
                    if itemUpload == False:
                        channel = ["Line","Instagram","facebook","Phone Number"]
                        return render(request,"Thamahakinview/edit.html",{
                            "product" : product,
                            "images" : list(zip(pathgoogle,preitems)),
                            "channels" : list(zip(channel,ast.literal_eval(product.t_channel))),
                            "message" : "upload only .phr and .jpg/.jpge"
                        })
                    itemUpload = itemUpload.split()
                    for itemUp in itemUpload:
                        items += itemUp + ' '
                        pathgoogle.append(f'https://drive.google.com/uc?id={itemUp}')
                if items == '':
                    product.t_image = '1jOY4xYqxS26Yu4RX9FANs46PZOcpCkZ8'
                    pathgoogle.append('https://drive.google.com/uc?id=1jOY4xYqxS26Yu4RX9FANs46PZOcpCkZ8')
                else:
                    check = items.find('1jOY4xYqxS26Yu4RX9FANs46PZOcpCkZ8')
                    if check == '-1':
                        items.replace('1jOY4xYqxS26Yu4RX9FANs46PZOcpCkZ8', '')
                        pathgoogle.remove('https://drive.google.com/uc?id=1jOY4xYqxS26Yu4RX9FANs46PZOcpCkZ8')
                    product.t_image = items
                product.save()
                return render(request, "Thamahakinview/detail.html",{
                    "product" : product,
                    "images" : pathgoogle,
                    "messages" : message,
                })
        else :
            return HttpResponseRedirect(reverse("logout"))

def forgot_view(request):
    if not request.user.is_authenticated :
        return render(request, "users/forgot_password.html")
    else :
        if not request.user.is_staff :
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("logout"))

def forgot(request):
    if not request.user.is_authenticated :
            if request.method == "POST" :
                mail = request.POST["email"]
                profile = Profile.objects.filter(p_mail=mail)
                # print(profile)
                if not profile :
                    # print("hello")
                    return render(request, 'users/forgot_password.html',{
                        "messages" : "Wrong E-mail",
                    })
                else :
                    profile = Profile.objects.get(p_mail=mail)
                    digit = randint(100000, 999999)
                    # print(digit)
                    # send_mail(
                    #     'Change Password',
                    #     str(digit),
                    #     'pornnapat.tos@gmail.com',
                    #     [profile.p_mail],
                    #     fail_silently=False,
                    # )
                    return render(request, "users/reset_password.html",{
                        "user" : profile.p_mail,
                        "digit" : digit,
                    })
    else :
        if not request.user.is_staff :
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("logout"))

def reset_view(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if not request.user.is_staff :
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("logout"))

def reset(request):
    if not request.user.is_authenticated :
        if request.method == "POST" :
            n_password = request.POST["n_password"]
            nc_password = request.POST["nc_password"]
            profile = Profile.objects.get(p_mail=request.POST["user"])
            if n_password==nc_password :
                user = User.objects.get(username=profile.p_user)
                # print(user)
                user.set_password(n_password)
                user.save()
                return render(request, "users/login.html", {
                        "message": "Change Password Success!"
                    })
            else :
                return render(request, "users/reset_password.html", {
                        "message": "Change Password fail!",
                        "user" : profile.p_mail,
                    })
    else :
        if not request.user.is_staff :
            return HttpResponseRedirect(reverse("index"))
        else :
            return HttpResponseRedirect(reverse("logout"))

# def verify(request):
#     if not request.user.is_authenticated :
#         if request.method == "POST" :
#             email = request.POST["email"]
#             verify = request.POST["verify"]
#             digit = request.POST["digit"]
#             profile = Profile.objects.get(p_mail=request.POST["email"])
#             if verify == digit :
#                 return render(request, "users/reset_password.html",{
#                     "user" : profile.p_mail,
#                 })
#             else :
#                 return render(request, "users/check_verify.html",{
#                         "user" : profile.p_mail,
#                         "digit" : digit,
#                         "messages" : "Wrong Verify",
#                     })
#     else :
#         if not request.user.is_staff :
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             return HttpResponseRedirect(reverse("logout"))