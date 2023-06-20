from backend.models import Family, Member
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request,"index.html")
    
def check_email(request):
    email = request.GET.get('email')
    email_exists = Member.objects.filter(email=email).exists()
    print(f'email=>{email}\n\nemail_exists=>{email_exists}')
    return JsonResponse({'email_exists': email_exists})

def register_user(request):
    csrftoken = get_token(request)
    if request.method == "POST":
        
        familyName =  request.POST['familyName']
        firstName =  request.POST['firstName']
        lastName =  request.POST['lastName']
        email =  request.POST['email']
        gender =  request.POST['gender']
        dob =  request.POST['date']
        password =  request.POST['familyName']
        
        family =  Family.objects.create(name=familyName)
       
        member = Member.objects.create(
            email=email,
            fname=firstName,
            lname=lastName,
            gender=gender,
            birth_date=dob, 
            password=password,
            family=family,
            is_housekeeper=True,
        )         
        #Hash password before saving user to db
        member.set_password(password)
        member.save()
        
        print(family, member)
        
        user = authenticate(request, username=email, password=password)
        print(f'THE USER IS {user}')
        if user:
            print(f"{email} {password} has been authenticated as {user}.\nREQUEST.POST details --> {request.POST}")
            login(request, user, backend="members.customauthbackend.EmailAuthBackend")
            print(f"Has been logged in {user}")
            # Redirect to a success page.
            return redirect('index')
        else:
            # Return an 'invalid login' error message.
            print(f"{user} Never authenticated\nREQUEST.POST details --> {request.POST}")
            messages.error(request, "Invalid email or password! Please try again.")
            return redirect('index')
    
    return render(request, "register.html", {"token": csrftoken})

def login_user(request):
    return render(request, "login.html")