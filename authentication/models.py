from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

class AppUser(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True)
    last_login = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=255, null=True)
    expires_in = models.DateTimeField(default=timezone.now)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
