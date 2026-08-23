from flask import Flask, render_template, request, jsonify, url_for
from datetime import datetime
from werkzeug.utils import secure_filename
import json
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['UPLOAD_FOLDER'] = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load photos configuration
def load_photos_config():
    config_path = 'photos_config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return None

def save_photos_config(config):
    config_path = 'photos_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

PHOTOS = load_photos_config()

# Helper function to get image path (returns path, not URL)
def get_image_path(config_key, fallback_url):
    if PHOTOS:
        # Navigate nested config keys
        keys = config_key.split('.')
        value = PHOTOS
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return fallback_url
        return value
    return fallback_url

# Helper function to convert path to URL (call within app context)
def path_to_url(path):
    if path.startswith('static/'):
        return url_for('static', filename=path.replace('static/', ''))
    return path

# Property Data
# NOTE: address/phone/email/floors/total_units/year_built/description are placeholders
# pending confirmed details from the property owner (see intake sheet).
PROPERTY = {
    "name": "Noor Residence",
    "tagline": "",
    "address": "Address to be confirmed — Addis Ababa, Ethiopia",
    "phone": "Phone to be confirmed",
    "email": "Email to be confirmed",
    "hours": "Hours to be confirmed",
    "lat": 9.0320,
    "lng": 38.7636,
    "floors": 7,
    "total_units": 12,
    "year_built": 2026,
    "description": (
        "Noor Residence is a modern residential tower in Addis Ababa, offering thoughtfully "
        "designed apartments with quality finishes and city views. Full details on the "
        "building and its amenities are coming soon."
    ),
}

FLOOR_PLANS = [
    {
        "id": "studio",
        "type": "Studio",
        "beds": 0,
        "baths": 1,
        "sqft_min": 520,
        "sqft_max": 620,
        "price_min": 75000,
        "price_max": 85000,
        "available": 4,
        "image": get_image_path("floor_plan_images.studio", "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&q=80"),
        "features": ["Quartz counters", "In-unit laundry", "City views"],
    },
    {
        "id": "one_bed",
        "type": "1 Bedroom",
        "beds": 1,
        "baths": 1,
        "sqft_min": 720,
        "sqft_max": 920,
        "price_min": 90000,
        "price_max": 105000,
        "available": 8,
        "image": get_image_path("floor_plan_images.one_bed", "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&q=80"),
        "features": ["Separate dining area", "Walk-in closet", "Soaking tub"],
    },
    {
        "id": "two_bed",
        "type": "2 Bedroom",
        "beds": 2,
        "baths": 2,
        "sqft_min": 1100,
        "sqft_max": 1420,
        "price_min": 110000,
        "price_max": 130000,
        "available": 5,
        "image": get_image_path("floor_plan_images.two_bed", "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800&q=80"),
        "features": ["Split bedroom layout", "Chef's kitchen", "Private balcony"],
    },
    {
        "id": "three_bed",
        "type": "3 Bedroom",
        "beds": 3,
        "baths": 2,
        "sqft_min": 1650,
        "sqft_max": 2100,
        "price_min": 140000,
        "price_max": 165000,
        "available": 2,
        "image": get_image_path("floor_plan_images.three_bed", "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&q=80"),
        "features": ["Corner unit", "Wraparound terrace", "Home office nook"],
    },
    {
        "id": "penthouse",
        "type": "Penthouse",
        "beds": 4,
        "baths": 3,
        "sqft_min": 3200,
        "sqft_max": 4000,
        "price_min": 200000,
        "price_max": 250000,
        "available": 1,
        "image": get_image_path("floor_plan_images.penthouse", "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80"),
        "features": ["Dual-level layout", "Private rooftop", "Butler's pantry"],
    },
]

AMENITIES = [
    {"icon": "dumbbell", "name": "Fitness Center", "desc": "State-of-the-art equipment, yoga studio & Peloton room"},
    {"icon": "droplets", "name": "Infinity Pool", "desc": "Heated rooftop pool with panoramic city views"},
    {"icon": "car", "name": "Valet Parking", "desc": "24/7 valet & electric vehicle charging stations"},
    {"icon": "wifi", "name": "Smart Home", "desc": "App-controlled climate, locks & custom lighting scenes"},
    {"icon": "building-2", "name": "Rooftop Lounge", "desc": "Sky terrace with bar, fire pits & private cabanas"},
    {"icon": "shield-check", "name": "24/7 Concierge", "desc": "Dedicated hospitality team for every need"},
    {"icon": "package", "name": "Package Room", "desc": "Refrigerated delivery storage & Amazon Hub"},
    {"icon": "paw-print", "name": "Pet Spa", "desc": "Dog wash, grooming station & pet relief area"},
    {"icon": "coffee", "name": "Resident Lounge", "desc": "Co-working spaces, private dining & demo kitchen"},
    {"icon": "bicycle", "name": "Bike Storage", "desc": "Secured bike room with tune-up station"},
    {"icon": "sparkles", "name": "Dry Cleaning", "desc": "On-site valet dry cleaning & pressing service"},
    {"icon": "gamepad-2", "name": "Game Room", "desc": "Billiards, ping pong, arcade & screening room"},
]

