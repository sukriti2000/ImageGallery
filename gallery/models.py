from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill,SmartResize


class User(AbstractUser):
    pass

class Images(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_images",default="")
	title=models.CharField(max_length=100,default="")
	image=models.FileField(default="")
	description=models.CharField(max_length=200)
	datetime=models.DateTimeField(default="") 

	large=ImageSpecField(
		source='image' , processors=[ResizeToFill(1920,1309)],format='PNG')
    
	thumbnail=ImageSpecField(
		source='image' , processors=[ResizeToFill(1280,873)],format='PNG')
	
	smart=ImageSpecField(
		source='image' , processors=[SmartResize(640,436)],format='PNG')

class Category(models.Model):
	image=models.ForeignKey(Images,on_delete=models.CASCADE,related_name="image_category",default="")
	category=models.CharField(max_length=100)

class Likes(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="liked_by",default="")
	image=models.ForeignKey(Images,on_delete=models.CASCADE,related_name="liked_image",default="")

class Profile(models.Model):
	photo_of=models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_pic",default="")
	pic=models.FileField(default="")

class Collection(models.Model):
	collection_of=models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_collection",default="")
	collected_images=models.ForeignKey(Images,on_delete=models.CASCADE,related_name="image_Collected",default="")

