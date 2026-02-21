<div align="center">

# ⚙️ Portfolio Backend API

### Django REST Framework API Server for the Portfolio Web Application

[![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16-A30000?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Cloudinary](https://img.shields.io/badge/Storage-Cloudinary-3448C5?logo=cloudinary&logoColor=white)](https://cloudinary.com/)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=white)](https://render.com/)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Technologies Used](#-technologies-used)
- [Database Design](#-database-design)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [Standardized API Responses](#-standardized-api-responses)
- [Error Handling](#-error-handling)
- [Environment Variables](#-environment-variables)
- [Local Setup](#-local-setup)
- [Production Deployment](#-production-deployment)
- [Live API Link](#-live-api-link)
- [Folder Structure](#-folder-structure)

---

## 🎯 Overview

The backend is a **RESTful API server** built with Django 6.0 and Django REST Framework. It serves as the data layer for the portfolio web application, providing:

- **CRUD APIs** for all portfolio sections (Profile, Skills, Projects, Experience, Education, Certifications, Contact)
- **JWT-based authentication** for admin operations with token blacklisting
- **Cloudinary integration** for cloud-based media storage (images, PDFs, resumes)
- **Standardized API responses** with consistent codes, messages, and data structures
- **PostgreSQL** as the production database (hosted on Render)
- **CORS & CSRF** configuration for secure cross-origin communication

---

## 🏗️ Architecture

The backend follows a clean **layered architecture** pattern:

```
Request Flow:
─────────────

Client Request
      │
      ▼
┌─────────────────────┐
│  Gunicorn (WSGI)    │  ← Production server
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Middleware Stack    │
│  ├─ CorsMiddleware  │  ← Cross-origin handling
│  ├─ WhiteNoise      │  ← Static file serving
│  ├─ Session         │
│  ├─ CSRF            │
│  └─ Authentication  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  URL Router         │
│  /api/ → api.urls   │
│  /admin/ → Django   │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  SafeJWT Auth       │  ← Graceful token validation
│  (Fails silently    │     (AnonymousUser on invalid token)
│   for public APIs)  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  API Views (CBVs)   │  ← Business logic
│  ├─ Permission      │     (IsAuthenticatedOrReadOnly /
│  │   checks         │      AllowAny / IsAdminUser)
│  ├─ File upload     │
│  │   handling       │     (Cloudinary upload)
│  └─ @transaction    │
│      .atomic        │     (Database integrity)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Serializers        │  ← Data validation & transformation
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Models (ORM)       │  ← Database abstraction
└──────────┬──────────┘
           ▼
    ┌──────┴──────┐
    ▼             ▼
PostgreSQL    Cloudinary
(Data)        (Media)
```

---

## 🛠️ Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Runtime language |
| Django | 6.0.1 | Web framework |
| Django REST Framework | 3.16.1 | RESTful API toolkit |
| SimpleJWT | 5.5.1 | JWT authentication |
| PostgreSQL | 14+ | Relational database |
| psycopg2-binary | 2.9.10 | PostgreSQL adapter |
| dj-database-url | 2.1.0 | Database URL parser |
| Cloudinary | 1.36.0 | Cloud media storage |
| django-cloudinary-storage | 0.3.0 | Django-Cloudinary bridge |
| django-cors-headers | 4.9.0 | CORS handling |
| Pillow | 12.1.0 | Image processing |
| WhiteNoise | 6.6.0 | Static file serving |
| Gunicorn | 21.2.0 | Production WSGI server |
| python-dotenv | 1.2.1 | Environment variable management |

---

## 🗄️ Database Design

The application uses **8 models** to represent all portfolio data:

```mermaid
erDiagram
    Profile {
        int id PK
        string name
        string title
        text bio
        url profile_picture
        url resume
        email email
        string phone
        text address
        url github_link
        url linkedin_link
        url twitter_link
        url leetcode_link
        datetime created_at
        datetime modified_at
    }

    Skill {
        int id PK
        string name
        int percentage
        string category
        datetime created_at
        datetime modified_at
    }

    Experience {
        int id PK
        string company_name
        string role
        url logo
        date start_date
        date end_date
        text description
        datetime created_at
        datetime modified_at
    }

    Project {
        int id PK
        string title
        url image
        text description
        string tech_stack
        url github_link
        url live_url
        datetime created_at
        datetime modified_at
    }

    Certification {
        int id PK
        string title
        url image
        url pdf_file
        datetime created_at
        datetime modified_at
    }

    Education {
        int id PK
        string institution
        string degree
        date start_date
        date end_date
        text description
        datetime created_at
        datetime modified_at
    }

    Contact {
        int id PK
        string name
        email email
        text message
        datetime sent_at
        datetime created_at
        datetime modified_at
    }

    ContactInfo {
        int id PK
        text address
        email email
        text description
        string phone
        url linkedin_link
        url github_link
        url twitter_link
        url leetcode_link
        datetime created_at
        datetime modified_at
    }
```

### Skill Categories

| Code | Label |
|---|---|
| `LANG` | Programming Languages |
| `WEB` | Web Technologies |
| `AI` | AI/ML Technologies |
| `SOFT` | Soft Skills |

### Notes

- All models include `created_at` (auto set on creation) and `modified_at` (auto updated on save) timestamp fields.
- All list endpoints return records ordered by `-created_at, -id` (newest first).
- Media fields (images, PDFs, resumes) store **Cloudinary URLs**, not local file paths.

---

## 📡 API Documentation

**Base URL:** `https://portfolio-web-app-backend.onrender.com/api/`

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/login/` | Login and obtain JWT tokens | ❌ No |
| `POST` | `/api/logout/` | Logout and blacklist refresh token | ✅ Yes |

#### POST `/api/login/`

**Request Body:**
```json
{
    "username": "admin",
    "password": "your_password"
}
```

**Success Response (200):**
```json
{
    "success": true,
    "return_code": "LOGIN_SUCCESS",
    "message": "Login successful.",
    "data": {
        "access": "eyJhbGciOiJIUzI1NiIs...",
        "refresh": "eyJhbGciOiJIUzI1NiIs...",
        "user_id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "is_superuser": true
    }
}
```

#### POST `/api/logout/`

**Request Body:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Success Response (205):**
```json
{
    "success": true,
    "return_code": "LOGOUT_SUCCESS",
    "message": "Logout successful.",
    "data": {
        "message": "Successfully logged out"
    }
}
```

---

### Portfolio Resource Endpoints

All portfolio resources follow the same CRUD pattern:

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/{resource}/` | List all items | ❌ No (Public) |
| `GET` | `/api/{resource}/{id}/` | Get single item | ❌ No (Public) |
| `POST` | `/api/{resource}/` | Create new item | ✅ Yes |
| `PUT` | `/api/{resource}/{id}/` | Update item | ✅ Yes |
| `DELETE` | `/api/{resource}/{id}/` | Delete item | ✅ Yes |

#### Available Resources

| Resource | Endpoint | Supports File Upload |
|---|---|---|
| **Profiles** | `/api/profiles/` | ✅ `profile_picture`, `resume` |
| **Skills** | `/api/skills/` | ❌ |
| **Experiences** | `/api/experiences/` | ✅ `logo` |
| **Projects** | `/api/projects/` | ✅ `image` |
| **Certifications** | `/api/certifications/` | ✅ `image`, `pdf_file` |
| **Education** | `/api/education/` | ❌ |
| **Contacts** | `/api/contacts/` | ❌ |
| **Contact Info** | `/api/contactinfo/` | ❌ |

> **Note:** The `Contacts` resource has special permissions — `POST` (submit a message) is open to **anyone**, while `GET`, `PUT`, and `DELETE` require **admin** privileges.

---

### Example: Skill CRUD

#### GET `/api/skills/` — List All Skills

**Response (200):**
```json
{
    "success": true,
    "return_code": "SKILL_RETRIEVED",
    "message": "Skills retrieved successfully.",
    "data": [
        {
            "id": 1,
            "name": "Python",
            "percentage": 90,
            "category": "LANG",
            "created_at": "2026-02-10T12:00:00Z",
            "modified_at": "2026-02-10T12:00:00Z"
        },
        {
            "id": 2,
            "name": "React",
            "percentage": 85,
            "category": "WEB",
            "created_at": "2026-02-10T12:05:00Z",
            "modified_at": "2026-02-10T12:05:00Z"
        }
    ]
}
```

#### POST `/api/skills/` — Create a Skill

**Request Body:**
```json
{
    "name": "Django",
    "percentage": 88,
    "category": "WEB"
}
```

**Response (201):**
```json
{
    "success": true,
    "return_code": "SKILL_CREATED",
    "message": "Skill created successfully.",
    "data": {
        "id": 3,
        "name": "Django",
        "percentage": 88,
        "category": "WEB",
        "created_at": "2026-02-18T14:30:00Z",
        "modified_at": "2026-02-18T14:30:00Z"
    }
}
```

#### PUT `/api/skills/3/` — Update a Skill

**Request Body (partial update supported):**
```json
{
    "percentage": 92
}
```

**Response (200):**
```json
{
    "success": true,
    "return_code": "SKILL_UPDATED",
    "message": "Skill updated successfully.",
    "data": {
        "id": 3,
        "name": "Django",
        "percentage": 92,
        "category": "WEB",
        "created_at": "2026-02-18T14:30:00Z",
        "modified_at": "2026-02-18T15:00:00Z"
    }
}
```

#### DELETE `/api/skills/3/` — Delete a Skill

**Response:** `204 No Content`

---

### Example: File Upload (Project)

#### POST `/api/projects/` — Create with Image

**Request:** `Content-Type: multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | ✅ | Project title |
| `description` | text | ✅ | Project description |
| `tech_stack` | string | ❌ | Comma-separated technologies |
| `github_link` | URL | ❌ | GitHub repository link |
| `live_url` | URL | ❌ | Live demo URL |
| `image` | file | ❌ | Project screenshot/image |

The image file is uploaded to **Cloudinary** automatically, and the returned `image` field contains the Cloudinary CDN URL.

---

## 🔐 Authentication

The API uses **JWT (JSON Web Token)** authentication via `djangorestframework-simplejwt`.

### How It Works

```
1. Login → POST /api/login/ with username & password
         ← Receive: { access: "...", refresh: "..." }

2. Authenticated Requests → Include header:
   Authorization: Bearer <access_token>

3. Token Refresh → When access token expires, use the refresh token
   (handled client-side)

4. Logout → POST /api/logout/ with { refresh: "..." }
          → Refresh token is blacklisted
```

### SafeJWT Authentication

The backend uses a **custom `SafeJWTAuthentication`** class that handles expired/invalid tokens gracefully:

- If a valid token is provided → user is authenticated.
- If an invalid/expired token is provided → request proceeds as **AnonymousUser** (no 401 error thrown).
- This allows public endpoints to remain accessible even when clients send stale tokens.

### Permission Levels

| Permission | Applies To | Description |
|---|---|---|
| `AllowAny` | Login, Contact POST | No authentication needed |
| `IsAuthenticatedOrReadOnly` | Most resources | Public can read; write requires auth |
| `IsAdminUser` | Contact GET/PUT/DELETE | Only admins can manage contact messages |

---

## 📦 Standardized API Responses

All API responses follow a consistent structure:

### Success Response

```json
{
    "success": true,
    "return_code": "RESOURCE_RETRIEVED",
    "message": "Human-readable success message.",
    "data": { ... }
}
```

### Error Response

```json
{
    "success": false,
    "return_code": "VALIDATION_ERROR",
    "message": "Human-readable error message.",
    "errors": { ... }
}
```

### Return Codes

| Category | Code | Message |
|---|---|---|
| **Auth** | `LOGIN_SUCCESS` | Login successful. |
| **Auth** | `LOGOUT_SUCCESS` | Logout successful. |
| **Auth** | `INVALID_CREDENTIALS` | Invalid email or password. |
| **Profile** | `PROFILE_RETRIEVED` / `CREATED` / `UPDATED` | Profile (action) successfully. |
| **Skill** | `SKILL_RETRIEVED` / `CREATED` / `UPDATED` | Skill(s) (action) successfully. |
| **Experience** | `EXPERIENCE_RETRIEVED` / `CREATED` / `UPDATED` | Experience (action) successfully. |
| **Project** | `PROJECT_RETRIEVED` / `CREATED` / `UPDATED` | Project(s) (action) successfully. |
| **Certification** | `CERTIFICATION_RETRIEVED` / `CREATED` / `UPDATED` | Certification(s) (action) successfully. |
| **Education** | `EDUCATION_RETRIEVED` / `CREATED` / `UPDATED` | Education (action) successfully. |
| **Contact** | `CONTACT_RETRIEVED` / `CREATED` / `UPDATED` | Contact (action) successfully. |
| **Error** | `VALIDATION_ERROR` | Validation failed. |

---

## ⚠️ Error Handling

The API handles errors at multiple levels:

| Layer | Strategy | Example |
|---|---|---|
| **Authentication** | `SafeJWTAuthentication` silently fails for invalid tokens | Stale token → AnonymousUser |
| **Validation** | Serializer validation with structured error responses | Missing required field → `VALIDATION_ERROR` |
| **Not Found** | `get_object_or_404()` returns 404 for missing resources | Invalid ID → `HTTP 404` |
| **Database** | `@transaction.atomic` ensures rollback on failures | Partial write → full rollback |
| **File Upload** | Cloudinary errors are caught and returned in response | Upload failure → error message |
| **Permissions** | DRF permission classes return 403/401 automatically | Unauthorized write → `HTTP 403` |

---

## 🔑 Environment Variables

Create a `.env` file in the `portpolio/` directory:

```env
# Django Core
SECRET_KEY=django-insecure-your-unique-secret-key
DEBUG=True

# Hosts & Security
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost

# CORS
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=http://localhost:5173

# JWT Configuration
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=1

# PostgreSQL Database
DB_NAME=portfolio_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
# DB_SSLMODE=require  # Enable for production

# Cloudinary (Media Storage)
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

---

## 💻 Local Setup

### Prerequisites

- Python 3.10+
- PostgreSQL 14+ (or a cloud-hosted instance)
- pip (latest)

### Steps

```bash
# 1. Navigate to backend
cd portpolio

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. (Optional) Load sample data
python load_data.py

# 8. Start development server
python manage.py runserver
```

The API will be available at: **`http://127.0.0.1:8000/api/`**

Django Admin Panel: **`http://127.0.0.1:8000/admin/`**

---

## 🚀 Production Deployment (Render)

### 1. Prepare the Repository

Ensure these files are in the root of your backend repo:
- `requirements.txt` — Python dependencies
- `build.sh` — Build script (runs pip install, collectstatic, migrate)
- `manage.py` — Django management command

### 2. Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/).
2. Click **New → Web Service**.
3. Connect your GitHub repository.
4. Configure:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn portfolio_backend.wsgi:application`
   - **Environment:** Python 3

### 3. Add Environment Variables

Add all variables from the [Environment Variables](#-environment-variables) section in Render's **Environment** tab. For production:

- Set `DEBUG=False`
- Set `ALLOWED_HOSTS` to include your Render domain
- Set `CORS_ALLOWED_ORIGINS` to include your Vercel frontend URL
- Set `DB_SSLMODE=require` for Render PostgreSQL

### 4. Create PostgreSQL Database

1. In Render, create a new **PostgreSQL** database.
2. Copy the connection details to your environment variables.

### Build Script (`build.sh`)

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

---

## 🔴 Live API Link

| Service | URL |
|---|---|
| **API Base URL** | [https://portfolio-web-app-backend.onrender.com/api/](https://portfolio-web-app-backend.onrender.com/api/)

### Quick Test

```bash
# Fetch all skills (public endpoint)
curl https://portfolio-web-app-backend.onrender.com/api/skills/

# Fetch all projects
curl https://portfolio-web-app-backend.onrender.com/api/projects/
```

---

## 📁 Folder Structure

```
portpolio/                           # Django Backend Root
│
├── api/                             # Main API application
│   ├── __init__.py
│   ├── admin.py                     # Django admin model registration
│   ├── apps.py                      # App configuration
│   ├── authentication.py            # SafeJWTAuthentication class
│   ├── models.py                    # 8 database models
│   ├── serializers.py               # DRF model serializers
│   ├── urls.py                      # API URL patterns (18 endpoints)
│   ├── views.py                     # Class-based API views (9 view classes)
│   ├── tests.py                     # Test module (placeholder)
│   ├── migrations/                  # Database migration files
│   └── util/                        # Utility modules
│       ├── responses.py             # APIResponse helper (standardized responses)
│       ├── cloudinary_util.py       # Cloudinary upload helper
│       └── base_serializer.py       # Base serializer with error formatting
│
├── portfolio_backend/               # Django Project Configuration
│   ├── __init__.py
│   ├── settings.py                  # Main settings (DB, CORS, JWT, Cloudinary)
│   ├── urls.py                      # Root URL configuration
│   ├── wsgi.py                      # WSGI application entry point
│   └── asgi.py                      # ASGI application entry point
│
├── media/                           # Local media directory (dev only)
├── manage.py                        # Django CLI management tool
├── requirements.txt                 # Python package dependencies
├── build.sh                         # Render deployment build script
├── load_data.py                     # Database seed script
├── db.sqlite3                       # Legacy SQLite database (deprecated)
├── .env                             # Environment variables (not in git)
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

---

<div align="center">

**Built with Django REST Framework** 🐍

</div>