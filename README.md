# Bisrate Gabriel Apartment in Addis — Luxury Apartment Website

A premium real estate marketing website built with Python Flask, HTML5, Tailwind CSS, and JavaScript.

## Project Structure

```
luxe_residences/
├── app.py                  # Flask backend + all property data
├── requirements.txt
├── templates/
│   └── index.html          # Main single-page template
└── static/
    ├── css/
    │   └── main.css        # All custom styles
    └── js/
        └── main.js         # All interactivity
```

## Quick Start

### 1. Create & activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python app.py
```

### 4. Open in browser
```
http://localhost:5000
```

---

## Features

### Sections
- **Hero** — Full-screen image, property name, tagline, CTA buttons, animated stats bar
- **Overview** — Property description, stacked images, key numbers
- **Map** — Embedded Google Maps iframe + nearby POI panel (restaurants, parks, transit, schools)
- **Floor Plans** — Filterable unit cards with images, specs, pricing, and availability
- **Pricing Table** — Sortable table of all unit types with real-time availability colors
- **Amenities** — 12-item grid with icons, names, descriptions
- **Gallery** — Drag/swipe slider with lightbox viewer
- **Neighborhood** — Description + image grid + POI list
- **Contact / Tour Form** — Full form with validation, POSTed to `/api/tour`

### API Endpoints
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Main page |
| `/api/availability?beds=N` | GET | Filter units by bedroom count |
| `/api/tour` | POST | Submit tour request (JSON body) |

### Customization
All property data lives in `app.py` at the top — edit `PROPERTY`, `FLOOR_PLANS`, `AMENITIES`, `GALLERY`, and `NEARBY` to match your actual listing.

### Google Maps
Replace the iframe `src` in `templates/index.html` → `#map` section with your actual embed URL from [Google Maps Embed API](https://developers.google.com/maps/documentation/embed/get-started).

---

## Tech Stack
- Python 3.10+ / Flask 3.x
- Tailwind CSS (CDN)
- Cormorant Garamond + Montserrat (Google Fonts)
- Lucide Icons (CDN)
- Vanilla JavaScript (no framework)

## Production Deployment
For production, use Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
