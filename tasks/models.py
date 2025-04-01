from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from authentication.models import AppUser

class Task(models.Model):
    title = models.CharField(blank=False, max_length=32)
    description = models.TextField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(AppUser, related_name='tasks', on_delete=models.CASCADE, default=1)