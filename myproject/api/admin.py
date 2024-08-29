from django.contrib import admin
from .apimodules.UserProfile import UserProfile
from .models import CustomUser


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CustomUser)