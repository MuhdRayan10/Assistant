
from pytube import Search
from datetime import datetime
from tkinter import *
from io import BytesIO
from PIL import Image, ImageTk
import requests
import os


def download_video(yt):

    start = datetime.now()

    yt = yt.streams.get_highest_resolution()

    try:
        yt.download()
    except:
        return False
    
    files = os.listdir()
    for file in files:
        if file.endswith(".mp4"):
            os.replace(file, f"./downloads/{file}")


    del yt, files
    return (datetime.now() - start).seconds

class YouTubeGUI(Tk):
    def __init__(self):
        super().__init__()
        
        self.title("YouTube downloader")
        self.geometry("600x450")

        self.config(bg="white")


        self.add_widgets()
        self.mainloop()

    def add_widgets(self):
        search_box = Entry(self, width=30, borderwidth=4, justify='center')
        search_box.pack(pady=5)

        search_button = Button(self, bg="brown", text="Search", command=lambda: self.search(search_box.get()))
        search_button.pack(pady=10)
        
        self.results = Frame(self, bg="#3c3c3c")
        self.results.pack(expand=True)


    def search(self, query):
        s = Search(query)

        for widget in self.results.winfo_children():
            widget.destroy()

        search = Label(self.results, text="Results", fg="#f5f5f5", bg="#3c3c3c")
        search.pack()


        for result in s.results[:4]:
            response = requests.get(result.thumbnail_url)

            img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((128, 72), Image.ANTIALIAS))

            frame = Frame(self.results, bg="#3c3c3c")
            frame.pack(anchor='w')

            btn = Button(frame, image=img, command=lambda x=result:self.selected(x), borderwidth=0)
            btn.image = img
            btn.grid(row=0, column=0, rowspan=2)
            
            title = Label(frame, text=result.title, fg="#f5f5f5", bg="#3c3c3c")
            title.grid(row=0, column=1)

            author = Label(frame, text=result.author, fg="#C1839F", bg="#3c3c3c")
            author.grid(row=1, column=1)

    def selected(self, search):
        pass      

YouTubeGUI()