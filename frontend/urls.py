from django.urls import path, include
from .views import *

urlpatterns = [
    # Page routes
    path("", index, name="index"),
]
