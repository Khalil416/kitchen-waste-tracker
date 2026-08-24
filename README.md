# 🍳 Kitchen Waste Tracker

A full-stack desktop application for tracking kitchen inventory, monitoring food expiry dates, recording waste, and analyzing financial loss — built with **Python**, **Flet**, **FastAPI**, and **SQLite**.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-Desktop_UI-02569B?logo=flutter&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 About

Kitchen Waste Tracker helps kitchen managers monitor inventory levels, track expiration dates, record food waste with cost estimates, and generate analytics reports. The application follows a **client-server architecture** where a Flet desktop frontend communicates with a FastAPI backend through RESTful HTTP endpoints.

This project was developed as a coursework for the **Software Engineering** course at Azerbaijan State Oil and Industry University (ASOIU).

---

## ✨ Features

### Inventory Management
- Full CRUD operations for inventory items (add, view, edit, delete)
- Auto-generated SKU codes (SKU-00001, SKU-00002, ...)
- Category-based organization (Dairy, Meat, Vegetable, Fruit, Dry Goods, Bakery)
- Storage location tracking (Fridge, Freezer, Pantry, Cold Room, Shelf, Counter)
- Search and multi-filter support (by name, category, status, storage)
- Pagination (6 items per page)

### Expiry Monitoring
- Real-time status calculation: **Fresh**, **Expiring Soon**, **Expired**
- Configurable alert threshold (1–14 days via slider)
- Dedicated Expiry Monitor page with tabbed view (Near Expiry / Expired / All)

### Waste Recording
- Transactional waste logging — inventory quantity is automatically reduced
- Predefined waste reasons: Expired, Spoiled, Prep Waste, Overproduction, Damaged, Other
- Cost estimation per waste entry
- Stock validation prevents wasting more than available quantity

### Analytics & Reports
- **Dashboard** — 4 summary cards (total items, near expiry, expired, weekly waste cost), waste distribution bar chart, daily trend line chart, expiring items table, recent waste logs
- **Reports page** — Waste Cost Trend chart, Waste by Reason breakdown, Top Wasted Items by Cost
- Period filtering: Daily (7 days), Weekly (4 weeks), Monthly (12 months)
- CSV export for waste reports

### User Management
- Role-based access control with 3 roles:
  - **Chef (Kitchen Staff)** — Dashboard, Inventory
  - **Inventory Manager** — above + Expiry Monitor, Waste Logs
  - **General Manager** — full access including Reports, Categories, Users, waste recording
- User CRUD (create, edit, activate/deactivate, delete)
- Manager hierarchy protection (head manager account cannot be modified)
- Session-based authentication

### UI/UX
- Light / Dark theme toggle on every page
- Responsive sidebar navigation with role-based menu items
- Snackbar notifications for success/error feedback
- Confirmation dialogs for destructive actions
- Pre-filled edit forms for seamless editing experience

---

## 🏗️ Architecture

```
┌─────────────────────┐          HTTP (REST)          ┌─────────────────────┐
│                     │  ◄──── requests library ────► │                     │
│   Flet Desktop UI   │         GET/POST/PUT/         │   FastAPI Backend   │
│   (main.py)         │         PATCH/DELETE           │   (api.py)          │
│                     │                                │                     │
└─────────────────────┘                                └──────────┬──────────┘
                                                                  │
                                                           sqlite3 module
                                                                  │
                                                    ┌─────────────┴─────────────┐
                                                    │                           │
                                              ┌─────┴─────┐             ┌───────┴───────┐
                                              │inventory.db│             │   reg.db      │
                                              │            │             │               │
                                              │• inventory │             │• users        │
                                              │• waste_logs│             │               │
                                              │• categories│             │               │
                                              └────────────┘             └───────────────┘
```

Both database files are created automatically on first launch and are **not** tracked in this repository.

---

## 📁 Project Structure

