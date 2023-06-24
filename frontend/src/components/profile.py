from django.core.paginator import Paginator
from reactpy import *
from .app_widgets import LoadingIndicator
import aiohttp
 
@component
def UserProfile(userUUID:str):
    [user, setUser] = use_state(None)
    [images, setImages] = use_state([])
    [otherNames, setOtherNames] = use_state('')
    [birthDate, setBirthDate] = use_state('')
    [gender, setGender] = use_state('')
    [isLoading, setIsLoading] = use_state('')
    [resultMessage, setResultMessage] = use_state('')
    [family, setFamily] = use_state(None)
    [stories, setStories] = use_state([])
    [activeTab, setActiveTab] = use_state('images')
    [page, setPage] = use_state(1)
    location = use_location()
    [image, setImage] = use_state('')
    [imageResultMessage, setImageResultMessage] = use_state('')

    
    async def fetch_user():
        async with aiohttp.ClientSession() as session:
            # Fetch user
            user_response = await session.get(f'http://localhost:8000/api/get-user?userUUID={userUUID}')
            # Check the response status and update the state
            if user_response.status == 200:
                user_data = await user_response.json()
                setUser(user_data)
                
            # Fetch images
            images_response = await session.get(f'http://localhost:8000/api/get-images?userUUID={userUUID}')
            # Check the response status and update the state
            if images_response.status == 200:
                images_data = await images_response.json()
                setImages(images_data)
                
            # Fetch family
            family_response = await session.get(f'http://localhost:8000/api/get-family?userUUID={userUUID}')
            # Check the response status and update the state
            if family_response.status == 200:
                family_data = await family_response.json()
                setFamily(family_data)
                
            # Fetch stories
            stories_response = await session.get(f'http://localhost:8000/api/get-stories?userUUID={userUUID}')
            # Check the response status and update the state
            if stories_response.status == 200:
                stories_data = await stories_response.json()
                setStories(stories_data)
                
    use_effect(fetch_user, [])
    
    @event(prevent_default=True)
    async def handleSaveChanges(props: dict):
        setIsLoading(True)
        
        setOtherNames(((props.get("currentTarget")).get("elements")[0]).get("value"))
        setBirthDate(((props.get("currentTarget")).get("elements")[1]).get("value"))
        setGender(((props.get("currentTarget")).get("elements")[2]).get("value"))

        async with aiohttp.ClientSession() as session:
            # Update member details
            update_response = await session.post(f'http://localhost:8000/api/update-member-details?userUUID={userUUID}',
                                                 json={
                                                     'userUUID': str(userUUID),
                                                     'otherNames': otherNames,
                                                     'birthDate': birthDate,
                                                     'gender': gender
                                                 })
            
            # Check the response status and update the state
            if update_response.status == 200:
                update_data = await update_response.json()
                setResultMessage(update_data['message'])
                setIsLoading(False)
            else:
                setResultMessage(f'An error occured while updating your profile 😓 \nTry again 🥺')
                setIsLoading(False)
    
    @event(prevent_default=True)
    async def handleImageChanges(props: dict):
        setIsLoading(True)
        # Get the image file from the props parameter
        image_file = props['currentTarget']['elements'][0]['files'][0]
        setImage(image_file)
        print(f'\n\nTHIS IS THE IMAGE=> {image_file}')
        async with aiohttp.ClientSession() as session:
            # Update member image
            # Use aiohttp.MultipartWriter to create a multipart/form-data object
            # Use aiohttp.MultipartWriter.append_formdata to add the image file and alt text as parts of the object
            mp = aiohttp.MultipartWriter()
            mp.append_form('image', image_file)
            mp.append_form('alt', 'display-image')
            update_image_response = await session.post(f'http://localhost:8000/api/update-member-image?userUUID={userUUID}', data=mp)

            # Check the response status and update the state variables
            if update_image_response.status == 200:
                update_image_data = await update_image_response.json()
                setImageResultMessage(update_image_data['message'])
                setIsLoading(False)
            else:
                setImageResultMessage(f'An error occured while updating your image 😓 \nTry again 🥺')
                setIsLoading(False)
        
    if not user:
        return LoadingIndicator()
    
    def renderImages():
        return html.div(
            {"class_name": "row"},
            [html.div(
                {"class_name": "col-md-4 mb-3"},
                html.img({
                    "src": image['url'],
                    "class_name": "img-thumbnail",
                    "width": 150,
                    "height": 150
                })
            ) for image in images]
        )
    
    def renderFamily():
        print(family['spouse_and_children'])
        return html.div(
            {},
            html.div(
                {"class_name": "row mb-3"},
                html.h4({"class_name": "col-md-12 text-center"}, "Spouse & Children"),
                [html.div(
                    {"class_name": "col-md-4 col-sm-6 d-flex justify-content-center align-items-center flex-column", "style": {"min-height": "100px"}},
                    html.img({
                        "src": member['display_image'],
                        "class_name": "rounded-circle text-center",
                        "width": 50,
                        "height": 50,
                        "style": {"border": f"2px solid {'purple' if member['relation'] == 'spouse' else 'green'}", "object-fit": "cover"}
                    }),
                    html.p({"class_name": "text-center", "style": {"height": "1.5em"}}, f"{'💍'+ member['fname']  if member['relation'] == 'spouse' else member['fname']} {member['lname']}")
                ) for member in family['spouse_and_children']]
            ),
            html.div(
                {"class_name": "row mb-3"},
                html.h4({"class_name": "col-md-12 text-center"}, "Parents"),
                [html.div(
                    {"class_name": "col-md-6 col-sm-6 d-flex justify-content-center flex-column", "style": {"min-height": "100px"}},
                    html.img({
                        "src": member['display_image'],
                        "class_name": "rounded-circle text-center",
                        "width": 50,
                        "height": 50,
                        "style": {"border": "2px solid blue", "object-fit": "cover"}
                    }),
                    html.p({"class_name": "text-center", "style": {"height": "1.5em"}}, f"{member['fname']} {member['lname']}")
                ) for member in family['parents']]
            ),
            html.div(
                {"class_name": "row mb-3"},
                html.h4({"class_name": "col-md-12 text-center"}, "Siblings"),
                [html.div(
                    {"class_name": "col-md-4 col-sm-6 d-flex justify-content-center flex-column", "style": {"min-height": "100px"}},
                    html.img({
                        "src": member['display_image'],
                        "class_name": "rounded-circle text-center",
                        "width": 55,
                        "height": 55,
                        "style": {"border": "2px solid red", "object-fit": "cover"}
                    }),
                    html.p({"class_name": "text-center", "style": {"height": "1.5em"}}, f"{member['fname']} {member['lname']}")
                ) for member in family['siblings']]
            ),
            html.div(
                {"class_name": "row mb-3"},
                html.h4({"class_name": "col-md-12 text-center"}, "Grandchildren"),
                [html.div(
                    {"class_name": "col-md-4 col-sm-6 d-flex justify-content-center flex-column", "style": {"min-height": "100px"}},
                    html.img({
                        "src": member['display_image'],
                        "class_name": "rounded-circle text-center",
                        "width": 50,
                        "height": 50,
                        "style": {"border": "2px solid orange", "object-fit": "cover"}
                    }),
                    html.p({"class_name": "text-center", "style": {"height": "1.5em"}}, f"{member['fname']} {member['lname']}")
                ) for member in family['grandchildren']]
            )
        )
        
    def renderStories(props: dict):
        # Assume stories is a list of dictionaries with title and content keys
        stories = props['stories']

        # Set the number of stories per page
        per_page = 1

        # Create a Paginator object with the stories list and the per_page value
        paginator = Paginator(stories, per_page)

        # Get the current page number from the state or default to 1
        page_number = props['page']

        # Get the current page object from the paginator
        page_obj = paginator.get_page(page_number)

        # Render the story in the current page using Bootstrap card
        return [
            html.div(
                {},
                html.div(
                    # Render the pagination buttons using Bootstrap pagination component
                    {"class_name": "d-flex justify-content-center"},
                    html.ul(
                        {
                            "class_name": "pagination",
                            "id": "story-pagination",
                        },
                        [
                            # Render the previous button with disabled attribute if it's the first page
                            html.li(
                                {
                                    "key": "previous",
                                    "class_name": "page-item" + (" disabled" if not page_obj.has_previous() else ""),
                                },
                                html.button(
                                    {
                                        "class_name": "page-link",
                                        "disabled": not page_obj.has_previous(),
                                        "onClick": lambda: props['setPage'](page_obj.previous_page_number())
                                        },
                                    "Previous"
                                    )
                                ),
                            # Render the next button with disabled attribute if it's the last page
                            html.li(
                                {
                                    "key": "next",
                                    "class_name": "page-item" + (" disabled" if not page_obj.has_next() else "")
                                    },
                                html.button(
                                    {
                                        "class_name": "page-link",
                                        "disabled": not page_obj.has_next(),
                                        "onClick": lambda: props['setPage'](page_obj.next_page_number())
                                        },
                                    "Next"
                                    )
                                )
                            ]
                        )
                    ),
                html.div(
                    {"class_name": "mb-3"},
                    html.div(
                        {"class_name": "card-body"},
                        html.h5({"class_name": "card-title text-center", "id": "story-title"}, page_obj[0]['title']),
                        html.hr(),
                        html.div({"class_name": "card-text"},
                                 [
                                     html.p({}, paragraph) for paragraph in page_obj[0]['content'].split('\n') if paragraph
                                     ]
                                 )
                        )
                    )
                ),
            ]

    return html.div(
        {"class_name": "container"},
        html.div(
            {"class_name": "row"},
            html.div(
                {"class_name": "col-md-6"},
                html.div(
                    {"class_name": "card mt-5"},
                    html.div(
                        {"class_name": "card-body"},
                        html.h3({"class_name": "card-title text-center"}, f"{user['fname']} {user['lname']}"),
                        html.img({
                            "src": user['display_image'],
                            "class_name": "rounded-circle mx-auto d-block",
                            "width": 150,
                            "height": 150
                            }),
                        html.hr(),
                        # Div to center the content below the image
                        html.div(
                            {"class_name": "text-center"},
                            html.p({"class_name": "card-text"}, f"Other names: {user['other_names']}"),
                            html.p({"class_name": "card-text"}, f"Gender: {user['gender']}"),
                            html.p({"class_name": "card-text"}, f"Birth Date: {user['birth_date']}"),
                            html.p({"class_name": "card-text"}, f"Family Name: {user['family_name']}"),
                            ),
                        html.hr(),
                        html.div({
                            "class_name": "d-grid gap-2",
                        },
                            html.div(
                                {"class_name": "row"},
                                # Three buttons with modals
                                html.div(
                                    {"class_name": "col-12 col-sm-6 col-md-4 col-lg-4 mb-3"},
                                    html.button(
                                        {
                                            # Use data-bs-toggle and data-bs-target attributes to link the button to the modal
                                            "href": "#",
                                            "data-bs-toggle": "modal",
                                            "data-bs-target": "#edit-profile-modal",
                                            "class_name": "btn btn-sm btn-primary mr-2", 
                                            "type": "button",
                                        },
                                        "Edit Profile",
                                    ),
                                ),
                                html.div(
                                    {"class_name": "col-12 col-sm-6 col-md-4 col-lg-4 mb-3"},
                                    html.button(
                                        {
                                            # Use data-bs-toggle and data-bs-target attributes to link the button to the modal
                                            "href": "#",
                                            "data-bs-toggle": "modal",
                                            "data-bs-target": "#change-image-modal",
                                            "class_name": "btn btn-sm btn-success mr-2",
                                            "type": "button"
                                        },
                                        "Change Image",
                                    ),
                                ),
                                html.div(
                                    {"class_name": "col-12 col-sm-6 col-md-4 col-lg-4 mb-3"},
                                    html.button(
                                        {
                                            # Use data-bs-toggle and data-bs-target attributes to link the button to the modal
                                            "href": "#",
                                            "data-bs-toggle": "modal",
                                            "data-bs-target": "#change-password-modal",
                                            "class_name": "btn btn-sm btn-danger mr-2", 
                                            "type": "button",
                                        },
                                        "Change Password",
                                    ),
                                ),
                            )
                        ),                        
                        # Modal for editing profile
                        html.div(
                            {
                                "id": "edit-profile-modal",
                                "class_name": "modal fade",
                                # Use tabindex, role and aria attributes for accessibility
                                "tabindex": "-1",
                                "role": "dialog",
                                "aria-labelledby": "edit-profile-modal-label",
                                "aria-hidden": "true"
                            },
                            html.div(
                                {
                                    "class_name":"modal-dialog modal-dialog-centered",
                                    "role":
                                        "document"
                                },
                            html.div(
                                {
                                    "class_name": "modal-content"
                                },
                                # Add a modal header with a title and a close button
                                html.div(
                                    {
                                        "class_name":"modal-header"
                                    },
                                html.h5(
                                    {
                                        "id":"edit-profile-modal-label",
                                        "class_name":"modal-title"
                                    },
                                    f"Edit Profile: {user['fname']} {user['lname']}"
                                    ),
                            html.button(
                                {
                                    # Use data-dismiss attribute to close the modal
                                    "type":
                                        "button",
                                    "data-bs-dismiss":
                                        "modal",
                                    "aria-label":
                                        "Close",
                                    'class':
                                        'close'
                                },
                                html.span({
                                    "aria-hidden":"true"
                                    },"❌"
                                )
                            )
                        ),
                                html.div({
                                    "class_name": "spinner-border text-danger",
                                    "role": "status"
                                } if isLoading else {},
                                         html.span({
                                            "class_name": "sr-only"
                                        }, "Loading..."
                                        ) if isLoading else None
                                ),
                                html.div({
                                    "class_name": "modal-body"
                                },
                                        html.form(
                                        {
                                            "method": "POST",
                                            'id': 'edit-profile-form',
                                            'onSubmit': handleSaveChanges
                                        },
                                html.div(
                                    {'class': 'form-group'},
                                    html.label(
                                        {
                                            'for': 'other-names-input'
                                        },
                                        f'Other Names'
                                    ),
                                    html.input({
                                        'id': 'other-names-input',
                                        'name': 'otherNames',
                                        'type': 'text',
                                        'class': 'form-control',
                                        'value': user["other_names"],
                                        'onChange': lambda event: setOtherNames(event['target']['value'])
                                    })
                                    ),
                                    html.div({
                                        'class': 'form-group'},
                                            html.label({
                                                'for': 'birth_date-input'},
                                                        f'Birth Date'),
                                            html.input({
                                                'id': 'birth_date-input',
                                                'name': 'birth_date',
                                                'type': 'date',
                                                'value': user['birth_date'],
                                                'placeholder': f'Enter your birth date here',
                                                'required': "false",
                                                'class': 'form-control',
                                                'onChange': lambda event: setBirthDate(event['target']['value'])
                                            })
                                        ),
                                    html.div(
                                        {'class': 
                                            'form-group'},
                                        html.label({'for': 
                                                        'gender-input'},
                                                f'Gender'),
                                        # Use select and option elements for a dropdown list
                                        html.select({
                                            "id": "gender-input",
                                            "name": "gender",
                                            "class": "form-control",
                                                "onChange": lambda event: setGender(event['target']['value'])
                                            },
                                        # Use selected attribute to pre-select the current value
                                        # Repeat this for other options
                                        html.option({
                                            "value": "Male",
                                            "selected": user['gender'] == "Male"
                                        }, "Male"),
                                        html.option({
                                            "value": "Female",
                                            "selected": user['gender'] == "Female"
                                        }, "Female"),
                                        html.option({
                                            "value": "Other",
                                            "selected": user['gender'] == "Other"
                                        }, "Other"),
                                        html.option({
                                            "value": "Prefer Not To Say",
                                            "selected": user['gender'] == 
                                                "Prefer Not To Say"
                                        }, "Prefer Not To Say")
                                        )
                                    ),
                                html.hr({
                                    "style": {"color": "white"}}),
                                # Add a modal footer with a submit button
                                html.div(
                                    {
                                        "class_name":
                                            'modal-footer'
                                    },
                                    # Use type="submit" attribute to submit the form
                                    # Use form attribute to link the button to the form
                                    # Use data-bs-dismiss attribute to close the modal after submitting
                                    html.button(
                                        {
                                            'type': 'submit',
                                            'form': 'edit-profile-form',
                                            'data-bs-dismiss': 'modal',
                                            'class': 'btn btn-primary'
                                        },
                                        "Save Changes"
                                    )
                                )
                            )
                        )
                )
            )
        ),
        # Modal for changing image
        html.div(
            {
                "id": "change-image-modal",
                "class_name":"modal fade",
                # Use tabindex, role and aria attributes for accessibility
                "tabindex":"-1",
                "role":"dialog",
                "aria-labelledby":"change-image-modal-label",
                "aria-hidden":"true"
                },
            html.div(
                {
                    "class_name": "modal-dialog modal-dialog-centered",
                    "role": "document"
                },
                html.div(
                    {
                        "class_name":"modal-content"
                    },
                    # Add a modal header with a title and a close button
                    html.div({
                        "class_name":"modal-header"},
                            html.h5({
                                 "id":"change-image-modal-label",
                                 "class_name":"modal-title"
                                 },
                                     "Change Image"
                                ),
                            html.button({
                                # Use data-bs-dismiss attribute to close the modal
                                "type":"button",
                                "data-bs-dismiss":"modal",
                                "aria-label":"Close",
                                'class':'close'
                            },
                                        html.span({
                                            "aria-hidden":"true"},
                                                  "❌"
                                        )
                            )
                        ),
                    # Add a modal body with an input field for changing image
                    html.form({
                        "method": "POST",
                        'id': 'edit-image-form',
                        'onSubmit': handleImageChanges,
                        'enctype': 'multipart/form-data',
                    },
                              html.div({
                                  "class_name":'modal-body'
                                },
                                        # Use form-group and form-control classes for styling
                                        html.div({
                                            "class_name":'form-group'
                                        },
                                                html.label({
                                                    "for":'image-input'
                                                },
                                                           f"Upload new profile image"
                                                ),
                                                # Use type="file" attribute to allow uploading files
                                                html.input({
                                                    # Use id attribute to link the label and the input
                                                    # Use name attribute to identify the input in the backend
                                                    # Use accept attribute to specify the file types allowed
                                                    # Use required attribute to make the input mandatory
                                                    # You can add more attributes as needed
                                                    'id':'image-input',
                                                    'name':'image',
                                                    'type':'file',
                                                    'accept':'image/*',
                                                    'required':"true",
                                                    'class':'form-control'
                                                })
                                            )
                                        ),
                              # Add a modal footer with a submit button
                              html.div({
                                  "class_name":'modal-footer'
                                },
                                # Use type="submit" attribute to submit the form
                                # Use form attribute to link the button to the form
                                # Use data-bs-dismiss attribute to close the modal after submitting
                                html.button({
                                    'type':'submit',
                                    'form':'edit-image-form',
                                    'data-bs-dismiss':'modal',
                                    'class':'btn btn-primary'
                            },
                                        "Change Image"
                            )
                        )
                    )
                )
            )
        ),
        # Modal for changing password
                    html.div(
                        {
                            "id": "change-password-modal",
                            "class_name":"modal fade",
                            # Use tabindex, role and aria attributes for accessibility
                            "tabindex":"-1",
                            "role":"dialog",
                            "aria-labelledby":"change-password-modal-label",
                            "aria-hidden":"true"
                        },
                        html.div(
                            {
                                "class_name": "modal-dialog modal-dialog-centered",
                                "role": "document"
                            },
                            html.div(
                                {
                                    "class_name":"modal-content"
                                },
                                # Modal header with a title and a close button
                                html.div(
                                    {
                                        "class_name":"modal-header"},
                                    html.h5(
                                        {
                                            "id":"change-password-modal-label",
                                            "class_name":"modal-title"
                                        },
                                        "Change Password"
                                    ),
                                    html.button(
                                        {
                                            # Use data-bs-dismiss attribute to close the modal
                                            "type":"button",
                                            "data-bs-dismiss":"modal",
                                            "aria-label":"Close",
                                            'class':'close'
                                        },
                                        html.span(
                                            {
                                                "aria-hidden":"true"
                                            },
                                            "❌"
                                        )
                                    )
                                ),
                                # Modal body with input fields for changing password
                                html.div(
                                    {
                                        "class_name":'modal-body'
                                    },
                                    # Use form-group and form-control classes for styling
                                    html.div(
                                        {
                                            "class_name":'form-group'
                                        },
                                        html.label(
                                            {
                                                "for":'old-password-input'
                                            },
                                            f"Old Password:"),
                                        # Use type="password" attribute to hide the input value
                                        html.input({
                                            # Use id attribute to link the label and the input
                                            # Use name attribute to identify the input in the backend
                                            # Use placeholder attribute to show a hint
                                            # Use required attribute to make the input mandatory
                                            # You can add more attributes as needed
                                            # Repeat this for other input fields
                                            'id':'old-password-input',
                                            'name':'old_password',
                                            'type':'password',
                                            'placeholder':f'Enter your old password here',
                                            'required':"true",
                                            'class':'form-control'
                                        })
                                        ),
                                    html.div(
                                        {
                                            'class': 'form-group'
                                        },
                                        html.label({
                                            'for': 'new-password-input'
                                        },
                                                   f'New Password:'),
                                        html.input({
                                            'id': 'new-password-input',
                                            'name': 'new_password',
                                            'type': 'password',
                                            'placeholder': f'Enter your new password here',
                                            'required': "true",
                                            'class': 'form-control'
                                        })
                                        ),
                                    html.div(
                                        {
                                            'class': 'form-group'
                                        },
                                        html.label(
                                            {
                                                'for': 'confirm-password-input'
                                            },
                                            f'Confirm Password:'),
                                        html.input({
                                            'id': 'confirm-password-input',
                                            'name': 'confirm_password',
                                            'type': 'password',
                                            'placeholder': f'Enter your new password again','required': "true",
                                            'class': 'form-control'
                                        })
                                    )
                                ),
                                # Add a modal footer with a submit button
                                html.div(
                                    {
                                        "class_name":
                                            'modal-footer'
                                    },
                                    # Use type="submit" attribute to submit the form
                                    # Use form attribute to link the button to the form
                                    # Use data-bs-dismiss attribute to close the modal after submitting
                                    html.button(
                                        {
                                            'type':'submit',
                                            'form':'change-password-form',
                                            'data-bs-dismiss':'modal',
                                            'class':'btn btn-primary'
                                        },
                                        "Change Password"
                                    )
                                )
                            )
                        )
                    )
                )
            )
            ),
            html.div(
                {"class_name": "col-md-6"},
                html.ul(
                    {"class_name": "nav nav-tabs"},
                    html.li({"class_name":"nav-item"},
                            html.a(
                                {
                                    "href": "#",
                                    "onClick": lambda e: setActiveTab('images'),
                                    "className": "nav-link "+("active" if activeTab == 'images' else "")
                                    },
                                "Images 📸"
                                )
                            ),
                    html.li({"class_name":"nav-item"},
                            html.a(
                                {
                                    "href": "#",
                                    "onClick": lambda e: setActiveTab('family'),
                                    "className": "nav-link "+("active" if activeTab == 'family' else "")
                                    },
                                "Family 🏠"
                                )
                            ),
                    html.li({"class_name":"nav-item"},
                            html.a(
                                {
                                    "href": "#",
                                    "onClick": lambda e: setActiveTab('stories'),
                                    "className": "nav-link "+("active" if activeTab == 'stories' else "")
                                },
                                "Stories 📔"
                            )
                            )
                    ),
                (renderImages() if activeTab == 'images' else (renderFamily() if activeTab == 'family' else renderStories({'stories': stories, 'page': page, 'setPage': setPage, 'location': location})))
                )
            )
        )
    