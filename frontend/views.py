from django.shortcuts import render
from django.http import request
from django.contrib.auth.models import AnonymousUser

def index(request):
    print(f"{(request.user)}")
    return render(request,"index.html")