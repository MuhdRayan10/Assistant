# MAIN FILE

from pytube import YouTube
from datetime import datetime
import os


def download_video(url):

    start = datetime.now()

    yt = YouTube(url)
    yt = yt.streams.get_highest_resolution()

    try:
        yt.download()
    except:
        return False
    
    files = os.listdir()
    for file in files:
        if file.endswith(".mp4"):
            os.replace(file, f"./downloads/{file}")

    return (datetime.now() - start).seconds

print(download_video("https://www.youtube.com/watch?v=JIPQbgPk4oA"))
