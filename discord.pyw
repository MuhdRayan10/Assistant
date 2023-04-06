from subprocess import call
from tkinter import Tk, Label
from PIL import Image, ImageTk
from time import sleep
import json

import win32.lib.win32con as win32con
import win32gui

the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)



FILE_PATH = "E:/Programming/Python/Assistant/Assistant/data/apps/locker/config.json"
ERROR_IMG = "E:/Programming/Python/Assistant/Assistant/data/apps/locker/404_image.png"

with open(FILE_PATH) as f:
    config = json.load(f)

if not config["lock"]:
    call("C:/Users/user/AppData/Local/Discord/Update.exe --processStart Discord.exe")
    
else:
    sleep(2)

    root = Tk()
    root.overrideredirect(True) 
    root.eval('tk::PlaceWindow . center')

    img = ImageTk.PhotoImage(Image.open(ERROR_IMG).resize((600, 400)))

    error = Label(image=img)
    error.img = img

    error.pack()
    error.after(7500, root.destroy)

    root.mainloop()
