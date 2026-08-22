# ✈️ Traveloop

> A full-stack travel planning web app built with Django. Plan trips, build itineraries, track budgets, manage packing lists, and book curated travel packages — all in one place.

🌐 **Live Demo:** [https://traveloop-1-8f1k.onrender.com](https://traveloop-1-8f1k.onrender.com)

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.0.14-green?logo=django)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38bdf8?logo=tailwindcss)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📸 Features

- 🔐 **Auth** — Email-based signup, login, and full password reset via email
- 🗺️ **Trip Planning** — Create trips with title, dates, and cover image
- 🏙️ **Itinerary Builder** — Add multi-city stops with ordered drag-like reordering
- 📅 **Timeline View** — Day-by-day activity timeline for each trip
- 💰 **Budget Tracker** — Breakdown by transport, hotel, food, activities, and misc with a chart
- 🎒 **Packing Checklist** — Add items by category, check them off as you pack
- 📝 **Trip Notes** — Write, edit, and delete freeform notes per trip
- 🔗 **Public Sharing** — Share any trip via an unguessable UUID link (no login needed)
- 🌍 **Destinations** — Browse curated destination catalog
- 📦 **Packages** — Browse and book travel packages
- 👤 **Profile** — Edit avatar, bio, phone, and travel style
- 🔍 **Search** — Search your cities and activities by keyword and date range
- 🛠️ **Admin Panel** — Full Django admin at `/admin/`

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 · Django 5.0.14 |
| Database (dev) | SQLite |
| Database (prod) | PostgreSQL |
| Frontend | Django Templates · Tailwind CSS 3 |
| CSS Build | Tailwind CLI (Node.js) |
| Static Files | WhiteNoise |
| Image Handling | Pillow |
| Web Server | Gunicorn |
| Hosting | Render.com |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Git

