from django.urls import path, include
from .views import *

urlpatterns = [
    #APIs
    path('api/check-email', check_email, name='check-email'),
    path('api/get-fathers', get_fathers, name='get-fathers'),
    path('api/get-mothers', get_mothers, name='get-mothers'),
    path('api/get-spouses', get_spouses, name='get-spouses'),
    path('api/get-user', get_user, name='get-user'),
    path('api/get-images', get_images, name='get-images'),
    path('api/get-family', get_family, name='get-family'),
    path('api/get-stories', get_stories, name='get-stories'),

    # Page routes
    path("register", register_user, name="register_user"),
    path("login", login_user, name="login_user"),
    path("logout", logout_user, name="logout_user"),
    path("user_profile", user_profile, name="user_profile"),
    path("edit_family", edit_family, name="edit_family"),
]
