from tkinter import *
from test_words import word_list
import time
import tkinter.font as tkFont
import random

start = None
end = None

window = Tk()
window.title("Speed Typing Tester")

window.minsize(width=300, height=200)
window.config(padx=20, pady=20)

def clicked_start():
    global start, end
    start = time.time()

    random_word = random.choice(word_list)
    label.config(text=random_word)

def clicked_stop():
    global start, end

    if start == None:
        print("You must start first!")
    else:
        end = time.time()
        length = end - start

        calc_label.config(text=f"Speed: {length:.2f} seconds")


# Define a custom font
custom_font = tkFont.Font(family="Arial", size=20)

#Labels
label = Label(window, font=custom_font ,text="Press start to begin: ")
label.grid(row=0, column=0)

#Labels
calc_label = Label(window, font=custom_font ,text=f"Speed:  seconds")
calc_label.grid(row=3, column=0)

# Create the button frame (container for buttons)
button_frame = Frame(window)
button_frame.grid(row=1, column=0, columnspan=3, sticky="ew")

# Make the three button columns equal
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

# Buttons
start_button = Button(button_frame, text="Start", font=custom_font , command=clicked_start)
start_button.grid(row=1, column=0, sticky="ew")

stop_button = Button(button_frame, text="Stop", font=custom_font , command=clicked_stop)
stop_button.grid(row=1, column=1, sticky="ew")

#Entries
entry = Entry(width=30, font=custom_font)
#Add some text to begin with
entry.insert(END, string=" ")
#Gets text in entry
print(entry.get())
entry.grid(row=2, column=0)


window.mainloop()