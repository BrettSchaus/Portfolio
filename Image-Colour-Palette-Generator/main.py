import numpy as np
from PIL import Image  # for reading image files
from flask import Flask, render_template, request

def get_top_10_colours(img):
    pixels = img.reshape(-1, 3) # Flattening the image

    pixels = (pixels // 10) * 10  # Rounding values since there could be many different colours
    unique, counts = np.unique(pixels, axis=0, return_counts=True)
    indices = np.argsort(counts)[::-1]
    top10 = unique[indices[:10]]
    top_10_counts = counts[indices[:10]]
    total_pixels = counts.sum()
    percentages = (top_10_counts / total_pixels) * 100
    
    colours = []

    # Converting our top 10 into HEX colours
    for i, colour in enumerate(top10):
        r, g, b = map(int, colour)
        hex_colour = f"#{r:02X}{g:02X}{b:02X}"

        brightness = (r * 299 + g * 587 + b * 114) / 1000

        if brightness < 128:
            text_colour = "white"
        else:
            text_colour = "black"

        colours.append({
            "hex": hex_colour,
            "percentage": percentages[i],
            "text_colour": text_colour
        })
    return colours

app = Flask(__name__)


@app.route('/', methods=["GET","POST"])
def home():
    
    colours = None
    
    if request.method == "POST":
        image = request.files['image']
        
        if image.filename != "":  # Checking to see if user chose an image
            image = Image.open(image)
            image = image.convert("RGB")
            image.save("static/uploaded.jpg")  #Saves image and converts to proper format for numpy
        
            my_img = Image.open("static/uploaded.jpg") # Loads from saved point, this way it doesn't rely on the object's current state
            img = np.array(my_img)

            colours = get_top_10_colours(img)
    
    return render_template("index.html", colours=colours)



if __name__ == "__main__":
    app.run(debug=True, port=5002)

