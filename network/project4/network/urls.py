
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all_posts", views.all_posts, name="all_posts"),
    path("add_post", views.add_post, name="add_post"),
    path("increase_like/<int:post_id>", views.increase_like, name="increase_like"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow_user/<int:post_user_id>", views.follow_user, name="follow_user"),
    path("unfollow_user/<int:post_user_id>", views.unfollow_user, name="unfollow_user"),

]
