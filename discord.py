from AppOpener import open as op
from tkinter import Tk, Label
from PIL import Image, ImageTk
from time import sleep
import json

sleep(2)

FILE_PATH = "E:/Programming/Python/Assistant/Assistant/data/apps/locker/config.json"
ERROR_IMG = "E:/Programming/Python/Assistant/Assistant/data/apps/locker/404_image.png"

with open(FILE_PATH) as f:
    config = json.load(f)

if not config["lock"]:
    op("discord")
else:
    root = Tk()
    root.overrideredirect(True) 
    root.eval('tk::PlaceWindow . center')

    img = ImageTk.PhotoImage(Image.open(ERROR_IMG).resize((600, 400)))

    error = Label(image=img)
    error.img = img

    error.pack()
    error.after(7500, root.destroy)

    root.mainloop()