```
kitchen-waste-tracker/
├── api.py                          # FastAPI app entry point
├── main.py                         # Flet app entry point
│
├── backend/
│   ├── __init__.py
│   ├── db.py                       # Database connection helpers & logging
│   ├── common/
│   │   └── helpers.py              # Shared business logic (SKU generation, status calc)
│   ├── schemas/
│   │   └── core.py                 # Pydantic models for request validation
│   └── routers/
│       ├── health.py               # Health check & root endpoints
│       ├── auth.py                 # POST /auth/login
│       ├── inventory.py            # CRUD for /inventory
│       ├── waste.py                # CRUD for /waste-logs
│       ├── users.py                # CRUD for /users
│       ├── categories.py           # CRUD for /categories
│       └── analytics.py            # Dashboard stats & report aggregations
│
├── views/
│   ├── login.py                    # Login page + DB initialization & migration
│   ├── dashboard.py                # Main dashboard with charts & summary cards
│   ├── inventory.py                # Inventory list with filters & pagination
│   ├── add_item.py                 # Add / Edit inventory item form
│   ├── item_detail.py              # Single item detail with stock management
│   ├── expiry_monitor.py           # Expiry tracking with threshold slider
│   ├── waste_logs.py               # Waste audit trail with date filtering
│   ├── waste_new.py                # Record new waste form
│   ├── reports.py                  # Analytics charts & CSV export
│   ├── categories.py               # Category management CRUD
│   ├── users_staff.py              # User management grid
│   ├── registration.py             # New user registration form
│   └── account.py                  # User profile page (read-only)
│
├── tools/
│   ├── check_users.py              # CLI utility to inspect users table
│   └── migrate_passwords.py        # One-off migration: plaintext → PBKDF2 hashes
│
├── reports/                        # Auto-created folder for CSV exports
├── requirements.txt
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Khalil416/kitchen-waste-tracker.git
   cd kitchen-waste-tracker
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

You need **two terminals**. On a fresh clone, start the desktop app **first** — it creates the SQLite databases and tables on launch. Starting the API against a non-existent database will return `no such table: users`.

**Terminal 1 — Start the Flet desktop app (initializes the database):**
```bash
python main.py
```

**Terminal 2 — Start the API server:**
```bash
uvicorn api:app --reload --port 8000
```

> **First run:** the database files are not tracked in this repository, so a fresh clone starts empty. Create your first account through the registration screen on launch.

### Demo Accounts

These accounts exist only if you have an existing local database from a previous run. On a fresh clone, register a new account instead.

| Username         | Role              |
|------------------|-------------------|
| `manager`        | General Manager   |
| `inventory1`     | Inventory Manager |
| `chef1`          | Kitchen Staff     |

### API Documentation

Once the backend is running, interactive API docs are available at:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🛠️ Tech Stack

| Layer     | Technology             | Purpose                                    |
|-----------|------------------------|--------------------------------------------|
| Frontend  | Flet                   | Desktop UI framework (Python-based)        |
| Backend   | FastAPI                | RESTful API server with auto-docs          |
| Database  | SQLite3                | Lightweight embedded relational database   |
| Charting  | flet_charts            | Line charts for dashboard trends           |
| HTTP      | requests               | Frontend-to-backend communication          |
| Validation| Pydantic               | Request body schema validation             |
| Security  | hashlib (PBKDF2)       | Password hashing with per-user salts       |
| Server    | Uvicorn                | ASGI server for FastAPI                    |

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint           | Description        |
|--------|--------------------|--------------------|
| POST   | `/auth/login`      | User login         |

### Inventory
| Method | Endpoint               | Description                          |
|--------|------------------------|--------------------------------------|
| GET    | `/inventory`           | List items (with search & filters)   |
| GET    | `/inventory/{id}`      | Get single item                      |
| POST   | `/inventory`           | Create new item                      |
| PUT    | `/inventory/{id}`      | Update item                          |
| DELETE | `/inventory/{id}`      | Delete item                          |

### Waste Logs
| Method | Endpoint         | Description                              |
|--------|------------------|------------------------------------------|
| GET    | `/waste-logs`    | List waste logs (optional item_id filter) |
| POST   | `/waste-logs`    | Record waste (transactional)             |

### Users
| Method | Endpoint                    | Description              |
|--------|-----------------------------|--------------------------|
| GET    | `/users`                    | List users (search/role) |
| GET    | `/users/{id}`               | Get single user          |
| POST   | `/users`                    | Create user              |
| PUT    | `/users/{id}`               | Update user              |
| PATCH  | `/users/{id}/active`        | Toggle active status     |
| DELETE | `/users/{id}`               | Delete user              |

Password fields are never included in user responses.

### Categories
| Method | Endpoint              | Description        |
|--------|-----------------------|--------------------|
| GET    | `/categories`         | List categories    |
| POST   | `/categories`         | Create category    |
| PUT    | `/categories/{id}`    | Update category    |
| DELETE | `/categories/{id}`    | Delete category    |

### Analytics
| Method | Endpoint                  | Description                        |
|--------|---------------------------|------------------------------------|
| GET    | `/dashboard/stats`        | Summary cards data                 |
| GET    | `/dashboard/waste-summary`| Waste distribution by reason       |
| GET    | `/reports/summary`        | Waste cost trend (period filter)   |
| GET    | `/reports/by-reason`      | Top waste reasons (period filter)  |

### System
| Method | Endpoint    | Description            |
|--------|-------------|------------------------|
| GET    | `/`         | API welcome message    |
| GET    | `/health`   | Health check           |

---

## 🔒 Security Notes

This is a **university coursework project**. Security posture:

**Implemented:**
- Passwords are hashed at rest using **PBKDF2-HMAC-SHA256** (200,000 iterations) with a unique per-user salt — no plaintext credentials are stored
- The `GET /users` and `GET /users/{id}` endpoints never return password data
- Login is verified by re-deriving the hash from the submitted password, not by comparison of stored secrets

**Known simplifications (not production-ready):**
- No JWT or token-based authentication (session-based via Flet's `page.session`, no expiry)
- No HTTPS (runs on localhost only)
- Role-based access is enforced on the **frontend routing layer** — the API does not verify roles per request
- SQLite is used for simplicity — production would use PostgreSQL or similar
- No automated test suite

---

## 👤 Author

**Khalil Allahverdiyev**

- GitHub: [@Khalil416](https://github.com/Khalil416)
- LinkedIn: [khalil-allahverdiyev](https://linkedin.com/in/khalil-allahverdiyev)
- Email: xelil.allahverdiyev06@gmail.com
