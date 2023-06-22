# Nostalgia

Nostalgia is a web application that allows users to create and share stories about their family members. Users can also view and edit their family tree, upload images of their relatives, and explore their family history.

## Features

- Create and edit stories about your family members
- View and edit your family tree
- Upload and manage images of your relatives
- Explore your family history with interactive charts and maps
- Connect with other users who share your ancestry

## Installation

To install Nostalgia, you'll need to have Python 3.9 or higher and Django 3.2 or higher installed on your system. You'll also need to install the following dependencies:

- ReactPy: A Python library for creating reactive web components
- aiohttp: An asynchronous HTTP client/server framework
- channels: A Django extension that provides support for WebSockets and other asynchronous features
- Pillow: A Python imaging library


To run Nostalgia, you’ll need to clone this repository and navigate to the project directory:
```
git clone https://github.com/tevin/nostalgia.git
cd nostalgia
```

You can install these dependencies using pip:
```
pip install -r requirements.txt
```

Then, you’ll need to apply the migrations and run the application using Uvicorn
```
python manage.py migrate
uvicorn nostalgia.asgi:application --reload
```


You can access the web application at <http://localhost:8000/>

## Usage

To use Nostalgia, you'll need to register an account or log in with an existing one. You can then create your profile and add your family members. You can also create and edit stories about your relatives, upload images of them, and view your family tree.

You can also explore your family history by using the charts and maps features. You can see the distribution of your ancestors by country, region, or city. You can also see the timeline of your ancestors' births and deaths.

You can also connect with other users who share your ancestry. You can send messages to them, view their profiles and stories, and invite them to join your family tree.

## License

Nostalgia is licensed under the MIT License. See the LICENSE file for more details.
