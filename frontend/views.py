from django.shortcuts import render
def index(request):
    request.session.save()
    return render(request,"index.html")
