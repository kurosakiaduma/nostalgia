from django.shortcuts import render
from django.http import request
from django.contrib.auth.models import AnonymousUser

def index(request):
    if request.USER == AnonymousUser:
        return render("index.html")