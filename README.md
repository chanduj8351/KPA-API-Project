
# 🚀 KPA Form Data API  – FastAPI Project

This is a backend assignment project built using **FastAPI**, fulfilling the requirements mentioned in the `KPA_form_data.postman_collection.json` API specification.

It includes:
- ✅ JWT-based login API
- ✅ (Optional) Form submission/data-handling API
- ✅ Full SQLite + SQLAlchemy integration
- ✅ Pydantic-based input validation
- ✅ Auto-generated Swagger documentation

---

## 📦 Tech Stack Used

| Component | Stack |
|----------|-------|
| Language | Python 3.11 |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite (used for development) |
| Security | JWT with OAuth2PasswordBearer |
| Docs | Swagger UI `/docs` |

> 💡 Note: PostgreSQL is preferred but SQLite is used here for simplicity and local testing.

---

## 🚀 Project Structure

KPA-API-PROJECT/

   ├── main.py                  ← FastAPI entry point  
   ├── auth.py                  ← Handles JWT authentication & password hashing  
   ├── models.py                ← SQLAlchemy ORM models  
   ├── database.py              ← DB engine & session setup  
   ├── insert_user.py           ← Script to insert test user with hashed password  
   ├── init_db.py               ← Script to create database tables  
   ├── kpa_forms.db             ← SQLite database file  
   ├── postman_collection.json  ← Postman collection with testable API requests  
   ├── requirements.txt         ← Python package dependencies  
   ├── .env                     ← Environment variables  
   ├── .env.example             ← Sample .env file  
   ├── README.md                ← Project readme (you're reading it 😉)
   
---

## 🚀 Setup Instructions

### 🛠️ Requirements
- Python 3.10+ installed
- Virtualenv (optional but recommended)
- `pip` package installer

### 🔄 Step-by-Step Setup

1. **Clone or Extract the Project**
   ```bash
   cd KPA-API-PROJECT
````

2. **Create and Activate Virtual Environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Fix bcrypt bug**
   (Optional but recommended if you hit bcrypt errors)

   ```bash
   pip uninstall bcrypt
   pip install bcrypt==3.2.0
   ```

5. **Create `.env` file**

   ```env
   SECRET_KEY=supersecretkey
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

6. **Initialize the database**

   ```bash
   python init_db.py
   ```

7. **Insert test user (Optional)**

   ```bash
   python insert_user.py
   ```

8. **Run the server**

   ```bash
   uvicorn main:app --reload
   ```

---

## 🔐 Test User Credentials

| Field    | Value       |
| -------- | ----------- |
| Phone    | 1234567890  |
| Password | testpass123 |

Use this to authenticate and get a token at `/api/auth/login`.

---

## 🔗 API Documentation

Once running, visit:
📘 **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
📘 **ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📮 Implemented Endpoints

| Method          | Endpoint           | Description                              |
| --------------- | ------------------ | ---------------------------------------- |
| POST            | `/api/auth/login`  | Authenticates user and returns JWT token |
| (Optional) POST | `/api/form/submit` | Accepts form data and stores it          |
| GET             | `/api/user/me`     | Returns the current user based on token  |

> 🛡️ All protected routes require the `Authorization: Bearer <token>` header.

---

## 📬 Postman Collection

Use `postman_collection.json` provided in the root folder.
It includes:

* Login request
* Auth-protected requests (can paste token manually)

✅ Make sure to **re-test and update it** before final submission.

---

## 📝 Features Implemented

* ✅ Secure login system using JWT
* ✅ SQLite + SQLAlchemy integration
* ✅ Token expiry and password hashing
* ✅ Swagger/OpenAPI documentation
* ✅ Environment-based configuration
* ✅ Modular and readable code
* ✅ Pydantic validation

---

## 🧪 Limitations / Assumptions

* Using SQLite instead of PostgreSQL (acceptable per assignment)
* No front-end included (Postman used for testing)
* Email is optional in user model

---

## 📤 Submission Checklist

✅ `✔` Source code in a ZIP or GitHub
✅ `✔` Updated Postman collection
✅ `✔` README file (this one!)
✅ `✔` Project demo video (screen-recorded)
✅ `✔` Submit links to code + video to:
📧 `contact@suvidhaen.com`


---

## 🙌 Author

**Name:** J Chandu
**Email:** chanduj8351@gmail.com

---

