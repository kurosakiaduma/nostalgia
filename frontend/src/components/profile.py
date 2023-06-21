from reactpy import *
from app_widgets import LoadingIndicator
import aiohttp
 
@component
def UserProfile(userUUID:str):
    [user, setUser] = use_state(None)
    [images, setImages] = use_state([])
    
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
                
    use_effect(fetch_user, [])
    
    if not user:
        return LoadingIndicator()
    
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
                        html.p({"class_name": "card-text"}, f"Email: {user['email']}"),
                        html.p({"class_name": "card-text"}, f"Gender: {user['gender']}"),
                        html.p({"class_name": "card-text"}, f"Birth Date: {user['birth_date']}"),
                    )
                )
            ),
            html.div(
                {"class_name": "col-md-6"},
                html.h3({"class_name": "text-center mt-5"}, "Images"),
                html.div(
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
            )
        )
    )