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

# Connect google drive api

from Google import Create_Service
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPE = ['https://www.googleapis.com/auth/drive']

floder_id = '18SCTkSPkw6Kiba2wgXkRfbd1mWnhIOTx'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPE)

# Path for temporaryfile image
PATH_IMAGE = os.path.join(os.path.normpath(os.getcwd() + os.sep + os.pardir), 'thammahakin/users/templates/temporaryfile')
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
        password = request.POST["password"]
        c_password = request.POST["cpassword"]
        if user_id and name and sname and password and c_password :
            if user_id.isnumeric() :
                user = Profile.objects.filter(p_user=user_id)
                # print(user)
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
                if 'intro' in request.POST: products = Thammart.objects.all()
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
                "products" : list(zip(favorite.p_fav.all(),image(favorite.p_fav.all()))),
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
    items = []
    for file in request.FILES.getlist('fileToUpload'):
        path = default_storage.save(
                os.path.join(PATH_IMAGE,file.name),
                ContentFile(file.read()))
        typefile = file.name
        typefile = typefile[(typefile.rfind('.')+1):len(typefile)]
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
                    Thammart.objects.create(t_user=request.user,t_name=product,t_detail=detail,t_cat=cat,t_count=0,t_price=price,t_image=items,t_channel=t_channel)
                    product_new = Thammart.objects.get(t_user=request.user,t_name=product,t_detail=detail,t_cat=cat,t_price=price,t_image=items,t_channel=t_channel)
                    # print(product_new)
                    products = Thammart.objects.all()
                    return render(request, "users/index.html", {
                    "products" : list(zip(products,image(products))),
                    })
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
                    imagea = imagea.replace("[","")
                    imagea = imagea.replace("]","")
                    imagea = imagea.replace("'","")
                    imagea = imagea.replace(",","")
                    if imagea == '1vqC3XJu47ia2WfbxYjH-ob7eNzq8mmsS':
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
                image = image.replace("[","")
                image = image.replace("]","")
                image = image.replace("'","")
                image = image.replace(",","")
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
                    image = image.replace("[","")
                    image = image.replace("]","")
                    image = image.replace("'","")
                    image = image.replace(",","")
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
                message = "Edit SuccessFul"
                product.save()
                product = Thammart.objects.get(id=request.POST["edit"])
                images = product.t_image.split()
                pathgoogle = []
                preitems = []
                items = []
                for image in images:
                    image = image.replace("[","")
                    image = image.replace("]","")
                    image = image.replace("'","")
                    image = image.replace(",","")
                    preitems.append(image)
                if request.POST.get('imageToDelete', False):
                    print('imageToDelete')
                    imageToDelete = request.POST.getlist('imageToDelete')
                    for image in imageToDelete:
                        service.files().delete(fileId=image).execute()
                        if image in preitems:
                            preitems.remove(image)
                    for image in preitems:
                        items.append(image)
                        pathgoogle.append(f'https://drive.google.com/uc?id={image}')
                else:
                    print('else imageToDelete')
                    for image in preitems:
                        items.append(image)
                        pathgoogle.append(f'https://drive.google.com/uc?id={image}')
                if request.POST.get('fileToUpload', True):
                    fileToUpload = request.FILES["fileToUpload"]
                    itemUpload = uploadImage(request, fileToUpload)
                    for itemUp in itemUpload:
                        items.append(itemUp)
                        pathgoogle.append(f'https://drive.google.com/uc?id={itemUp}')
                print(items)
                if items == []:
                    product.t_image = '1vqC3XJu47ia2WfbxYjH-ob7eNzq8mmsS'
                else:
                    if '1vqC3XJu47ia2WfbxYjH-ob7eNzq8mmsS' in items:
                        items.remove('1vqC3XJu47ia2WfbxYjH-ob7eNzq8mmsS')
                        pathgoogle.remove('https://drive.google.com/uc?id=1vqC3XJu47ia2WfbxYjH-ob7eNzq8mmsS')
                    product.t_image = items
                product.save()
                return render(request, "Thamahakinview/detail.html",{
                    "product" : product,
                    "images" : pathgoogle,
                    "messages" : message,
                })
        else :
            return HttpResponseRedirect(reverse("logout"))

# def edit_profile_view(request):
#     return render(request, "users/edit_profile.html")

# def edit_profile(request):
#     return render(request, "users/edit_rpofile.html")