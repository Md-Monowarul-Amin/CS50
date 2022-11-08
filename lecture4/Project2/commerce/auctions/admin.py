from django.contrib import admin
from .models import AuctionListing, Category, User, Bid, Comment, ModifiedAuctionListing
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(ModifiedAuctionListing)


