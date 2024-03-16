from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=32)
    initial_bid = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    image = models.URLField()
    open = models.BooleanField(default=True)

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)


class Categories(models.Model):
    category = models.CharField(max_length=32)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)