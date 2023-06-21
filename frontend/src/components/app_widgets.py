import aiohttp
from backend.models import GENDER_CHOICES
from reactpy import *
import asyncio


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
                   "Birth Date:"
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
def otherNames():
    [otherNames, setotherNames] = use_state('')
    
    return html.div(
        {
            "class_name": "mb-3"
        },
        html.label
        ({
            "html_for": "otherNames",
            "class_name": "form-label"
            }, "Other names"
        ),
        html.input
        ({
            "type": "text",
            "name":"otherNames",
            "class_name": "form-control","required": "True",
            "value": otherNames,
            "title": "Your other names",
            "onChange": lambda event: setotherNames(event['target']['value'])
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
def SpouseSelect(familyUUID:str, userUUID:str):
    [spouses, setSpouses] = use_state([])
    [spouse, setSpouse] = use_state(None)
    
    async def fetch_spouses():
        async with aiohttp.ClientSession() as session:
            # Fetch spouses
            spouses_response = await session.get(f'http://localhost:8000/api/get-spouses?familyUUID={familyUUID}&userUUID={userUUID}')
            # Check the response status and update the state
            if spouses_response.status == 200:
                spouses_data = await spouses_response.json()
                print(f'SPOUSES DATA=>{spouses_data}')
                setSpouses(spouses_data)
                
    use_effect(fetch_spouses, [])
    
    return html.div(
        html.div({"class": "mb-3"},
            html.label({
                "html_for": "spouse-select",
                "class_name": "mb-3"}, "Spouse 💍"),
            html.select({   
                        "name": "spouse",
                        "class_name": "form-control",
                        "id": "spouse-select",
                        "value": spouse,
                        "onChange": lambda event: setSpouse(event['target']['value'])
                        },
                        [html.option({"value": ""}, "None")] + [html.option({"value": member['id']}, f"{member['fname']} {member['lname']}") for member in spouses]
                        )
            )
        )

@component
def ParentSelect(familyUUID:str, userUUID:str):
    [fathers, setFathers] = use_state([])
    [mothers, setMothers] = use_state([])    
    [mother, setMother] = use_state(None)
    [father, setFather] = use_state(None)
    
    async def fetch_parents():
        async with aiohttp.ClientSession() as session:
            # Fetch fathers
            fathers_response = await session.get(f'http://localhost:8000/api/get-fathers?familyUUID={familyUUID}&userUUID={userUUID}')
            # Check the response status and update the state
            if fathers_response.status == 200:
                fathers_data = await fathers_response.json()
                setFathers(fathers_data)
            
            # Fetch mothers
            mothers_response = await session.get(f'http://localhost:8000/api/get-mothers?familyUUID={familyUUID}&userUUID={userUUID}')
            # Check the response status and update the state
            if mothers_response.status == 200:
                mothers_data = await mothers_response.json()
                setMothers(mothers_data)
                
    use_effect(fetch_parents, [])
    
    return html.div(
        html.div({"class": "mb-3"},
            html.label({
                "html_for": "mother-select",
                "class_name": "mb-3"}, "Mother:"),
            html.select({   
                "name": "mother",
                "class_name": "form-control",
                "id": "mother-select",
                "value": mother,
                "onChange": lambda event: setMother(event['target']['value'])
            },
                        [html.option({"value": ""}, "None")] + [html.option({"value": member['id']}, f"{member['fname']} {member['lname']}") for member in mothers]
                        )
            ),
        html.div({"class": "mb-3"},
            html.label({
                "html_for": "father-select",
                "class_name": "mb-3"}, "Father:"),
            html.select({   
                "name": "father",
                "class_name": "form-control",
                "id": "father-select",
                "value": father,
                "onChange": lambda event: setFather(event['target']['value'])
            },
                            [html.option({"value": ""}, "None")] + [html.option({"value": member['id']}, f"{member['fname']} {member['lname']}") for member in fathers]
            )
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
        {"class_name": "row mb-3"},
        html.div
        (
        {"class_name": "mb-3 col-md-6"},
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
            {"class_name": "mb-3 col-md-6"},
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
    
@component
def MemberImageUpload():
    [image, setImage] = use_state(None)
    
    return html.div(
        {"class_name": "mb-3"},
        html.label({"class_name": "form-label"}, "Family member image: "),
        html.input({
            "class_name": "form-control",
            "name":"image",
            "type": "file",
            "accept": "image/*",
            "onChange": lambda event: setImage(event['target']['files'][0])
        }),
    )

@component
def LoadingIndicator():
    return html.div(
        {"class_name": "d-flex justify-content-center align-items-center main-div"},
        html.div(
            {"class_name": "loading-indicator"},
            html.span({}, "."),
            html.span({}, "."),
            html.span({}, ".")
        ),
        css={
            ".loading-indicator span": {
                "animation-name": "bounce",
                "animation-duration": "1.4s",
                "animation-iteration-count": "infinite",
                "animation-timing-function": "ease-in-out",
                "display": "inline-block",
                "font-size": 24,
            },
            ".loading-indicator span:nth-child(1)": {
                "animation-delay": "-0.32s",
            },
            ".loading-indicator span:nth-child(2)": {
                "animation-delay": "-0.16s",
            },
            "@keyframes bounce": {
                "0%, 80%, 100%": {
                    "transform": "scale(0)",
                },
                "40%": {
                    "transform": "scale(1)",
                }
            }
        }
    )