> **Just want to try it?** Visit the live app:
> 👉 [https://traveloop-1-8f1k.onrender.com](https://traveloop-1-8f1k.onrender.com)
>
> Demo login: `traveler_demo` / `demo12345`

### 1. Clone the repository

```bash
git clone https://github.com/your-username/traveloop.git
cd traveloop
```

### 2. Set up a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Node dependencies and build CSS

```bash
npm install
npm run build:css
```

### 5. Set environment variables

Create a `.env` file or set these in your shell:

```env
SECRET_KEY=your-django-secret-key
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

> For local dev, `SECRET_KEY` can be any random string. Email settings are only required for password reset.

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. (Optional) Seed demo data

```bash
python manage.py seed_demo
```

This creates a demo user, 4 destinations, 5 packages, testimonials, and a sample booking.

> Demo login: `traveler_demo` / `demo12345`
> Or try the live app directly: [https://traveloop-1-8f1k.onrender.com](https://traveloop-1-8f1k.onrender.com)

### 8. Create a superuser for admin

```bash
python manage.py createsuperuser
```

### 9. Start the development server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000**

---

## 📁 Project Structure

```
traveloop/
├── manage.py                    # Django CLI entry point
├── requirements.txt             # Python dependencies
├── package.json                 # Node/Tailwind dependencies
├── tailwind.config.js           # Tailwind configuration
├── build.sh                     # Render.com deploy script
│
├── traveloop/                   # Django project config
│   ├── settings.py              # All settings (DB, email, static, auth)
│   ├── urls.py                  # Root URL router
│   ├── wsgi.py                  # Production server entry point
│   └── asgi.py                  # Async server entry point
│
├── travel/                      # Main application
│   ├── models.py                # 12 database models
│   ├── views.py                 # 24 view functions
│   ├── views_auth.py            # Sign-up view
│   ├── urls.py                  # App URL patterns
│   ├── auth_urls.py             # Auth URL patterns
│   ├── forms.py                 # 10 form classes
│   ├── admin.py                 # Admin panel config
│   ├── context_processors.py   # Global template context
│   ├── migrations/              # Database schema history
│   └── management/commands/
│       └── seed_demo.py         # Demo data seeder
│
├── templates/                   # All HTML templates
│   ├── base.html                # Master layout
│   ├── includes/                # Navbar, footer, sidebar, messages
│   └── travel/                  # 25 page templates + 7 auth templates
│
├── static/
│   ├── css/tailwind.css         # Compiled CSS (auto-generated)
│   ├── css/custom.css           # Custom styles
│   └── js/                      # main.js, budget.js, booking.js
│
├── static_src/input.css         # Tailwind source — edit this
└── media/trip_covers/           # User-uploaded images
```

---

## 🎨 CSS Development

During development, keep Tailwind watching for changes:

```bash
npm run watch:css
```

To build once for production:

```bash
npm run build:css
```

---

## 🗄️ Database Models

| Model | Description |
|---|---|
| `UserProfile` | Extended user profile (avatar, bio, travel style) |
| `Trip` | A user's trip with dates and cover image |
| `CityStop` | A city visit within a trip, ordered |
| `Activity` | An activity in a city (category, cost, duration) |
| `Budget` | Per-trip budget split across 5 categories |
| `PackingItem` | Checklist item per trip |
| `Note` | Freeform note per trip |
| `Destination` | Curated public destination |
| `Package` | Bookable travel package |
| `Booking` | User's package booking record |
| `Testimonial` | Customer review |
| `NewsletterSubscriber` | Newsletter email record |

---

## 🔑 URL Overview

| URL | Description |
|---|---|
| `/` | Landing page |
| `/accounts/signup/` | Register |
| `/accounts/login/` | Login |
| `/dashboard/` | User dashboard |
| `/trips/` | All trips |
| `/trips/create/` | New trip |
| `/trips/<id>/itinerary/` | Itinerary builder |
| `/trips/<id>/timeline/` | Day-by-day timeline |
| `/trips/<id>/budget/` | Budget breakdown |
| `/trips/<id>/packing/` | Packing checklist |
| `/trips/<id>/notes/` | Trip notes |
| `/share/<uuid>/` | Public trip share link |
| `/destinations/` | Destination catalog |
| `/packages/` | Package catalog |
| `/profile/` | Edit profile |
| `/admin/` | Django admin panel |

---

## ☁️ Deploying to Render

### Environment Variables (set in Render dashboard)

```
SECRET_KEY=<strong-random-key>
RENDER=true
RENDER_EXTERNAL_HOSTNAME=traveloop-1-8f1k.onrender.com
DATABASE_URL=postgresql://user:pass@host/dbname
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Build Command

```bash
./build.sh
```

The `build.sh` script runs `pip install`, `collectstatic`, and `migrate` automatically on every deploy.

### Notes
- Static files are served by **WhiteNoise** — no CDN needed
- Media uploads (`trip_covers/`, `avatars/`) are ephemeral on Render's free tier. For persistent storage, integrate **AWS S3** or **Cloudinary**
- PostgreSQL with `ssl_require=True` is enforced in production

---

## 📧 Email Setup (Password Reset)

The app uses Gmail SMTP. To enable:

1. Enable 2-Factor Authentication on your Google account
2. Generate an **App Password** at `myaccount.google.com/apppasswords`
3. Set `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in your environment

---

## 🧪 Admin Panel

Access at `/admin/` after creating a superuser.

Registered models with search, filter, and list display:
- Users (with inline profile)
- Trips, CityStops, Activities
- Budgets, PackingItems, Notes
- Destinations, Packages, Bookings
- Testimonials, NewsletterSubscribers

Admin branding: **Traveloop Admin**

---

## 🌱 Seed Demo Data

```bash
python manage.py seed_demo
```

Creates:
- **Demo user:** `traveler_demo` / `demo12345`
- **4 Destinations:** Santorini, Kyoto, Swiss Alps, Banff
- **5 Packages** with real pricing and Unsplash images
- **3 Testimonials** with avatars
- **1 Sample booking** for the demo user

Safe to run multiple times — uses `get_or_create` throughout.

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

## 🙌 Built With

- [Django](https://www.djangoproject.com/) — The web framework for perfectionists with deadlines
- [Tailwind CSS](https://tailwindcss.com/) — Utility-first CSS framework
- [WhiteNoise](https://whitenoise.readthedocs.io/) — Simplified static file serving
- [Pillow](https://pillow.readthedocs.io/) — Image processing
- [Gunicorn](https://gunicorn.org/) — Python WSGI HTTP Server
- [Render](https://render.com/) — Cloud hosting platform
