from backend.models import Family, Member
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime as dt


def index(request):
    print(f'THE USER IS {request.user}')
    request.session.save()
    print(request.session)
    print(request)
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
        password =  request.POST['password']
        
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
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user, backend="members.customauthbackend.EmailAuthBackend")
            request.session.save()
            # Redirect to a success page.
            return render(request, 'index.html')
        else:
            # Return an 'invalid login' error message.
            print(f"{user} Never authenticated\nREQUEST.POST details --> {request.POST}")
            messages.error(request, "Invalid email or password! Please try again.")
            return render(request, 'index.html')
    
    return render(request, "register.html", {"token": csrftoken})

def login_user(request):
    csrftoken = get_token(request)
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(f'THE USER IS {user}')
        if user:
            print(f"{username} {password} has been authenticated as {user}.\nREQUEST.POST details --> {request.POST}")
            login(request, user, backend="backend.customauthbackend.EmailAuthBackend")
            request.session.save()
            print(request.session)
            print(request)
            messages.success(request, "Successfully logged in!")
            print(f"Has been logged in {user}")
            # Redirect to a success page.
            return redirect('index')
        else:
            messages.warning(request, "Invalid details")
            pass

    return render(request, "login.html", {"token": csrftoken})

def logout_user(request):
    user = request.user
    persona = Member.objects.get(uuid=user.uuid)
    """
    Update the last activity time for the current user.

    Args:
        request (HttpRequest): The current HTTP request.
    """
    if request.user.is_authenticated:
        # Get the session key for the current user
        session_key = request.session.session_key

        # Get the session object for the current user
        session = Session.objects.get(session_key=session_key)

        # Update the last activity time for the session
         # Activate the GMT +3 timezone
         # Get the Nairobi timezone object
        import pytz
        nairobi_tz = pytz.timezone('Africa/Nairobi')

        session.last_activity = dt.now(nairobi_tz)
        session.save()
        print(persona, session.last_activity)
    
    persona.last_logged = session.last_activity
    persona.save()
    logout(request)
    messages.success(request, "Sign Out Successful")
    return redirect('index')