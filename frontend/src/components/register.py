import aiohttp
from asgiref.sync import sync_to_async
from backend.models import Family, Member, GENDER_CHOICES
from reactpy import *

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
    [emailError, setEmailError] = use_state('')
    [gender, setGender] = use_state("Prefer Not To Say")
    [password, setPassword] = use_state('')

    async def handleEmailChange(event):
        email = event['target']['value']
        setEmail(email) # Update the email state
        print("I TRIED TO ACTIVATE THIS FUNCTION")
        
        # Make an API call to backend to check if the email already exists in the database
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://localhost:8000/api/check-email?email={email}') as response:
                data = await response.json()
                if data['email_exists']:
                    # Display an error message to the user
                    setEmailError('A member with this email already exists')
                else:
                    setEmailError('')
    
    @sync_to_async
    def create_family(familyName):
        return Family.objects.create(name=familyName)
    
    @sync_to_async
    def create_housekeeper(firstName, lastName, email, gender, dob, password, family):
       
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
        return member
    
    @event(stop_propagation=True, prevent_default=True)            
    async def handleSubmit(event):
        
        # Prevent the form from being submitted if there's an error with email integrity check
        if emailError:
            return
        
        # Get the form data
        formData = event.get("target").get("elements")
        
        familyName = formData[1]['value']
        firstName = formData[2]['value']
        lastName = formData[3]['value']
        username = formData[4]['value']
        gender = formData[5]['value']
        dob = formData[6]['value']
        password = formData[7]['value']
        
        # Create a new family
        family = await create_family(familyName)
                        
        # Create a new member for the family
        await create_housekeeper(firstName, lastName, username, gender, dob, password, family)

        # Make an API call to backend to log in the user
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:8000/api/login', data={'username': username, 'password': password}, headers={'X-CSRFToken': csrftoken}) as response:
                
                data = await response.json()
                print("IN ASYNC LOGIN", data)
                if data['success']:
                    # Login was successful
                    print('Logged in')
                else:
                    # Login failed
                    print('Invalid username or password')        
    
    return html.div(
        {"class": "container"},
        html.div(
            {"class": "card mt-5"},
            html.div(
                {"class": "card-body"},
                html.h3({"class": "card-title text-center"}, "Sign your family up 👨🏾‍👩🏾‍👧🏾‍👦🏾"),
                html.form(
                    {"onSubmit": handleSubmit,
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
                            "class": f"form-control {'is-invalid' if emailError else ''}",
                            "required": "True",
                            "value": email,
                            "onChange": handleEmailChange
                            }),
                        html.div({"class": "invalid-feedback"}, emailError)
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
                    html.button(
                        {
                            "type": "submit",
                            "class": "btn btn-primary",
                            "disabled": bool(emailError)
                        },
                        "Submit"
                    ),
                )
            )
        )
    )