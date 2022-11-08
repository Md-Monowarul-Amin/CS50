from datetime import datetime
from email.policy import default

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)



class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description= models.CharField(max_length=64)
    starting_bid = models.IntegerField()
    image = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name="listings")
    creation_time = models.DateField(default=datetime.now)
    watchers = models.ManyToManyField(User, blank=True, related_name= "watchlist")
    current_bid = models.IntegerField(default=starting_bid)

    def __str__(self) -> str:
        return self.title




class Bid(models.Model):
    bid_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid_price = models.IntegerField()
    bid_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.bid_owner.name}: {self.bid_price}"


class Comment(models.Model):
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    
    def __str__(self) -> str:
        return {self.comment}


