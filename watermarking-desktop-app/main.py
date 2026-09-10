from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageFont, ImageDraw, ImageTk

# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfile

watermark_image = None
image = None
photo = None
panel = None

def browse_file():
    global watermark_image, image, photo

    file = askopenfile(
        mode='rb',
        initialdir='/home/brett/Downloads',
        title="Select image",
        filetypes=[
            ('JPG files', '*.jpg'),
            ('JPEG files', '*.jpeg'),
            ('PNG files', '*.png')
        ]
    )

    if file:
        image = Image.open(file)
        print("Loaded image successfully!")

        # Limit the image size while keeping its proportions
        image.thumbnail((600, 800))
        # Convert PIL image to a Tkinter-compatible image
        photo = ImageTk.PhotoImage(image)


        panel = Label(window, image=photo)
        panel.image = photo
        panel.grid(row=0, column=0, columnspan=3)
        watermark_image = image.copy() # Modifiable copy

def add_watermark():
    global watermark_image, image, photo

    if watermark_image is None:
        print("Please select an image first.")
        return

    w, h = image.size

    x = int(w / 2)
    y = int(h / 2)

    if x > y:
        font_size = y
    elif y > x:
        font_size = x
    else:
        font_size = x

    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(font_size / 6))

    # Create transparent layer for rotated text
    text_layer = Image.new("RGBA", watermark_image.size, (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_layer)

    text_draw.text(
        (x, y),
        "Watermark",
        fill=(0, 0, 0, 255),
        font=font,
        anchor="mm"
    )

    # Rotate text 45 degrees
    text_layer = text_layer.rotate(45, expand=False)

    # Combine with original image
    watermark_image = Image.alpha_composite(
        watermark_image.convert("RGBA"),
        text_layer
    )

    # Display the watermarked image
    photo = ImageTk.PhotoImage(watermark_image)

    panel = Label(window, image=photo)
    panel.image = photo
    panel.grid(row=0, column=0, columnspan=3)

    print("Watermark added!")


def save_image():
    global watermark_image, image, photo

    if watermark_image is None:
        print("Please select an image first.")
        return

    save_path = "/home/brett/Downloads/watermarked_image.jpg"

    watermark_image.convert("RGB").save(save_path)

    print(f"Image saved to {save_path}")

window = Tk()
window.title("Watermarking Application")

window.minsize(width=600, height=600)
window.config(padx=20, pady=20)

# Make the image area expand vertically
window.grid_rowconfigure(0, weight=1)
# Make the main column expand horizontally
window.grid_columnconfigure(0, weight=1)

# Create the button frame (container for buttons)
button_frame = Frame(window)
button_frame.grid(row=1, column=0, columnspan=3, sticky="ew")

# Make the three button columns equal
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)


# Buttons
browse_button = Button(button_frame, text="Browse", command=browse_file)
browse_button.grid(row=0, column=0, sticky="ew")

save_button = Button(button_frame, text="Save", command=save_image)
save_button.grid(row=0, column=2, sticky="ew")

add_watermark_button = Button(button_frame, text="Add Watermark", command=add_watermark)
add_watermark_button.grid(row=0, column=1, sticky="ew")







window.mainloop()