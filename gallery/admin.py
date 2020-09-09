from django.contrib import admin
from .models import User,Images,Category,Profile,Likes,Collection

# Register your models here.
admin.site.register(User)
admin.site.register(Images)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Likes)
admin.site.register(Collection)
