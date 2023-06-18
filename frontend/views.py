from django.shortcuts import render
from django.middleware.csrf import get_token

def index(request):
    csrftoken = get_token(request)
    return render(request,"index.html", {"token": csrftoken})
