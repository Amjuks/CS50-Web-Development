from django.contrib.auth.models import AbstractUser
from django.db import models
from colorfield.fields import ColorField


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=32)
    color = models.SmallIntegerField(default=0x000000)   

    def __str__(self) -> str:
        return f'{self.name} - ID: {self.id}'


class Listings(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    starting_price = models.PositiveIntegerField()
    highest_bid = models.PositiveIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.URLField(blank=True, null=True)
    open = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    users_wishlist = models.ManyToManyField(User, related_name="wishlist_items", blank=True)

    def get_highest_bid(self):
         return self.bids.order_by('-amount').first()

    def __str__(self) -> str:
        open = 'Open' if self.open else 'Closed'

        if self.highest_bid:
            bid = f'Highest bid: ${self.highest_bid}'
        else:
            bid = f'Starting price: ${self.starting_price}'

        return f'{self.id}. {self.title}: {bid} [{open}]'


class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name='bids')
    amount = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} bid ${self.amount} on "{self.listing}"'
    

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} {self.listing}: {self.content}'
    

# class Wishlist(models.Model):
#     user = models.ManyToManyField(User, related_name="user_wishlist")
#     listing = models.ForeignKey(Listings, on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return f'{self.user}: {self.listing}'