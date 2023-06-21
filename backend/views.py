from backend.models import Family, Member, MemberImage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime as dt, date
from dateutil.relativedelta import relativedelta


def index(request):
    print(f'THE USER IS {request.user}')
    request.session.save()
    print("SESSION ITEMS")
    print(request.session.items())
    print("REQUEST")
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
            request.user = user
            messages.success(request, "Created your family. Please log in.")
            return redirect('login_user')
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

        if user:
            login(request, user, backend="backend.customauthbackend.EmailAuthBackend")
            request.session.save()
            messages.success(request, "Successfully logged in!")
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
    return redirect('login_user')

@login_required
def edit_family(request):
    print(f"THE FAMILY IS {request.user.family}")
    csrftoken = get_token(request)
    if request.method == "POST":
        print(f'\nPOST REQUEST DETAILS=> {request.POST}\n')
        family =  request.user.family.uuid
        firstName =  request.POST['firstName'].title()
        otherNames = request.POST['otherNames'].title()
        lastName =  request.POST['lastName'].title()
        email =  request.POST['email']
        father_id = request.POST['father'] or None
        mother_id = request.POST['mother'] or None
        spouse = request.POST['spouse'] or None
        gender =  request.POST['gender']
        dob =  request.POST['date']
        password =  request.POST['password']
        
        family =  Family.objects.get(uuid=family)
       
        
        # Get father instance
        father = None
        if father_id:
            father = Member.objects.get(id=father_id)
        
        # Get mother instance
        mother = None
        if mother_id:
            mother = Member.objects.get(id=mother_id)
        
        member = Member.objects.create(
            email=email,
            fname=firstName,
            lname=lastName,
            gender=gender,
            other_names = otherNames,
            birth_date=dob, 
            password=password,
            father=father,
            mother=mother,
            family=family,
            is_housekeeper=False,
        )
        
        #Hash password before saving user to db
        member.set_password(password)
        member.save()
        
        # Handle spouse assignment
        if spouse:
            member.spouse_of.set([spouse])
        
        # Handle image upload
        image = request.FILES.get('image')
        if image:
            MemberImage.objects.create(member=member, image=image)

    return render(request, "edit_family.html", {"token": csrftoken})

def get_fathers(request):
    family_uuid = request.GET.get('familyUUID')
    user_uuid = request.GET.get('userUUID')
    members = Member.objects.filter(family__uuid=family_uuid, gender="Male").values('id', 'fname', 'lname')
    return JsonResponse(list(members), safe=False)

def get_mothers(request):
    family_uuid = request.GET.get('familyUUID')
    user_uuid = request.GET.get('userUUID')
    members = Member.objects.filter(family__uuid=family_uuid, gender="Female").values('id', 'fname', 'lname')
    return JsonResponse(list(members), safe=False)

def get_spouses(request):
    family_uuid = request.GET.get('familyUUID')
    user_uuid = request.GET.get('userUUID')
    today = date.today()
    age_limit = today - relativedelta(years=17)
    members = Member.objects.filter(family__uuid=family_uuid, birth_date__lte=age_limit).values('id', 'fname', 'lname')
    return JsonResponse(list(members), safe=False)