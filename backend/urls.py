from django.urls import path, include
from .views import *

urlpatterns = [
    #APIs
    path('api/check-email', check_email, name='check-email'),
    path('api/get-fathers', get_fathers, name='get-fathers'),
    path('api/get-mothers', get_mothers, name='get-mothers'),
    # Page routes
    path("register", register_user, name="register_user"),
    path("login", login_user, name="login_user"),
    path("logout", logout_user, name="logout_user"),
    path("edit_family", edit_family, name="edit_family")
]
