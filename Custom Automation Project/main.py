import os
import random
import subprocess
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
# Folder Path
wallpaper_folder = "/home/brett/Pictures/Wallpapers"

change_interval = 10

number_of_images = 10

headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
params = {
    "query": "animals",
    "orientation": "landscape",
    "per_page": 30
}

response = requests.get("https://api.unsplash.com/search/photos", headers=headers, params=params)
response.raise_for_status()

data = response.json()
results = data.get("results", [])

# Download images
downloaded = 0

for photo in results:
    if downloaded >= number_of_images: # Breaks loop once downloaded has reached specified value
        break
    image_url = photo["urls"]["full"]

    image_response = requests.get(
        image_url,
        timeout=60
    )

    image_response.raise_for_status()

    file_path = os.path.join(
        wallpaper_folder,
        f"animal_{downloaded}.jpg"
    )

    with open(file_path, "wb") as file:
        file.write(image_response.content)

    print(f"Downloaded: animal_{downloaded}.jpg")

    downloaded += 1

# Find wallpapers
photos = [
    file
    for file in os.listdir(wallpaper_folder)
    if file.lower().endswith(
        (".jpg", ".jpeg", ".png", ".webp")
    )
]



# Change GNOME wallpaper
while True:

    photo = random.choice(photos)

    photo_path = os.path.join(
        wallpaper_folder,
        photo
    )

    print(f"Setting wallpaper: {photo}")

    # GNOME light mode
    subprocess.run([
        "gsettings",
        "set",
        "org.gnome.desktop.background",
        "picture-uri",
        f"file://{photo_path}"
    ])

    # GNOME dark mode
    subprocess.run([
        "gsettings",
        "set",
        "org.gnome.desktop.background",
        "picture-uri-dark",
        f"file://{photo_path}"
    ])

    time.sleep(change_interval)