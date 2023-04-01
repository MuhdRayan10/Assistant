
from pytube import Search
from datetime import datetime
from tkinter import *
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

class GUI(Tk):
    def __init__(self):
        super().__init__()
        
        self.title("YouTube downloader")
        self.geometry("500x400")

        self.config(bg="white")


        self.add_widgets()
        self.mainloop()

    def add_widgets(self):
        search_box = Entry(self, width=30, borderwidth=4)
        search_box.pack(pady=5)

        search_button = Button(self, bg="brown", text="Search", command=lambda: self.search(search_box.get()))
        search_button.pack(pady=10)

        results = Frame(self, bg="red")
        results.pack(expand=True)

    def search(self, query):
        s = Search(query)
        for result in s.results:
            print(result.thumbnail_url)




GUI()