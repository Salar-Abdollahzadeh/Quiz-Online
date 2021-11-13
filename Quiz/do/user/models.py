from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Address(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)