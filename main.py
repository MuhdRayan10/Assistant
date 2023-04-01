# MAIN FILE

from pytube import Search
from datetime import datetime
import os


def download_video(search):

    start = datetime.now()

    s = Search(search)

    yt = s.results[0]
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

             

print(download_video("Organic Chemistry tutor electricity"))
