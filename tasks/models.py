from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser

class Task(models.Model):
    title = models.CharField(blank=False, max_length=32)
    description = models.TextField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

class AppUser(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_login = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=255, null=True)

    USERNAME_FIELD = 'email'