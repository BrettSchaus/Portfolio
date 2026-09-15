from tkinter import *
import random

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Ariel", 40, "italic")


PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_SEC = 5
timer = None

def reset_timer(event=None):
    global timer
    
    if timer is not None:
        window.after_cancel(timer)
    
    count_down(WORK_SEC)

def start_timer():
    count_down(WORK_SEC)
    
def count_down(count):
    global timer
    
    timer_label.config(text=count)

    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        input.delete("1.0", END)


window = Tk()
window.title("Disappearing Text Writing App")
window.minsize(width=300, height=200)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Labels
timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW,font=(FONT_NAME, 40, "bold"))
timer_label.grid(column=1, row=0)

check_label = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
check_label.grid(column=1, row=1)


# Buttons
start_image = Button(text="Start", width=10, height=2, font=(FONT_NAME, 20), highlightthickness=0, command=start_timer)
start_image.grid(column=0, row=0)

# Entry
input = Text(width=80, height=20)
input.bind("<Key>", reset_timer)
input.grid(column=0, row=2, columnspan=2, sticky="nsew")



window.mainloop()