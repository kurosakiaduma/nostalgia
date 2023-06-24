from reactpy import *
import aiohttp

@component
def SearchBar(userFamily: str):
    [searchInput, setSearchInput] = use_state('')
    [searchResults, setSearchResults] = use_state([])

    async def handleSearchInputChange(event):
        setSearchInput(event['target']['value'])
        # call async function to fetch search results from API
        results = await fetchSearchResults(searchInput, userFamily)
        # update searchResults state with the results
        setSearchResults(results)

    return html.div({
        },
                    html.input({
                        'type': 'text',
                        'value': searchInput,
                        'onChange': handleSearchInputChange
                    }),
        SearchResults(props={'results': searchResults})
    )


@component
def SearchResults(props: dict):
    return html.div(
        [html.div(
            {"class_name": "card mt-5"},
            html.div(
                {"class_name": "card-body"},
                html.h3({"class_name": "card-title text-center"}, f"{result['fname']} {result['lname']}"),
                html.img({
                    "src": result['display_image'],
                    "class_name": "rounded-circle mx-auto d-block",
                    "width": 150,
                    "height": 150
                    }),
                html.hr(),
                # Div to center the content below the image
                html.div(
                    {"class_name": "text-center"},
                    html.p({"class_name": "card-text"}, f"Other names: {result['other_names']}"),
                    html.p({"class_name": "card-text"}, f"Gender: {result['gender']}"),
                    html.p({"class_name": "card-text"}, f"Birth Date: {result['birth_date']}"),
                    html.p({"class_name": "card-text"}, f"Family Name: {result['family_name']}"),
                    ),
                html.hr(),
                html.div({
                    "class_name": "d-grid gap-2",
                },
                    # Edit button with modal
                    html.button(
                        {
                            # Use data-bs-toggle and data-bs-target attributes to link the button to the modal
                            "href": "#",
                            "data-bs-toggle": "modal",
                            "data-bs-target": "#edit-member-modal",
                            "class_name": "btn btn-sm btn-primary mr-2", 
                            "type": "button",
                        },
                        "Edit Member",
                    ),
                )
            )
        ) for result in props['results']]
    )

async def fetchSearchResults(searchInput, userFamily):
    async with aiohttp.ClientSession() as session:
        # Fetch search results
        response = await session.get(f'http://localhost:8000/api/search?query={searchInput}&userFamily={userFamily}')
        # Check the response status and return the results
        if response.status == 200:
            results = await response.json()
            return results