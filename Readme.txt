# Little Lemon — Back-End Capstone

A RESTful API built with **Django REST Framework** and **MySQL** for the Little Lemon restaurant. Handles menu management, table bookings, and token-based user authentication—no gatekeeping, just clean endpoints.

---

## 🛠️ Tech Stack
* **Backend:** Python, Django, Django REST Framework (DRF)
* **Database:** MySQL
* **Auth:** Djoser (Token Authentication)
* **Environment:** Pipenv

---

## 🚀 Getting Started (Local Setup)

### 1. Spin up the Database
Open your MySQL client and create the database:
```sql
CREATE DATABASE littlelemon;
```

### 2. Wire Up Your Credentials
Head over to `littlelemon/settings.py`, locate the `DATABASES` config, and plug in your local MySQL `USER` and `PASSWORD`.

### 3. Install & Run
Pop open your terminal in VS Code and run the following:
```bash
# Install dependencies & activate the virtual environment
pipenv install
pipenv shell

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Fire up the local server
python manage.py runserver
```
Your API is now live at **`http://127.0.0.1:8000`** ✨

### 4. Run the Vibe Check (Unit Tests)
Make sure nothing is broken:
```bash
python manage.py test
```

---

## 🗺️ API Endpoints

**Base URL:** `http://127.0.0.1:8000`

### General & Admin

| Endpoint | Methods | Access | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | Public | Static HTML home page |
| `/admin/` | `GET`, `POST` | Staff/Admin | Django admin dashboard |

### Menu & Bookings

| Endpoint | Methods | Access | Description |
| :--- | :--- | :--- | :--- |
| `/api/menu/` | `GET` | Public | Fetch all menu items |
| `/api/menu/` | `POST` | 🔒 Auth Required | Add a new item to the menu |
| `/api/menu/<id>/` | `GET`, `PUT`, `PATCH`, `DELETE` | Public / 🔒 Auth | View, update, or delete a specific menu item |
| `/api/bookings/` | `GET` | Public | View all table bookings |
| `/api/bookings/` | `POST` | 🔒 Auth Required | Create a new table reservation |
| `/api/bookings/<id>/` | `GET`, `PUT`, `PATCH`, `DELETE` | 🔒 Auth Required | View, update, or cancel a specific booking |

### Authentication (Djoser)

| Endpoint | Method | Access | Description |
| :--- | :--- | :--- | :--- |
| `/auth/users/` | `POST` | Public | Register a new user (`username`, `password`) |
| `/auth/token/login/` | `POST` | Public | Log in & grab your `auth_token` |
| `/auth/token/logout/` | `POST` | 🔒 Auth Required | Log out & invalidate your token |
| `/auth/users/me/` | `GET` | 🔒 Auth Required | Get the currently logged-in user's profile |

---

## 🧪 Testing the Flow in Insomnia (or Postman)

Follow this quick flow to test protected routes without hitting `401 Unauthorized` errors:

1. **Register a user**  
   `POST /auth/users/`
   ```json
   {
     "username": "testuser",
     "password": "Str0ngPass!234"
   }
   ```

2. **Grab your token**  
   `POST /auth/token/login/` with the same JSON body above. Copy the `auth_token` string from the response.

3. **Set your Auth Header**  
   For any protected request below, add this to your request headers:
   ```text
   Authorization: Token <your_auth_token>
   ```

4. **Create a menu item**  
   `POST /api/menu/`
   ```json
   {
     "title": "Greek Salad",
     "price": "12.99",
     "inventory": 20
   }
   ```

5. **Book a table**  
   `POST /api/bookings/`
   ```json
   {
     "name": "Jane",
     "no_of_guests": 4,
     "booking_date": "2026-12-01T19:00:00Z"
   }
   ```

6. **Verify everything saved**  
   Hit `GET /api/menu/` and `GET /api/bookings/` to see your fresh data in action.
