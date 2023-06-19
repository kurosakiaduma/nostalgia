from django.shortcuts import render
from django.contrib import messages
from django.middleware.csrf import get_token

def index(request):
    csrftoken = get_token(request)
    if request.method == "POST":
        print(request.POST)
        return render(request,"index.html", {"token": csrftoken})

    else:
        return render(request,"index.html", {"token": csrftoken})
