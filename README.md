# Prime City Properties - Commercial Real Estate Platform

> **Company Motto**: “Stop Searching. Start Living.”

Prime City Properties is an enterprise-grade, production-ready luxury real estate platform built with **Python**, **Django 5**, **PostgreSQL**, **HTML5/CSS3**, and **Bootstrap 5**, explicitly customized for the Nigerian real estate market.

---

## 🌟 Key Features

### Public Portal
- **Advanced Search & Multi-Facet Filtering**: Real-time filtering by Location (Lekki Phase 1, Ikoyi, Victoria Island, Banana Island, Maitama Abuja, Port Harcourt), Property Type, Bedrooms, Bathrooms, Min/Max Price in Nigerian Naira (₦), Area size in sqm, Swimming Pool, Garage, and status (For Sale, For Rent, Sold, Rented).
- **Luxury Property Cards & Detail Pages**: High-resolution image galleries, price in ₦, detailed story callouts ("What makes this property special?"), specs grid, features/amenities, nearby landmarks, and direct WhatsApp inquiry buttons.
- **Dedicated Tour Booking Workflow**: Integrated Schedule a Tour experience with date/time picker, server-side date validation (prevents past dates), spam protection, and reference receipt generator.
- **Floating Schedule Tour Button**: Fixed, elegant bottom-right widget accessible across all devices without blocking navigation.
- **Contact Management**: Inquiry system with phone/email/office details and interactive message form.
- **Legal Compliance Suite**: Terms & Conditions, Refund Policy, Privacy Policy, and Accessibility Statement pages.
- **Technical SEO**: Dynamic `sitemap.xml`, `robots.txt`, and OpenGraph metadata tags.

### Administrative Backend
- **Custom Admin Metrics Dashboard**: Overview of total properties, active listings, pending tour bookings count, unread customer messages, and total portfolio valuation.
- **Property Management**: Publish/unpublish, feature properties, upload multiple image galleries with primary toggles, manage locations and amenities.
- **Tour Booking Workflows**: Filter and search appointments, toggle booking status (Pending, Confirmed, Completed, Cancelled).
- **Inquiry Management**: Mark messages as Read/Unread, Archive, or Delete.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.12, Django 5.1, Django REST Framework
- **Database**: PostgreSQL (with automatic SQLite fallback for rapid local dev)
- **Frontend**: HTML5, Vanilla JS, Bootstrap 5, Custom CSS Variables & Micro-animations
- **Branding Palette**: Khaki (`#6B5E4C`), Cream (`#FAF7F2`), Dark Ebony (`#1C1614`), Warm Gold (`#C5A059`)
- **Typography**: Google Fonts (*Playfair Display* serif headings + *Plus Jakarta Sans* clean sans body)

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
- Python 3.10+ installed
- Git installed
- PostgreSQL installed (optional for local SQLite fallback)

### 2. Environment Setup
```bash
# Clone or open project directory
cd PrimeCity

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 4. Run Database Migrations & Seed Initial Data
```bash
# Apply database migrations
python manage.py migrate

# Populate realistic Nigerian luxury sample properties, locations, testimonials & initial setup
python manage.py seed_properties
```
*Administrator Credentials Security Notice*:
- To create a new administrator account: `python manage.py createsuperuser`
- To update an existing administrator password: `python manage.py changepassword <email>`
- You can also change your password directly from the user dashboard after logging in (`/dashboard/`).

### 5. Start Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser. Access the admin dashboard at `http://127.0.0.1:8000/admin/`.

---

## 🧪 Running Automated Tests

Run the full Django test suite to verify models, views, filters, tour bookings, and forms:

```bash
python manage.py test
```

---

## 🚢 Production Deployment Guide

### Option 1: Docker Compose (Recommended)
```bash
# Build and launch production containers (Nginx + Gunicorn + PostgreSQL)
docker-compose up -d --build

# Run migrations & seed inside docker web container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py seed_properties
```

### Option 2: Linux (Ubuntu/Debian) Nginx + Gunicorn Manual Deployment
1. **PostgreSQL Database Setup**:
   ```sql
   CREATE DATABASE primecity_db;
   CREATE USER primecity_user WITH PASSWORD 'secure_password_here';
   GRANT ALL PRIVILEGES ON DATABASE primecity_db TO primecity_user;
   ```
2. **Configure Production Settings**:
   Set `DJANGO_SETTINGS_MODULE=config.settings.production` and updated `.env` values.
3. **Collect Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```
4. **Copy Systemd & Nginx configs**:
   - Copy `deployment/gunicorn.service` to `/etc/systemd/system/gunicorn.service`
   - Copy `deployment/nginx.conf` to `/etc/nginx/sites-available/primecity`
   - Enable Nginx site: `ln -s /etc/nginx/sites-available/primecity /etc/nginx/sites-enabled/`
   - Restart services: `systemctl restart gunicorn nginx`
