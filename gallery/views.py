from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
from PIL import Image,ImageEnhance
from PIL import ImageFilter


from PIL.ImageFilter import (
    RankFilter, MedianFilter, MinFilter, MaxFilter
    )
from .models import User,Images,Category,Profile,Likes,Collection


# Create your views here.

def index(request):
    instance1=Images.objects.all()
    instance1=instance1.order_by('-datetime').all()
    instance2=Category.objects.all()
    
    if request.user.is_authenticated:
        lists=[]
        my_likes=Likes.objects.filter(user=request.user)
        for posts in my_likes:
            lists.append(posts.image.id)
    else:
        lists=[]
   
    return render(request,"gallery/index.html",{
        "Image":instance1,"Category":instance2,"lists":lists
        })
	
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "gallery/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "gallery/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST["email"]
        pic=request.FILES["profile"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "gallery/login.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            
        except IntegrityError:
            return render(request, "gallery/login.html", {
                "message": "Username already taken."
            })
        login(request, user)
        instance=Profile(photo_of=user,pic=pic)
        instance.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "gallery/login.html")	

def Form_page(request):
	return render(request,"gallery/form.html")


def Form(request):
	if request.method=="POST":
		title=request.POST["title"]
		image=request.FILES["image"]
		date=datetime.datetime.now()
		user=request.user
		description=request.POST["description"]
		instance=Images(user=user,title=title,image=image,description=description,datetime=date)
		instance.save()
		category=request.POST.getlist("checks[]")
		for c in category:
			instance2=Category(image=instance,category=c)
			instance2.save()
		return HttpResponseRedirect(reverse("index"))
	
def Search(request):
    if request.method=="POST":
        to_search=request.POST["search"]
        result=Category.objects.filter(category__contains=to_search)
        likes=[]
        my_likes=Likes.objects.filter(user=request.user)
        for posts in my_likes:
                likes.append(posts.image.id)
        return render(request,"gallery/search_result.html",{
            "result":result,"lists":likes
            })
def api(request):
    return render(request,"gallery/Api.html")

def profile_pic(request,user_id):
    instance=User.objects.get(pk=user_id)
    image=Profile.objects.get(photo_of=instance)
    return HttpResponse(image.pic.url)

def add_like(request,image_id):
    my_user=request.user
    image=Images.objects.get(pk=image_id)
    check=Likes.objects.filter(image=image).filter(user=my_user).first()
    if check is None:
        instance=Likes(image=image,user=my_user)
        instance.save()
        return HttpResponse("liked")
    else:
        check.delete()
        return HttpResponse("dislike")

def collection(request):
    user=request.user
    items=user.my_collection.all()
    likes=[]
    my_likes=Likes.objects.filter(user=request.user)
    for posts in my_likes:
            likes.append(posts.image.id)
    my_list=[]
    for item in items:
        my_list.append(item.collected_images)
    return render(request,"gallery/collection.html",{
        "Image":my_list,"lists":likes
        })

def add_collection(request,image_id):
    user=request.user
    item=Images.objects.get(pk=image_id)
    check=user.my_collection.all()
    for i in check:
        if image_id==i.collected_images.id:
            return HttpResponse("already in list")
    instance=Collection(collection_of=user,collected_images=item)
    instance.save()
    return HttpResponse("added")

def remove_collection(request,image_id):
    item=Images.objects.get(pk=image_id)
    Collection.objects.filter(collection_of=request.user).filter(collected_images=item).delete()
    return HttpResponseRedirect(reverse("collection"))

def edit_flip(request,image_id):
    item=Images.objects.get(pk=image_id)
    image_url=item.image.url
    sliced=image_url[6:]
    image=Image.open(image_url) 
    filpped_vertical=image.transpose(Image.FLIP_LEFT_RIGHT).save("media/transpose_"+sliced)
    return HttpResponse("/media/transpose_"+sliced)

def edit_contrast(request,image_id):
    item=Images.objects.get(pk=image_id)
    image_url=item.image.url
    sliced=image_url[6:]
    image=Image.open(image_url) 
    en=ImageEnhance.Contrast(image)
    img2=en.enhance(1.5)
    img2.save("media/contrast_"+sliced)
    return HttpResponse("/media/contrast_"+sliced)

def edit_bw(request,image_id):
    item=Images.objects.get(pk=image_id)
    image_url=item.image.url
    sliced=image_url[6:]
    image=Image.open(image_url) 
    en=ImageEnhance.Color(image)
    img2=en.enhance(0.0)
    img2.save("media/bw_"+sliced)
    return HttpResponse("/media/bw_"+sliced)

        
def edit_median(request,image_id):
    item=Images.objects.get(pk=image_id)
    image_url=item.image.url
    sliced=image_url[6:]
    image=Image.open(image_url) 
    img2 = image.filter(MedianFilter(size=9))
    img2.save("media/median_"+sliced)
    return HttpResponse("/media/median_"+sliced)