# Load gallery from config or use defaults
if PHOTOS and 'gallery' in PHOTOS:
    GALLERY = PHOTOS['gallery']
else:
    GALLERY = [
        {"url": "https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=1200&q=85", "caption": "Elegant Lobby"},
        {"url": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=1200&q=85", "caption": "Spacious Living Room"},
        {"url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=1200&q=85", "caption": "Modern Kitchen"},
        {"url": "https://images.unsplash.com/photo-1564078516393-cf04bd966897?w=1200&q=85", "caption": "Luxury Master Bath"},
        {"url": "https://images.unsplash.com/photo-1609137144813-7d9921338f24?w=1200&q=85", "caption": "Addis Ababa Skyline View"},
        {"url": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=1200&q=85", "caption": "State-of-the-art Fitness Center"},
        {"url": "https://images.unsplash.com/photo-1611348524140-53c9a25263d6?w=1200&q=85", "caption": "City Views from Residence"},
        {"url": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=1200&q=85", "caption": "Building Exterior"},
    ]

NEARBY = [
    {"type": "restaurant", "name": "Yod Abyssinia", "dist": "2.5 km", "desc": "Traditional Ethiopian cuisine with cultural shows"},
    {"type": "park", "name": "Unity Park", "dist": "3.0 km", "desc": "Historic park with museums and gardens"},
    {"type": "transit", "name": "Bole International Airport", "dist": "5.5 km", "desc": "Main international airport"},
    {"type": "school", "name": "Addis Ababa University", "dist": "4.0 km", "desc": "Ethiopia's premier university"},
    {"type": "restaurant", "name": "Castelli Restaurant", "dist": "1.8 km", "desc": "Fine Italian dining since 1948"},
    {"type": "park", "name": "Meskel Square", "dist": "3.5 km", "desc": "Major public square and cultural venue"},
]


@app.route("/")
def index():
    # Convert floor plan image paths to URLs
    floor_plans_with_urls = []
    for fp in FLOOR_PLANS:
        fp_copy = fp.copy()
        fp_copy['image'] = path_to_url(fp['image'])
        floor_plans_with_urls.append(fp_copy)
    
    # Convert gallery paths to URLs
    gallery_with_urls = []
    for item in GALLERY:
        item_copy = item.copy()
        item_copy['url'] = path_to_url(item['url'])
        gallery_with_urls.append(item_copy)
    
    # Prepare template data with image URLs
    template_data = {
        'property': PROPERTY,
        'floor_plans': floor_plans_with_urls,
        'amenities': AMENITIES,
        'gallery': gallery_with_urls,
        'nearby': NEARBY,
        'hero_image': path_to_url(get_image_path('hero_image', 'https://images.unsplash.com/photo-1609137144813-7d9921338f24?w=2400&q=95')),
        'overview_main': path_to_url(get_image_path('overview_images.main', 'https://images.unsplash.com/photo-1609137144813-7d9921338f24?w=700&q=85')),
        'overview_secondary': path_to_url(get_image_path('overview_images.secondary', 'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=400&q=85')),
        'neighborhood_cityscape': path_to_url(get_image_path('neighborhood_images.cityscape', 'https://images.unsplash.com/photo-1611348524140-53c9a25263d6?w=600&q=85')),
        'neighborhood_unity_park': path_to_url(get_image_path('neighborhood_images.unity_park', 'static/images/unity_park.jpg')),
        'neighborhood_restaurant': path_to_url(get_image_path('neighborhood_images.restaurant', 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&q=85')),
        'contact_bg': path_to_url(get_image_path('contact_background', 'https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=1600&q=85')),
    }
    return render_template("index.html", **template_data)


@app.route("/api/availability")
def availability():
    bed_filter = request.args.get("beds", "all")
    results = []
    for fp in FLOOR_PLANS:
        if bed_filter == "all" or str(fp["beds"]) == bed_filter:
            results.append({
                "id": fp["id"],
                "type": fp["type"],
                "beds": fp["beds"],
                "baths": fp["baths"],
                "sqft_min": fp["sqft_min"],
                "sqft_max": fp["sqft_max"],
                "price_min": fp["price_min"],
                "price_max": fp["price_max"],
                "available": fp["available"],
            })
    return jsonify(results)


@app.route("/api/tour", methods=["POST"])
def schedule_tour():
    data = request.get_json()
    required = ["name", "email", "phone", "date", "unit_type"]
    for field in required:
        if not data.get(field):
            return jsonify({"success": False, "message": f"Missing field: {field}"}), 400
    # In production: save to DB, send email, etc.
    return jsonify({
        "success": True,
        "message": f"Thank you, {data['name']}! Your tour is confirmed for {data['date']}. We'll reach out at {data['email']}.",
    })


# Admin routes
@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/upload", methods=["POST"])
def upload_photo():
    try:
        if 'photo' not in request.files:
            return jsonify({"success": False, "message": "No photo file provided"}), 400
        
        file = request.files['photo']
        category = request.form.get('category')
        caption = request.form.get('caption', '')
        
        if not category:
            return jsonify({"success": False, "message": "Category is required"}), 400
        
        if file.filename == '':
            return jsonify({"success": False, "message": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"success": False, "message": "Invalid file type. Use PNG, JPG, or JPEG"}), 400
        
        # Generate filename based on category
        ext = file.filename.rsplit('.', 1)[1].lower()
        
        # Map category to config structure and filename
        category_map = {
            'hero': ('hero_image', 'hero.jpg'),
            'overview_main': ('overview_images.main', 'overview-main.jpg'),
            'overview_secondary': ('overview_images.secondary', 'overview-secondary.jpg'),
            'contact_bg': ('contact_background', 'contact-bg.jpg'),
            'floorplan_studio': ('floor_plan_images.studio', 'floorplans/studio.jpg'),
            'floorplan_1bed': ('floor_plan_images.one_bed', 'floorplans/1bed.jpg'),
            'floorplan_2bed': ('floor_plan_images.two_bed', 'floorplans/2bed.jpg'),
            'floorplan_3bed': ('floor_plan_images.three_bed', 'floorplans/3bed.jpg'),
            'floorplan_penthouse': ('floor_plan_images.penthouse', 'floorplans/penthouse.jpg'),
            'neighborhood_cityscape': ('neighborhood_images.cityscape', 'neighborhood/cityscape.jpg'),
            'neighborhood_unity_park': ('neighborhood_images.unity_park', 'unity_park.jpg'),
            'neighborhood_restaurant': ('neighborhood_images.restaurant', 'neighborhood/restaurant.jpg'),
        }
        
        if category == 'gallery':
            # For gallery, generate unique filename
            import time
            filename = f"gallery/gallery-{int(time.time())}.{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Ensure gallery directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            
            # Update config - add to gallery array
            config = load_photos_config() or {}
            if 'gallery' not in config:
                config['gallery'] = []
            
            config['gallery'].append({
                'url': f'static/images/{filename}',
                'caption': caption or 'Gallery Photo'
            })
            save_photos_config(config)
            
        elif category in category_map:
            config_key, filename = category_map[category]
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            
            # Update config
            config = load_photos_config() or {}
            
            # Navigate to nested key and update
            keys = config_key.split('.')
            if len(keys) == 1:
                config[keys[0]] = f'static/images/{filename}'
            else:
                if keys[0] not in config:
                    config[keys[0]] = {}
                config[keys[0]][keys[1]] = f'static/images/{filename}'
            
            save_photos_config(config)
        else:
            return jsonify({"success": False, "message": "Invalid category"}), 400
        
        # Reload config
        global PHOTOS
        PHOTOS = load_photos_config()
        
        return jsonify({"success": True, "message": "Photo uploaded successfully"})
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/admin/photos")
def list_photos():
    try:
        photos = []
        config = load_photos_config() or {}
        
        # Helper to add photo to list
        def add_photo(url, name, category, caption=None):
            if url and url.startswith('static/'):
                photos.append({
                    'url': url_for('static', filename=url.replace('static/', '')),
                    'name': name,
                    'category': category,
                    'caption': caption
                })
        
        # Single images
        if 'hero_image' in config:
            add_photo(config['hero_image'], 'Hero Image', 'Hero')
        
        if 'contact_background' in config:
            add_photo(config['contact_background'], 'Contact Background', 'Contact')
        
        # Overview images
        if 'overview_images' in config:
            if 'main' in config['overview_images']:
                add_photo(config['overview_images']['main'], 'Overview Main', 'Overview')
            if 'secondary' in config['overview_images']:
                add_photo(config['overview_images']['secondary'], 'Overview Secondary', 'Overview')
        
        # Floor plans
        if 'floor_plan_images' in config:
            for key, value in config['floor_plan_images'].items():
                add_photo(value, f'Floor Plan - {key.replace("_", " ").title()}', 'Floor Plans')
        
        # Neighborhood
        if 'neighborhood_images' in config:
            for key, value in config['neighborhood_images'].items():
                add_photo(value, f'Neighborhood - {key.replace("_", " ").title()}', 'Neighborhood')
        
        # Gallery
        if 'gallery' in config:
            for item in config['gallery']:
                add_photo(item['url'], item.get('caption', 'Gallery Photo'), 'Gallery', item.get('caption'))
        
        return jsonify(photos)
    
    except Exception as e:
        return jsonify([])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
