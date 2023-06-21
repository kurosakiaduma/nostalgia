from reactpy import *
from .form_widgets import *
    
    
@component
def registerFamily(csrftoken: str):  
    return html.div(
        {"class_name": "container"},
        html.div(
            {"class_name": "card mt-5"},
            html.div(
                {"class_name": "card-body"},
                html.h3({"class_name": "card-title text-center"}, "Sign your family up 👨🏾‍👩🏾‍👧🏾‍👦🏾"),
                html.form(
                    {
                     "method": "POST",
                    },
                    html.input({
                        "type": "hidden",
                        "name": "csrfmiddlewaretoken",
                        "value": csrftoken
                        }),
                    familyName(),
                    firstName(),
                    lastName(),
                    genderSelect(),
                    DateInput(),
                    auth_details(),
                )
            )
        )
    )
    
@component
def newMember(csrftoken: str, familyName: str):  
    return html.div(
        {"class_name": "container"},
        html.div(
            {"class_name": "card mt-5"},
            html.div(
                {"class_name": "card-body"},
                html.h3({"class_name": "card-title text-center"}, "Add a new family member 👨🏾‍👩🏾‍👧🏾‍👦🏾"),
                html.form(
                    {
                     "method": "POST",
                    },
                    html.input({
                        "type": "hidden",
                        "name": "csrfmiddlewaretoken",
                        "value": csrftoken
                        }),
                    firstName(),
                    otherNames(),
                    lastName(),
                    genderSelect(),
                    DateInput(),
                    ParentSelect(familyName),
                    auth_details(),
                )
            )
        )
    )