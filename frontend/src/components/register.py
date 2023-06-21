from reactpy import *
from .app_widgets import *
    
    
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
def newMember(csrftoken: str, familyUUID: str, familyName: str, userUUID: str):  
    return html.div(
        {"class_name": "container"},
        html.div(
            {"class_name": "card mt-5"},
            html.div(
                {"class_name": "card-body"},
                html.h3({"class_name": "card-title text-center"}, f"Add a {familyName} 👨🏾‍👩🏾‍👧🏾‍👦🏾 member"),
                html.hr(),
                html.form(
                    {
                     "method": "POST",
                    },
                    html.input({
                        "type": "hidden",
                        "name": "csrfmiddlewaretoken",
                        "value": csrftoken
                        }),
                    # Use a row to wrap the form elements
                    html.div({"class_name": "row"},
                        # Use col-md-6 for each form element
                        html.div({"class_name": "col-md-6"}, MemberImageUpload()),
                        html.div({"class_name": "col-md-6"}, firstName()),
                        html.div({"class_name": "col-md-6"}, lastName()),
                        html.div({"class_name": "col-md-6"}, otherNames()),
                        html.div({"class_name": "col-md-6"}, genderSelect()),
                        html.div({"class_name": "col-md-6"}, DateInput()),
                        html.div({"class_name": "col-md-6"}, ParentSelect(familyUUID, userUUID)),
                        html.div({"class_name": "col-md-6"}, SpouseSelect(familyUUID, userUUID)),
                        html.div({"class_name": "col-md-6"}, auth_details()),
                    )
                )
            )
        )
    )