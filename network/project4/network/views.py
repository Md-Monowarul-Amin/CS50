from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.exceptions import ObjectDoesNotExist


from .models import *


class NewPostForm(forms.Form):
    post_text = forms.CharField(max_length=10000)


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def all_posts(request):
    posts = Post.objects.all()
    current_user = request.user
    form = NewPostForm()
    return render(request, "network/AllPost.html", {"posts": posts, "current_user": current_user, "form": form})


def add_post(request):
    print("inside add posst")
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            print("valid")
            post_text = form.cleaned_data['post_text']
            posted_by = request.user

            Post.objects.create(user = posted_by, post_text = post_text)
            print(post_text)
            return render(request, "network/index.html")

        else:
            print("error")

        
def increase_like(request, post_id):
    # print("increase_like")
    catched_post = Post.objects.get(pk = post_id)
    user = request.user
    try:
        likes.objects.get(user=user, post = catched_post)
        catched_post.like_count -= 1
        catched_post.save()
        likes.objects.get(user = user, post = catched_post).delete()
        # print(likes.objects.all())
    except ObjectDoesNotExist:
        likes.objects.create(user=user, post=catched_post)
        catched_post.like_count += 1
        catched_post.save()
    
    print(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect((request.META.get('HTTP_REFERER')))



def count_follower(user_id):
    user = User.objects.get(pk= user_id)
    folllowers = Follow.objects.filter(followed_person = user)
    return len(folllowers)
    

def count_following(user_id):
    user = User.objects.get(pk = user_id)
    followings = Follow.objects.filter(follower = user)
    return len(followings)

def profile(request, user_id):
    user = User.objects.get(pk = user_id)
    this_user_posts = Post.objects.filter(user= user)
    reversed_posts = []
    for i in reversed(range(len(this_user_posts))):
        reversed_posts.append(this_user_posts[i])

    follow = True
    try:
        Follow.objects.get(followed_person = user, follower = request.user)
        follow = True
    except ObjectDoesNotExist:
        follow = False
    
    follower_count = count_follower(user_id)
    following_count = count_follower(user_id)


    return render(request, 'network/profile.html', {'posts': reversed_posts, 'follow': follow, "post_user_id": user_id, "followers": follower_count, "following": following_count} )



def follow_user(request, post_user_id):
    followed_person = User.objects.get(id=post_user_id)
    follower = User.objects.get(pk = request.user.id)
    Follow.objects.create(followed_person = followed_person, follower = follower)

    return HttpResponseRedirect((request.META.get('HTTP_REFERER')))

def unfollow_user(request, post_user_id):
    following_person = User.objects.get(pk = post_user_id)
    follower = User.objects.get(pk = request.user.id)
    Follow.objects.get(follower = following_person, followed_person= follower).delete()

    return HttpResponseRedirect((request.META.get('HTTP_REFERER')))




