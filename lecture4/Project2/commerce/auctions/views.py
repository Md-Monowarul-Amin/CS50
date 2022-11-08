from datetime import datetime
from doctest import debug_script
from email.mime import image
from pydoc import describe
from re import A, I
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import is_valid_path, reverse
from django import forms

import auctions


from .models import *

class NewAuctionForm(forms.Form):
    title = forms.CharField(label="title", max_length=64)
    description = forms.CharField(widget=forms.Textarea)
    starting_bid = forms.IntegerField(label="starting_bid")
    image = forms.URLField(label="image Url")
    # category = forms.Select(choices=Category.objects.all())
    # category = forms.Select(attrs={'class': 'form-control'})

def index(request):
    auctions = AuctionListing.objects.all()
    return render(request, "auctions/index.html",{"auctions":auctions})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def create_auction(request):
    if request.method == "POST":
        form = NewAuctionForm(request.POST)
        if form.is_valid():
            print("IS valid")
            title = form.cleaned_data['title']
            category_ = Category.objects.get(pk = request.POST["category"])
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            print(image)
            created_by = request.user
            creation_time = datetime.now()
            starting_bid = (form.cleaned_data['starting_bid'])
            AuctionListing.objects.create(title=title, description= description, starting_bid= starting_bid, 
            image = image,category = category_, created_by= created_by, creation_time= creation_time, current_bid = starting_bid)
            
            print(starting_bid)
            return HttpResponseRedirect(reverse("index"))

        else:
            print("NOT VALID") 
        user = request.user
        # print(category, title)
       
    user = request.user
    category = Category.objects.all()
    create_auction_form = NewAuctionForm()
    return render(request, "auctions/create_auction.html",{"form": create_auction_form, "categories":category}) 


def listing(request, listing_id):
    auction_listing = AuctionListing.objects.get(pk= listing_id)
    return render(request, "auctions/listing.html", {"listing": auction_listing})
