# How to Add Your Own Photos to the Website

This guide will show you how to easily add your own photos to your Bisrate Gabriel Apartments website.

## Quick Start

1. **Put your photos in the `static/images` folder**
2. **Edit the `photos_config.json` file** to point to your photos
3. **Restart the website** to see your changes

That's it! No coding required.

---

## Step-by-Step Instructions

### Step 1: Organize Your Photos

Create folders inside `static/images/` to keep things organized:

```
static/images/
├── hero.jpg                    (Main homepage image)
├── overview-main.jpg           (Building exterior)
├── overview-secondary.jpg      (Interior shot)
├── contact-bg.jpg             (Contact section background)
├── unity_park.jpg             (Already exists)
├── floorplans/
│   ├── studio.jpg
│   ├── 1bed.jpg
│   ├── 2bed.jpg
│   ├── 3bed.jpg
│   └── penthouse.jpg
├── neighborhood/
│   ├── cityscape.jpg
│   ├── restaurant.jpg
│   └── (other neighborhood photos)
└── gallery/
    ├── lobby.jpg
    ├── living-room.jpg
    ├── kitchen.jpg
    ├── bathroom.jpg
    ├── skyline.jpg
    ├── fitness.jpg
    ├── city-view.jpg
    └── exterior.jpg
```

### Step 2: Edit photos_config.json

Open the `photos_config.json` file in any text editor (Notepad, VS Code, etc.) and update the paths to match your photo filenames.

**Example:**
```json
{
  "hero_image": "static/images/hero.jpg",
  "overview_images": {
    "main": "static/images/overview-main.jpg",
    "secondary": "static/images/overview-secondary.jpg"
  },
  "floor_plan_images": {
    "studio": "static/images/floorplans/studio.jpg",
    "one_bed": "static/images/floorplans/1bed.jpg",
    "two_bed": "static/images/floorplans/2bed.jpg",
    "three_bed": "static/images/floorplans/3bed.jpg",
    "penthouse": "static/images/floorplans/penthouse.jpg"
  },
  "neighborhood_images": {
    "cityscape": "static/images/neighborhood/cityscape.jpg",
    "unity_park": "static/images/unity_park.jpg",
    "restaurant": "static/images/neighborhood/restaurant.jpg"
  },
  "contact_background": "static/images/contact-bg.jpg",
  "gallery": [
    {
      "url": "static/images/gallery/lobby.jpg",
      "caption": "Elegant Lobby"
    },
    {
      "url": "static/images/gallery/living-room.jpg",
      "caption": "Spacious Living Room"
    }
  ]
}
```

### Step 3: Restart the Website

If the website is running:
1. Stop it (press `Ctrl+C` in the terminal)
2. Start it again: `python app.py`

Your new photos will now appear on the website!

---

## Photo Specifications

### Recommended Image Sizes

- **Hero Image**: 2400px wide (landscape)
- **Overview Images**: 700-1000px wide
- **Floor Plans**: 800px wide
- **Gallery Images**: 1200px wide
- **Neighborhood Images**: 400-600px wide

### File Formats
- Use `.jpg` or `.jpeg` for photos
- Use `.png` for images with transparency
- Keep file sizes under 2MB for faster loading

### Tips for Best Results
- Use high-quality, well-lit photos
- Keep images in landscape (horizontal) orientation for most sections
- Compress images before uploading to reduce file size
- Use descriptive filenames (e.g., `lobby-entrance.jpg` instead of `IMG_1234.jpg`)

---

## Adding Gallery Photos

To add more photos to the gallery section:

1. Add your photos to `static/images/gallery/`
2. Open `photos_config.json`
3. Add new entries to the `gallery` array:

```json
"gallery": [
  {
    "url": "static/images/gallery/lobby.jpg",
    "caption": "Elegant Lobby"
  },
  {
    "url": "static/images/gallery/your-new-photo.jpg",
    "caption": "Your Photo Description"
  }
]
```

You can add as many gallery photos as you want!

---

## Troubleshooting

### Photo not showing up?
1. Check that the filename in `photos_config.json` matches exactly (including capitalization)
2. Make sure the photo is in the correct folder
3. Restart the website after making changes

### Photo looks stretched or distorted?
- Use the recommended image sizes above
- Make sure your photo has the right orientation (landscape vs portrait)

### Website won't start after changes?
- Check that your `photos_config.json` file has valid JSON syntax
- Make sure all quotes and commas are in the right place
- You can use an online JSON validator to check for errors

---

## Need Help?

If you run into issues:
1. Double-check your file paths in `photos_config.json`
2. Make sure all photos are in the `static/images/` folder
3. Restart the website after making changes
4. Check the terminal for any error messages

---

## Reverting to Default Photos

If you want to go back to the default placeholder photos, simply:
1. Rename or delete `photos_config.json`
2. Restart the website

The website will automatically use the default Unsplash photos.