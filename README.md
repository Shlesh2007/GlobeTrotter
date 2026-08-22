# ✈️ GlobeTrotter

> A full-stack travel planning web app built with Django. Plan trips, build itineraries, track budgets, manage packing lists, and book curated travel packages — all in one place.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.0.14-green?logo=django)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38bdf8?logo=tailwindcss)

---

## 📸 Features

- 🔐 **Authentication** — Email/username login, signup, and password reset.
- 🗺️ **Trip Planning** — Create trips with custom titles, dates, and cover images.
- 🏙️ **Itinerary Builder** — Add multi-city stops with drag-and-drop reordering.
- 📅 **Timeline View** — Day-by-day activity timeline for each trip.
- 💰 **Budget Tracker** — Cost breakdowns by transport, hotel, food, and activities.
- 🎒 **Packing Checklist** — Organize items by category and check them off as you pack.
- 📝 **Trip Notes** — Write and edit freeform notes per trip.
- 🌍 **Destinations & Packages** — Browse curated destinations and book travel packages.
- 📊 **Admin Analytics Dashboard** — Built-in dashboard for tracking platform usage and trends.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Git

> **Demo Login (Normal User):**
> Email/Username: `sndarji172007@gmail.com`
> Password: `Naiya@2002`
> 
> **Admin Login (Superuser):**
> Username: `Naiya`
> Password: `Shlesh@17`

---

## 💻 Local Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Shlesh2007/GlobeTrotter.git
cd GlobeTrotter(LDEC_odoo)
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

### 4. Set environment variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-django-secret-key
```
*(For local development, `SECRET_KEY` can be any random string).*

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create an Admin User (Optional)
```bash
python manage.py createsuperuser
```

### 7. Start the Development Server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser to view the app!

---

## 🛠️ Tech Stack

- **Backend:** Python, Django 5.0.14
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Frontend:** HTML5, Django Templates, Tailwind CSS
- **Charts:** Chart.js (Analytics Dashboard)
