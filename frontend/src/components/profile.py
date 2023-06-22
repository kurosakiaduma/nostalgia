from django.core.paginator import Paginator
from dash import dcc
import dash as html
from reactpy import *
from .app_widgets import LoadingIndicator
import aiohttp
 
@component
def UserProfile(userUUID:str):
    [user, setUser] = use_state(None)
    [images, setImages] = use_state([])
    [family, setFamily] = use_state(None)
    [stories, setStories] = use_state([])
    [activeTab, setActiveTab] = use_state('images')
    [page, setPage] = use_state(1)
    location = use_location()
    
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
    
    print(f"\n\nTHESE ARE THE STORIES=> {stories}\n\n")
    
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
        return html.div(
            {},
            html.div(
                {"class_name": "row mb-3"},
                html.h4({"class_name": "col-md-12 text-center"}, "Spouse & Children"),
                [html.div(
                    {"class_name": "col-md-2"},
                    html.img({
                        "src": member['display_image'],
                        "class_name": "rounded-circle",
                        "width": 50,
                        "height": 50,
                        "style": {"border": "2px solid green"}
                    }),
                    html.p({"class_name": "text-center"}, f"{member['fname']} {member['lname']}")
                ) for member in family['spouse_and_children']]
            ),
            html.div(
                {"class_name": "row mb-3"},
                html.h4({"class_name": "col-md-12 text-center"}, "Parents"),
                [html.div(
                    {"class_name": "col-md-2"},
                    html.img({
                        "src": member['display_image'],
                        "class_name": "rounded-circle",
                        "width": 50,
                        "height": 50,
                        "style": {"border": "2px solid blue"}
                    }),
                    html.p({"class_name": "text-center"}, f"{member['fname']} {member['lname']}")
                ) for member in family['parents']]
            ),
            html.div(
                {"class_name": "row mb-3"},
                html.h4({"class_name": "col-md-12 text-center"}, "Siblings"),
                [html.div(
                    {"class_name": "col-md-2"},
                    html.img({
                        "src": member['display_image'],
                        "class_name": "rounded-circle",
                        "width": 50,
                        "height": 50,
                        "style": {"border": "2px solid red"}
                    }),
                    html.p({"class_name": "text-center"}, f"{member['fname']} {member['lname']}")
                ) for member in family['siblings']]
            ),
            html.div(
                {"class_name": "row mb-3"},
                html.h4({"class_name": "col-md-12 text-center"}, "Grandchildren"),
                [html.div(
                    {"class_name": "col-md-2"},
                    html.img({
                        "src": member['display_image'],
                        "class_name": "rounded-circle",
                        "width": 50,
                        "height": 50,
                        "style": {"border": "2px solid orange"}
                    }),
                    html.p({"class_name": "text-center"}, f"{member['fname']} {member['lname']}")
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
                    {"class_name": "card mb-3"},
                    html.div(
                        {"class_name": "card-body"},
                        html.h5({"class_name": "card-title"}, page_obj[0]['title']),
                        html.p({"class_name": "card-text"}, page_obj[0]['content'])
                    )
                )
            ),
            html.div(
                # Render the pagination buttons using Bootstrap pagination component
                {"class_name": "d-flex justify-content-center"},
                html.ul(
                    {"class_name": "pagination"},
                    [
                        # Render the previous button with disabled attribute if it's the first page
                        html.li(
                            {
                                "key": "previous",
                                "class_name": "page-item" + (" disabled" if not page_obj.has_previous() else "")
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
            )
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
                        html.p({"class_name": "card-text"}, f"Other names: {user['other_names']}"),
                        html.p({"class_name": "card-text"}, f"Gender: {user['gender']}"),
                        html.p({"class_name": "card-text"}, f"Birth Date: {user['birth_date']}"),
                        html.p({"class_name": "card-text"}, f"Family Name: {user['family_name']}"),
                        html.a(
                            {
                                "href": f"/edit-user?userUUID={userUUID}",
                                "class_name": "btn btn-primary btn-block"
                            },
                            "Edit Profile"
                        )
                    )
                )
            ),
            html.div(
                {"class_name": "col-md-6"},
                html.h3({"class_name": "text-center mt-5"}, activeTab.capitalize()),
                html.ul(
                    {"class_name": "nav nav-tabs"},
                    html.li({"class_name":"nav-item"},
                            html.a(
                                {
                                    "href": "#",
                                    "onClick": lambda e: setActiveTab('images'),
                                    "className": "nav-link "+("active" if activeTab == 'images' else "")
                                    },
                                "Images"
                                )
                            ),
                    html.li({"class_name":"nav-item"},
                            html.a(
                                {
                                    "href": "#",
                                    "onClick": lambda e: setActiveTab('family'),
                                    "className": "nav-link "+("active" if activeTab == 'family' else "")
                                    },
                                "Family"
                                )
                            ),
                    html.li({"class_name":"nav-item"},
                            html.a(
                                {
                                    "href": "#",
                                    "onClick": lambda e: setActiveTab('stories'),
                                    "className": "nav-link "+("active" if activeTab == 'stories' else "")
                                },
                                "Stories"
                            )
                            )
                    ),
                (renderImages() if activeTab == 'images' else (renderFamily() if activeTab == 'family' else renderStories({'stories': stories, 'page': page, 'setPage': setPage, 'location': location})))
                )
            )
        )