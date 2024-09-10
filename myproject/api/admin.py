from django.contrib import admin
from .apimodules.UserProfile import UserProfile
from .models import CustomUser
from .apimodules.Room import *


# Register your models here.
admin.site.register(UserProfile)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomUser._meta.fields]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Room._meta.fields]
    search_fields = ['room_name']

admin.site.register(Message)