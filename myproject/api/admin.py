from django.contrib import admin
from .apimodules.UserProfile import UserProfile
from .models import CustomUser
from .apimodules.Room import *


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CustomUser)
admin.site.register(Room)
admin.site.register(Message)