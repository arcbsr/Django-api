from django.db import models
from sqlalchemy import false
from api.models import CustomUser


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

def __str__(self):
        return self.user.username