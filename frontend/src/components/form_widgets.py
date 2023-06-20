import aiohttp
from backend.models import GENDER_CHOICES
from reactpy import *


@component
def DateInput():
    [date, setDate] = use_state('')

    return html.div(
        {
            "class_name": "mb-3"
        },
        html.label({
            "class_name": "form-label mb-3",
            "html_for": "date-input"
            },
                   "Date:"
        ),
        html.input({
            "type": "date",
            "name":"date",
            "class_name": "form-control mb-3","required": "True",
            "id": "date-input",
            "value": date,
            "onChange": lambda event: setDate(event['target']['value'])
            })
        )


@component
def lastName():
    [lastName, setLastName] = use_state('')
    
    return html.div(
        {
            "class_name": "mb-3"
        },
        html.label
        ({
            "html_for": "lastName",
            "class_name": "form-label"
            }, "Last name"
        ),
        html.input
        ({
            "type": "text",
            "name":"lastName",
            "class_name": "form-control","required": "True",
            "value": lastName,
            "title": "Your surname name",
            "onChange": lambda event: setLastName(event['target']['value'])
            })
        )

@component
def firstName():
    [firstName, setFirstName] = use_state('')
    return html.div(
        {"class_name": "mb-3"},
        html.label(
            {
                "class_name": "form-label",
                "html_for": "firstName"
            }, 
            "First name"
        ),
        html.input({
            "type": "text",
            "name":"firstName",
            "class_name": "form-control",
            "required": "True",
            "value": firstName,
            "title": "Your first name",
            "onChange": lambda event: setFirstName(event['target']['value'])
        })
        )
    
@component
def familyName():
    [familyName, setFamilyName] = use_state('')
    
    return html.div(
        {"class_name": "mb-3"},
        html.label({"class_name": "form-label",
                    "html_for": "familyName",
                    }, 
                   "Family name"),
        html.input({
            "type": "text",
            "name":"familyName",
            "class_name": "form-control",
            "required": "True",
            "value": familyName,
            "title": "The main family surname",
            "onChange": lambda event: setFamilyName(event['target']['value'])
            })
        )

@component
def genderSelect():
    [gender, setGender] = use_state("Prefer Not To Say")
    
    return html.div({"class": "mb-3"},
                    html.label({
                        "html_for": "gender-select",
                        "class_name": "mb-3"}, "Gender:"),
                    html.select({   
                                 "name": "gender",
                                 "class_name": "form-control",
                                 "id": "gender-select",
                                 "value": gender,
                                 "onChange": lambda event: setGender(event['target']['value'])
                                 },
                                [html.option({"value": value}, label) for value, label in GENDER_CHOICES]
                                )
                    )

@component
def auth_details():
    [email, setEmail] = use_state('')
    [emailError, setEmailError] = use_state('')
    [password, setPassword] = use_state('')
    connection = use_connection()
    location = use_location()
    scope = use_scope()

    # Access information about the current connection, location, and scope
    current_url = location.pathname + location.search
    
    @event(prevent_default=True)
    async def handleEmailChange(event):
        email = event['target']['value']
        setEmail(email) # Update the email state
        
        # Make an API call to backend to check if the email already exists in the database
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://localhost:8000/api/check-email?email={email}') as response:
                data = await response.json()
                if data['email_exists'] and not("login" in current_url):
                    # Display an error message to the user
                    setEmailError('A member with this email already exists')
                else:
                    setEmailError('')
    
    return html.div(
        {"class_name": "mb-3"},
        html.div
        (
        {"class_name": "mb-3"},
        html.label({"class_name": "form-label"}, "Email"),
        html.input({
            "type": "email",
            "name":"email",
            "class_name": f"form-control {'is-invalid' if emailError else ''}",
            "required": "True",
            "value": email,
            "onChange": handleEmailChange
            }),
        html.div({"class_name": "invalid-feedback"}, emailError),
        ),
        html.div(
            {"class_name": "mb-3"},
                        html.label({"class_name": "form-label"}, "Password"),
                        html.input({
                            "type": "password",
                            "name":"password",
                            "class_name": "form-control",
                            "required": "True",
                            "value": password,
                            "onChange": lambda event: setPassword(event['target']['value'])
                        })
                    ),
        html.button({
            "type": "submit",
            "class_name": "btn btn-primary mb-3",
            "disabled": bool(emailError)
            },
                    "Submit"
                    )
        )
