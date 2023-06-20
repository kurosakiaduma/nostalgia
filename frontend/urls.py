from django.urls import path, include
from .views import *

urlpatterns = [
    #APIs
    path('api/check-email', check_email, name='check-email'),
    # Page routes
    path("", index, name="index"),
    path("register", register_user, name="register_user"),
    path("login", login_user, name="login_user"),
]
