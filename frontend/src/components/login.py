from .app_widgets import auth_details
from reactpy import *

@component
def loginForm(csrftoken: str):  
    return html.div(
        {"class_name": "container"},
        html.div(
            {"class_name": "card mt-5"},
            html.div(
                {"class_name": "card-body"},
                html.h3({"class_name": "card-title text-center"}, "Log in 👨🏾‍👩🏾‍👧🏾‍👦🏾"),
                html.form(
                    {
                     "method": "POST",
                    },
                    html.input({
                        "type": "hidden",
                        "name": "csrfmiddlewaretoken",
                        "value": csrftoken
                        }),
                    auth_details(),
                )
            )
        )
    )