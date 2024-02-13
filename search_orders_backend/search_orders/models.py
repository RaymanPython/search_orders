from django.db import models
from django.contrib.auth.models import User
from ninja import Router


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

class Order(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)