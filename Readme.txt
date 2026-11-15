LITTLE LEMON - BACK-END CAPSTONE (Django REST Framework + MySQL)

HOW TO RUN
1. In MySQL run:  CREATE DATABASE littlelemon;
2. In littlelemon/settings.py (DATABASES) set your MySQL USER and PASSWORD.
3. In the VS Code terminal:
     pipenv install
     pipenv shell
     python manage.py makemigrations
     python manage.py migrate
     python manage.py runserver
4. Run the unit tests with:  python manage.py test

API PATHS TO TEST (base URL http://127.0.0.1:8000)
/                           Static HTML home page
/api/menu/                  GET list menu items | POST create item (login required)
/api/menu/1/                GET / PUT / PATCH / DELETE a single menu item
/api/bookings/              GET list bookings | POST create booking (login required)
/api/bookings/1/            GET / PUT / PATCH / DELETE a single booking (login required)
/auth/users/                POST registration  {"username": "...", "password": "..."}
/auth/token/login/          POST login -> returns {"auth_token": "..."}
/auth/token/logout/         POST logout (needs token)
/auth/users/me/             GET current user (needs token)
/admin/                     Django admin

TESTING IN INSOMNIA
1. POST /auth/users/  with JSON body {"username":"testuser","password":"Str0ngPass!234"}
2. POST /auth/token/login/ with the same body; copy the "auth_token" value.
3. For protected requests add the header:   Authorization: Token <auth_token>
4. POST /api/menu/      body {"title":"Greek Salad","price":"12.99","inventory":20}
5. POST /api/bookings/  body {"name":"Jane","no_of_guests":4,"booking_date":"2026-12-01T19:00:00Z"}
6. GET /api/menu/ and GET /api/bookings/ to see the data.
