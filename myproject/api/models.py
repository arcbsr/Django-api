 

# Create your models here.
# api/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from .apimodules import * 

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'User'),
    )
    ACTIVE_CHOICES = (
        ('active', 'Active'),
        ('deactive', 'Deactive'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    status = models.CharField(max_length=10, choices=ACTIVE_CHOICES, default='active')

    def __str__(self):
        return self.username
