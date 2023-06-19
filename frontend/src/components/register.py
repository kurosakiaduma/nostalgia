from asgiref.sync import sync_to_async
from reactpy import *
from backend.models import *
from django.db.utils import IntegrityError
from django.contrib import messages
from django.contrib.auth.hashers import make_password

@component
def DateInput():
    [date, setDate] = use_state('')

    return html.div(
        html.label({"class": "form-label", "for": "date-input"}, "Date:"),
        html.input({
            "type": "date",
            "name":"date",
            "class": "form-control",
            "id": "date-input",
            "value": date,
            "onChange": lambda event: setDate(event['target']['value'])
        })
    )


@component
def registerFamily(csrftoken: str):
    [familyName, setFamilyName] = use_state('')
    [firstName, setFirstName] = use_state('')
    [lastName, setLastName] = use_state('')
    [email, setEmail] = use_state('')
    [gender, setGender] = use_state("Prefer Not To Say")
    [password, setPassword] = use_state('')

    @sync_to_async
    def create_family(familyName):
        return Family.objects.create(name=familyName)
    
    @sync_to_async
    def create_housekeeper(firstName, lastName, email, gender, dob, password, family):
        #Hash password before saving user to db
        password = make_password(password)
        return Member.objects.create(
            email=email,
            fname=firstName,
            lname=lastName,
            gender=gender,
            birth_date=dob, 
            password=password,
            family=family,
            is_housekeeper=True,
        )
        
    async def handleSubmit(event):
        # Get the form data
        formData = event.get("target").get("elements")
        
        familyName = formData[0]['value']
        firstName = formData[1]['value']
        lastName = formData[2]['value']
        username = formData[3]['value']
        gender = formData[4]['value']
        dob = formData[5]['value']
        password = formData[6]['value']
        
        try:
            # Create a new family
            family = await create_family(familyName)
            
            # Create a new member for the family
            member = await create_housekeeper(firstName, lastName, username, gender, dob, password, family)
            print(f'family=> {family}\n member=> {member}')
                
        except IntegrityError:
            messages.warning("Already present user")
        
        
        
    return html.div(
        {"class": "container"},
        html.div(
            {"class": "card mt-5"},
            html.div(
                {"class": "card-body"},
                html.h3({"class": "card-title text-center"}, "Sign your family up 👨🏾‍👩🏾‍👧🏾‍👦🏾"),
                html.form(
                    {"on_submit": handleSubmit,
                     "method": "POST",
                    
                    },
                    html.input({
                        "type": "hidden",
                        "name": "csrfmiddlewaretoken",
                        "value": csrftoken
                        }),
                    html.div(
                        {"class": "mb-3"},
                        html.label({"class": "form-label",
                                    "for": "familyName"}, 
                                   "Family name"),
                        html.input({
                            "type": "text",
                            "name":"familyName",
                            "class": "form-control",
                            "required": "True",
                            "value": familyName,
                            "onChange": lambda event: setFamilyName(event['target']['value'])
                        })
                    ),
                    html.div(
                        {"class": "mb-3"},
                        html.label({"class": "form-label",
                                    "for": "firstName"}, 
                                   "First name"),
                        html.input({
                            "type": "text",
                            "name":"firstName",
                            "class": "form-control",
                            "required": "True",
                            "value": firstName,
                            "onChange": lambda event: setFirstName(event['target']['value'])
                        })
                    ),
                    html.div(
                        {"class": "mb-3"},
                        html.label({"for": "lastName",
                                    "class": "form-label"}, "Last name"),
                        html.input({
                            "type": "text",
                            "name":"lastName",
                            "class": "form-control",
                            "required": "True",
                            "value": lastName,
                            "onChange": lambda event: setLastName(event['target']['value'])
                        })
                    ),
                    html.div(
                        {"class": "mb-3"},
                        html.label({"class": "form-label"}, "Email"),
                        html.input({
                            "type": "email",
                            "name":"email",
                            "class": "form-control",
                            "required": "True",
                            "value": email,
                            "onChange": lambda event: setEmail(event['target']['value'])
                        })
                    ),
                    html.div(
                        html.label({"for": "gender-select",
                                    "class": "mb-3"}, "Gender:"),
                        html.select(
                            {   
                            "name": "gender",
                            "class": "form-control",
                            "id": "gender-select",
                            "value": gender,
                            "onChange": lambda event: setGender(event['target']['value'])
                            },
                            [html.option({"value": value}, label) for value, label in GENDER_CHOICES]
                            )
                        ),
                    html.div({"class": "mb-3"},
                             DateInput()
                             ),
                    html.div(
                        {"class": "mb-3"},
                        html.label({"class": "form-label"}, "Password"),
                        html.input({
                            "type": "password",
                            "name":"password",
                            "class": "form-control",
                            "required": "True",
                            "value": password,
                            "onChange": lambda event: setPassword(event['target']['value'])
                        })
                    ),
                    html.button({"type":"submit",  'className': 'btn btn-primary'}, 'Submit')
                )
            )
        )
    )