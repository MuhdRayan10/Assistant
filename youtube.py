
from tkinter import messagebox, ttk
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
from datetime import datetime
from tkinter import *
from io import BytesIO
from PIL import Image, ImageTk
import requests
import threading
import os

FORMATS = ['13'+ str(i) for i in range(7,2,-1)]

def download_video(vid):

    start = datetime.now()
    error, i = True, 0
    
    while error:

        try:
            with YoutubeDL({'format':FORMATS[i]}) as ydl:
                ydl.download(['https://www.youtube.com/watch?v='+vid])
            break

        except:
            i += 1
            error = True

            if i > 5: break  

    files = os.listdir()
    for file in files:
        if file.endswith(".mp4"):
            os.replace(file, f"./data/downloads/{file.replace(f' [{vid}]', '')}")


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
        self.search_box = ttk.Entry(self, width=50, justify='center')
        self.search_box.pack(pady=20)

        self.search_box.bind('<Return>', lambda _: self.search())

        
        search_button = ttk.Button(self, text="Search", command=self.search)
        search_button.pack()
        
        separator = ttk.Separator(self)
        separator.pack(pady=10, fill='x', expand=True)

        self.results = Frame(self, bg="#3c3c3c")
        self.results.pack(expand=True)


    def search(self):
        query = self.search_box.get()

        s = VideosSearch(query, limit=4).result()

        for widget in self.results.winfo_children():
            widget.destroy()

        search = Label(self.results, text="Results", fg="#f5f5f5", bg="#3c3c3c")
        search.pack()


        for result in s["result"]:

            response = requests.get(result['thumbnails'][0]['url'])

            img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((128, 72), Image.ANTIALIAS))

            frame = Frame(self.results, bg="#3c3c3c")
            frame.pack(anchor='w')

            thread = threading.Thread(target=self.selected, args=(result['id'],))

            btn = Button(frame, image=img, command=thread.start, borderwidth=0)
            btn.image = img
            btn.grid(row=0, column=0, rowspan=2)
            

            title = Label(frame, text="   " + result["title"], fg="#f5f5f5", bg="#3c3c3c", justify='center')
            title.grid(row=0, column=1, sticky=NSEW)

            author = Label(frame, text=result["channel"]["name"], fg="#C1839F", bg="#3c3c3c")
            author.grid(row=1, column=1)

        del s

    def selected(self, search):

        messagebox.showinfo("Starting Download", "The video will be downloaded shortly.")
        
        t = download_video(search)

        messagebox.showinfo("Download successful", f"The video has been downloaded in {t} seconds.")
        del t

YouTubeGUI()