# Traveloop — Full Project Documentation

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [Project Structure](#3-project-structure)
4. [Setup & Installation](#4-setup--installation)
5. [Configuration](#5-configuration)
6. [Database Models](#6-database-models)
7. [URL Routing](#7-url-routing)
8. [Views](#8-views)
9. [Forms](#9-forms)
10. [Authentication](#10-authentication)
11. [Admin Panel](#11-admin-panel)
12. [Templates](#12-templates)
13. [Static Files & CSS](#13-static-files--css)
14. [Context Processors](#14-context-processors)
15. [Management Commands](#15-management-commands)
16. [Deployment (Render)](#16-deployment-render)
17. [Feature Summary](#17-feature-summary)

---

## 1. Project Overview

**Traveloop** is a full-stack travel planning web application built with Django. It lets users:

- Create and manage personal trips with cover images
- Build detailed itineraries with city stops and activities
- Track budgets broken down by category
- Manage packing checklists
- Write and organize trip notes
- Share trips publicly via a UUID-based link
- Browse curated destinations and travel packages
- Book packages and view booking history
- Manage their user profile

The project is structured as a single Django app (`travel`) inside a project container (`traveloop`).

---

## 2. Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 · Django 5.0.14 |
| Database (local) | SQLite3 |
| Database (production) | PostgreSQL via `dj-database-url` |
| ORM | Django ORM |
| Authentication | Django built-in auth + custom email-as-username |
| Frontend | Django Templates · Tailwind CSS 3 · Custom CSS |
| CSS Build | Tailwind CLI via Node/npm |
| Static files | WhiteNoise |
| Image handling | Pillow |
| Web server | Gunicorn (production) |
| Hosting | Render |

### Python Dependencies (`requirements.txt`)

```
Django==5.0.14
dj-database-url==3.1.2
gunicorn==26.0.0
pillow==12.2.0
whitenoise==6.12.0
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2026.2
packaging==26.2
```

### Node Dependencies (`package.json`)

```json
{
  "devDependencies": {
    "tailwindcss": "^3.4.3",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.38"
  }
}
```

---

## 3. Project Structure

```
Hackathon_parul/
├── manage.py                    # Django management entry point
├── db.sqlite3                   # Local SQLite database
├── requirements.txt             # Python dependencies
├── package.json                 # Node/Tailwind dependencies
├── tailwind.config.js           # Tailwind CSS configuration
├── postcss.config.js            # PostCSS configuration
├── build.sh                     # Production build script (Render)
│
├── traveloop/                   # Django project config
│   ├── settings.py              # App settings, DB, email, static
│   ├── urls.py                  # Root URL dispatcher
│   ├── wsgi.py                  # WSGI entry point
│   └── asgi.py                  # ASGI entry point
│
├── travel/                      # Main application
│   ├── models.py                # All data models
│   ├── views.py                 # Main view functions
│   ├── views_auth.py            # Sign-up view
│   ├── urls.py                  # App URL patterns
│   ├── auth_urls.py             # Auth URL patterns
│   ├── forms.py                 # All Django forms
│   ├── admin.py                 # Admin registrations
│   ├── context_processors.py   # Template global context
│   ├── apps.py                  # App config
│   ├── migrations/              # Database migrations
│   └── management/
│       └── commands/
│           └── seed_demo.py     # Demo data seeder
│
├── templates/
│   ├── base.html                # Base layout
│   ├── includes/
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   ├── sidebar.html
│   │   └── messages.html
│   └── travel/
│       ├── home.html
│       ├── dashboard.html
│       ├── trip_form.html
│       ├── trip_detail.html
│       ├── my_trips.html
│       ├── itinerary_builder.html
│       ├── itinerary_timeline.html
│       ├── budget_breakdown.html
│       ├── packing_checklist.html
│       ├── notes.html
│       ├── note_edit.html
│       ├── profile.html
│       ├── public_itinerary.html
│       ├── destination_list.html
│       ├── destination_detail.html
│       ├── package_list.html
│       ├── book_package.html
│       ├── booking_confirmation.html
│       ├── my_bookings.html
│       ├── search.html
│       ├── city_search.html
│       ├── activity_search.html
│       ├── about.html
│       ├── contact.html
│       ├── testimonials.html
│       └── auth/
│           ├── login.html
│           ├── signup.html
│           ├── password_reset.html
│           ├── password_reset_done.html
│           ├── password_reset_confirm.html
│           ├── password_reset_complete.html
│           └── password_reset_email.txt
│
├── static/
│   ├── css/
│   │   ├── tailwind.css         # Compiled Tailwind output
│   │   └── custom.css           # Custom overrides
│   └── js/
│       ├── main.js
│       ├── booking.js
│       └── budget.js
│
├── static_src/
│   └── input.css                # Tailwind source input
│
└── media/
    └── trip_covers/             # User-uploaded trip images
```

---

## 4. Setup & Installation

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Git

### Local Development

```bash
# 1. Clone the repository
git clone <repo-url>
cd Hackathon_parul

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Node dependencies and build CSS
npm install
npm run build:css

# 5. Run migrations
python manage.py migrate

# 6. (Optional) Seed demo data
python manage.py seed_demo

# 7. Create a superuser for admin
python manage.py createsuperuser

# 8. Start the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

### CSS Watch Mode

During development, keep Tailwind watching for changes:

```bash
npm run watch:css
```

---

## 5. Configuration

### `traveloop/settings.py`

| Setting | Value / Behavior |
|---|---|
| `DEBUG` | `True` locally, `False` when `RENDER` env var is set |
| `SECRET_KEY` | Read from `SECRET_KEY` environment variable |
| `ALLOWED_HOSTS` | `127.0.0.1`, `localhost`, Render hostname |
| `DATABASE` | SQLite locally; PostgreSQL on Render via `DATABASE_URL` |
| `STATIC_ROOT` | `staticfiles/` — collected for production |
| `MEDIA_ROOT` | `media/` — uploaded files |
| `LOGIN_URL` | `/accounts/login/` |
| `LOGIN_REDIRECT_URL` | `/dashboard/` |
| `LOGOUT_REDIRECT_URL` | `/accounts/login/` |
| `EMAIL_BACKEND` | SMTP via Gmail |
| `EMAIL_HOST_USER` | From `EMAIL_HOST_USER` env var |
| `EMAIL_HOST_PASSWORD` | From `EMAIL_HOST_PASSWORD` env var |

### Required Environment Variables (Production)

```
SECRET_KEY=<django-secret-key>
RENDER=true
RENDER_EXTERNAL_HOSTNAME=<your-app>.onrender.com
DATABASE_URL=postgresql://...
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=<gmail-app-password>
```

---

## 6. Database Models

All models live in `travel/models.py`.

---

### `UserProfile`

Extends the built-in Django `User` with a one-to-one profile.

| Field | Type | Notes |
|---|---|---|
| `user` | OneToOneField → User | Cascade delete |
| `avatar` | ImageField | Uploaded to `avatars/` |
| `phone` | CharField(20) | Optional |
| `bio` | TextField | Optional |
| `preferred_travel_style` | CharField(80) | e.g. "backpacker", "luxury" |

---

### `Trip`

The core entity a user creates to plan a journey.

| Field | Type | Notes |
|---|---|---|
| `user` | ForeignKey → User | Owner |
| `title` | CharField(180) | |
| `description` | TextField | |
| `start_date` / `end_date` | DateField | |
| `cover_image` | ImageField | Uploaded to `trip_covers/` |
| `created_at` | DateTimeField | Auto |
| `public_slug` | UUIDField | Unique, auto-generated |
| `is_public` | BooleanField | Enables public sharing |

**Properties:**
- `total_budget` — returns budget total if a Budget object exists, else `0.00`
- `total_days` — `(end_date - start_date).days + 1`, minimum 1

---

### `CityStop`

A single city visit within a trip, ordered by the `order` field.

| Field | Type | Notes |
|---|---|---|
| `trip` | ForeignKey → Trip | |
| `city_name` | CharField(120) | |
| `country` | CharField(120) | |
| `arrival_date` / `departure_date` | DateField | |
| `order` | PositiveIntegerField | Unique per trip |

**Meta:** `unique_together = ("trip", "order")`

---

### `Activity`

An activity attached to a city stop.

| Field | Type | Notes |
|---|---|---|
| `city_stop` | ForeignKey → CityStop | |
| `title` | CharField(150) | |
| `category` | CharField | Choices: sightseeing, food, adventure, culture, shopping, other |
| `description` | TextField | Optional |
| `cost` | DecimalField | In INR, min 0 |
| `duration_hours` | DecimalField | Min 0, step 0.5 |
| `activity_date` | DateField | |

---

### `Budget`

One-to-one budget record per trip, split by category.

| Field | Type |
|---|---|
| `transport_cost` | DecimalField |
| `hotel_cost` | DecimalField |
| `food_cost` | DecimalField |
| `activity_cost` | DecimalField |
| `miscellaneous_cost` | DecimalField |

**Property:** `total_cost` — sum of all five fields.

---

### `PackingItem`

A checklist item for a trip.

| Field | Type | Notes |
|---|---|---|
| `trip` | ForeignKey → Trip | |
| `item_name` | CharField(120) | |
| `category` | CharField | Choices: documents, clothing, electronics, toiletries, medicine, other |
| `is_packed` | BooleanField | Default False |

---

### `Note`

A freeform note attached to a trip.

| Field | Type |
|---|---|
| `trip` | ForeignKey → Trip |
| `title` | CharField(150) |
| `content` | TextField |
| `created_at` | DateTimeField (auto) |

---

### `Destination`

A curated travel destination shown on the public site.

| Field | Type | Notes |
|---|---|---|
| `name` | CharField(120) | |
| `slug` | SlugField | Unique |
| `country` | CharField(80) | |
| `short_description` | CharField(255) | |
| `description` | TextField | |
| `image_url` | URLField | Unsplash URL |
| `featured` | BooleanField | Shows on homepage |

---

### `Package`

A bookable travel package linked to a destination.

| Field | Type | Notes |
|---|---|---|
| `destination` | ForeignKey → Destination | |
| `name` | CharField(180) | |
| `slug` | SlugField | |
| `headline` | CharField(255) | |
| `description` | TextField | |
| `duration_days` | PositiveSmallIntegerField | |
| `price_per_person` | DecimalField | |
| `max_travelers` | PositiveSmallIntegerField | Default 8 |
| `image_url` | URLField | |
| `featured` | BooleanField | |

---

### `Booking`

Records a user booking a package.

| Field | Type |
|---|---|
| `user` | ForeignKey → User |
| `package` | ForeignKey → Package |
| `travel_date` | DateField |
| `travelers_count` | PositiveSmallIntegerField |
| `total_price` | DecimalField |
| `status` | CharField (default: `"confirmed"`) |
| `booked_at` | DateTimeField (auto) |

---

### `Testimonial`

Customer review shown on the public homepage.

| Field | Type |
|---|---|
| `name` | CharField(120) |
| `role` | CharField(120) |
| `quote` | TextField |
| `rating` | PositiveSmallIntegerField (1–5) |
| `avatar_url` | URLField |
| `featured` | BooleanField |

**Property:** `star_range` — returns `range(self.rating)` for template star loops.

---

### `NewsletterSubscriber`

Stores newsletter email signups.

| Field | Type |
|---|---|
| `email` | EmailField (unique) |
| `active` | BooleanField |
| `subscribed_at` | DateTimeField (auto) |

---

## 7. URL Routing

### Root URLs (`traveloop/urls.py`)

| Prefix | Includes |
|---|---|
| `admin/` | Django admin |
| `accounts/` | `travel.auth_urls` |
| `` (empty) | `travel.urls` |

Media files are served via Django only in `DEBUG` mode.

---

### Auth URLs (`travel/auth_urls.py`) — prefix: `/accounts/`

| URL | View | Name |
|---|---|---|
| `signup/` | `views_auth.sign_up` | `signup` |
| `login/` | Django `LoginView` | `login` |
| `logout/` | Django `LogoutView` | `logout` |
| `password-reset/` | Django `PasswordResetView` | `password_reset` |
| `password-reset/done/` | Django `PasswordResetDoneView` | `password_reset_done` |
| `reset/<uidb64>/<token>/` | Django `PasswordResetConfirmView` | `password_reset_confirm` |
| `reset/done/` | Django `PasswordResetCompleteView` | `password_reset_complete` |

---

### App URLs (`travel/urls.py`) — namespace: `travel`

| URL Pattern | View | Name |
|---|---|---|
| `` | `home` | `home` |
| `destinations/` | `destination_list` | `destination_list` |
| `packages/` | `package_list` | `package_list` |
| `dashboard/` | `dashboard` | `dashboard` |
| `trips/create/` | `trip_create` | `trip_create` |
| `trips/` | `trip_list` | `my_trips` |
| `trips/<id>/` | `trip_detail` | `trip_detail` |
| `trips/<id>/edit/` | `trip_edit` | `trip_edit` |
| `trips/<id>/delete/` | `trip_delete` | `trip_delete` |
| `trips/<id>/itinerary/` | `itinerary_builder` | `itinerary_builder` |
| `trips/<id>/city-stop/<stop_id>/<direction>/` | `city_stop_move` | `city_stop_move` |
| `trips/<id>/timeline/` | `itinerary_timeline` | `itinerary_timeline` |
| `city-search/` | `city_search` | `city_search` |
| `activity-search/` | `activity_search` | `activity_search` |
| `trips/<id>/budget/` | `budget_breakdown` | `budget_breakdown` |
| `trips/<id>/packing/` | `packing_checklist` | `packing_checklist` |
| `trips/<id>/packing/<item_id>/toggle/` | `packing_toggle` | `packing_toggle` |
| `trips/<id>/packing/<item_id>/delete/` | `packing_delete` | `packing_delete` |
| `trips/<id>/notes/` | `notes_page` | `notes_page` |
| `trips/<id>/notes/<note_id>/edit/` | `note_edit` | `note_edit` |
| `trips/<id>/notes/<note_id>/delete/` | `note_delete` | `note_delete` |
| `profile/` | `profile_page` | `profile` |
| `share/<uuid:slug>/` | `public_itinerary` | `public_itinerary` |

---

## 8. Views

All views are in `travel/views.py` unless noted.

### Public Views

| View | Description |
|---|---|
| `home` | Landing page with featured destinations, packages, stats, and search form |
| `destination_list` | Lists all `Destination` objects |
| `package_list` | Lists all `Package` objects |
| `public_itinerary` | Publicly shareable trip view by UUID slug (no login required) |

### Protected Views (require `@login_required`)

#### Dashboard

- **`dashboard`** — shows trip count, city count, activity count, total budget, upcoming trips, recent trips, and recent activities.

#### Trip Management

| View | HTTP Methods | Description |
|---|---|---|
| `trip_create` | GET, POST | Creates a new trip; auto-creates a linked `Budget` |
| `trip_list` | GET | Lists all user trips |
| `trip_detail` | GET | Shows trip overview, city stops, and latest notes |
| `trip_edit` | GET, POST | Edits an existing trip |
| `trip_delete` | POST only | Deletes a trip and redirects |

#### Itinerary Building

| View | Description |
|---|---|
| `itinerary_builder` | Displays and handles two sub-forms: add city stop (`action=add_city`) and add activity (`action=add_activity`) |
| `city_stop_move` | Swaps `order` values of adjacent city stops (direction: `up` or `down`) |
| `itinerary_timeline` | Groups all activities by `activity_date` into a `day_map` dict for timeline rendering |

#### Search

| View | Description |
|---|---|
| `city_search` | Filters city stops by keyword, arrival/departure dates |
| `activity_search` | Filters activities by title, description, category, and dates |

#### Budget

- **`budget_breakdown`** — GET/POST to update budget fields; passes chart data (labels + values) for a JS chart.

#### Packing Checklist

| View | Method | Description |
|---|---|---|
| `packing_checklist` | GET, POST | List and add packing items; supports `?category=` filter |
| `packing_toggle` | POST | Toggles `is_packed` on a single item |
| `packing_delete` | POST | Deletes a packing item |

#### Notes

| View | Method | Description |
|---|---|---|
| `notes_page` | GET, POST | List and create notes |
| `note_edit` | GET, POST | Edit a note |
| `note_delete` | POST | Delete a note |

#### Profile

- **`profile_page`** — GET/POST; updates both `User` fields (name, email) and `UserProfile` fields (avatar, phone, bio, travel style).

---

## 9. Forms

All forms are in `travel/forms.py`.

| Form | Model/Base | Key Fields |
|---|---|---|
| `StyledLoginForm` | `AuthenticationForm` | Email-labeled username field with Bootstrap classes |
| `SignUpForm` | `UserCreationForm` | email (as username), first/last name, password; email uniqueness check |
| `TripForm` | `Trip` | title, description, dates, cover image, is_public; end ≥ start validation |
| `CityStopForm` | `CityStop` | city, country, arrival/departure dates, order; departure ≥ arrival validation |
| `ActivityForm` | `Activity` | city_stop (filtered per trip), title, category, description, cost, duration, date |
| `BudgetForm` | `Budget` | transport, hotel, food, activity, miscellaneous costs |
| `PackingItemForm` | `PackingItem` | item_name, category |
| `NoteForm` | `Note` | title, content |
| `ProfileForm` | `UserProfile` | avatar, phone, bio, travel style + user first/last name, email (via `user=` kwarg) |
| `SearchForm` | `Form` | keyword `q`, start date, end date; end ≥ start validation |

All form widgets apply `form-control` CSS class for consistent Bootstrap/Tailwind styling.

---

## 10. Authentication

### Login

- URL: `/accounts/login/`
- Uses Django's built-in `LoginView` with `StyledLoginForm`
- Users log in with **email** (stored as username)
- Redirects authenticated users to `/dashboard/`

### Sign Up (`/accounts/signup/`)

- Custom `sign_up` view in `views_auth.py`
- Uses `SignUpForm` which sets `username = email`
- Auto-creates a `UserProfile` on successful registration
- Logs the user in immediately after registration
- Redirects to `/dashboard/`

### Logout

- URL: `/accounts/logout/`
- Redirects to `/accounts/login/`

### Password Reset

Full Django password reset flow:

1. `/accounts/password-reset/` — enter email
2. `/accounts/password-reset/done/` — email sent confirmation
3. `/accounts/reset/<uidb64>/<token>/` — set new password
4. `/accounts/reset/done/` — success page

Email is sent via Gmail SMTP using environment variable credentials.

---

## 11. Admin Panel

Admin is available at `/admin/` and branded as **Traveloop Admin**.

### Registered Models

| Model | List Display | Filters / Search |
|---|---|---|
| `User` | (default + inline profile) | Built-in |
| `UserProfile` | user, phone, travel style | Search by username, phone |
| `Trip` | title, user, dates, is_public | Filter by public/date; search title |
| `CityStop` | city, country, trip, dates, order | Filter by country; search city |
| `Activity` | title, city, category, cost, date | Filter by category/date; search title |
| `Budget` | trip, all 5 cost fields | — |
| `PackingItem` | item, trip, category, is_packed | Filter by category/packed |
| `Note` | title, trip, created_at | Search title; ordered by newest |

`UserProfile` appears as a stacked inline inside the `User` admin page.

---

## 12. Templates

### Layout

- `base.html` — master layout; includes navbar, messages, sidebar, footer
- `includes/navbar.html` — navigation bar (uses `nav_recent_trips` from context processor)
- `includes/sidebar.html` — sidebar navigation
- `includes/footer.html` — footer
- `includes/messages.html` — Django flash message display

### Page Templates (`templates/travel/`)

| Template | Purpose |
|---|---|
| `home.html` | Landing page — hero, stats, featured destinations/packages |
| `dashboard.html` | User dashboard — stats, upcoming/recent trips |
| `trip_form.html` | Create/edit trip (shared by both) |
| `trip_detail.html` | Full trip overview with city stops |
| `my_trips.html` | User's trip list |
| `itinerary_builder.html` | Add/reorder city stops and activities |
| `itinerary_timeline.html` | Day-by-day activity timeline view |
| `budget_breakdown.html` | Budget form + chart visualization |
| `packing_checklist.html` | Packing list with toggle/delete |
| `notes.html` | Note listing and creation |
| `note_edit.html` | Edit a single note |
| `profile.html` | User profile edit page |
| `public_itinerary.html` | Read-only public trip view |
| `destination_list.html` | All destinations |
| `destination_detail.html` | Single destination detail |
| `package_list.html` | All packages |
| `book_package.html` | Package booking form |
| `booking_confirmation.html` | Post-booking confirmation |
| `my_bookings.html` | User's booking history |
| `city_search.html` | City stop search results |
| `activity_search.html` | Activity search results |
| `search.html` | General search |
| `about.html` | About page |
| `contact.html` | Contact page |
| `testimonials.html` | Testimonials listing |
| `auth/login.html` | Login form |
| `auth/signup.html` | Sign-up form |
| `auth/password_reset*.html` | Full password reset flow |

---

## 13. Static Files & CSS

### Structure

```
static/
├── css/
│   ├── tailwind.css     # Compiled Tailwind output (generated, do not edit)
│   └── custom.css       # Custom styles layered on top
└── js/
    ├── main.js          # General JS utilities
    ├── booking.js       # Booking form interactions
    └── budget.js        # Budget chart rendering
```

### Tailwind Build

The source input is `static_src/input.css`. The compiled output goes to `static/css/tailwind.css`.

```bash
# One-time build
npm run build:css

# Watch mode (development)
npm run watch:css
```

Configuration is in `tailwind.config.js` and `postcss.config.js`.

In production, WhiteNoise serves static files with `CompressedManifestStaticFilesStorage`:

```bash
python manage.py collectstatic
```

---

## 14. Context Processors

`travel/context_processors.py` — `travel_globals`

Injects `nav_recent_trips` into every template context. For authenticated users, this is the 4 most recently created trips — used to populate quick-links in the navbar.

Registered in `settings.py` under `TEMPLATES > OPTIONS > context_processors`.

---

## 15. Management Commands

### `seed_demo`

```bash
python manage.py seed_demo
```

Creates a complete set of demo data (safe to run multiple times — uses `get_or_create` / `update_or_create`):

- **Demo user:** `traveler_demo` / `demo12345` (email: `demo@traveloop.com`)
- **4 Destinations:** Santorini, Kyoto, Swiss Alps, Banff National Park
- **5 Packages:** spread across the destinations with realistic pricing
- **1 Demo booking** for the demo user on the first package
- **3 Testimonials** with avatar URLs
- **1 Newsletter subscriber** seed entry

---

## 16. Deployment (Render)

### `build.sh`

The `build.sh` script is the Render build command. It typically handles:

```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

### Environment Variables (set in Render dashboard)

```
SECRET_KEY=<strong-random-key>
RENDER=true
RENDER_EXTERNAL_HOSTNAME=<your-app>.onrender.com
DATABASE_URL=postgresql://<user>:<pass>@<host>/<db>
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=<16-char-gmail-app-password>
```

### Database

- Locally: SQLite (`db.sqlite3`)
- On Render: PostgreSQL via `DATABASE_URL`, with `ssl_require=True` enforced

### Static Files

WhiteNoise serves static files directly from Django — no separate CDN needed. `collectstatic` aggregates files to `staticfiles/`.

### Media Files

User-uploaded media (`trip_covers/`, `avatars/`) is stored in `media/`. On Render's free tier, the filesystem is ephemeral — for persistent media storage, integrate a cloud bucket (e.g., AWS S3 or Cloudinary).

---

## 17. Feature Summary

| Feature | Status |
|---|---|
| Email-based sign up & login | ✅ |
| Password reset via email | ✅ |
| User profile (avatar, bio, travel style) | ✅ |
| Trip CRUD with cover image | ✅ |
| Multi-city itinerary builder | ✅ |
| City stop reordering (up/down) | ✅ |
| Activity tracking per city | ✅ |
| Day-by-day timeline view | ✅ |
| Budget breakdown with chart | ✅ |
| Packing checklist with toggle | ✅ |
| Trip notes (create, edit, delete) | ✅ |
| Public trip sharing via UUID link | ✅ |
| Destination catalog | ✅ |
| Package catalog | ✅ |
| Package booking | ✅ |
| Testimonials | ✅ |
| Newsletter subscriber model | ✅ |
| City & activity search | ✅ |
| Dashboard with stats | ✅ |
| Django admin panel | ✅ |
| Demo data seeder command | ✅ |
| Tailwind CSS frontend | ✅ |
| WhiteNoise static file serving | ✅ |
| Render deployment ready | ✅ |
| PostgreSQL production database | ✅ |
