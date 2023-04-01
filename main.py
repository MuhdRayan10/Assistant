# MAIN FILE

from pytube import YouTube

def download_video(url):
    yt = YouTube(url)

    yt = yt.streams.get_highest_resolution()

    try:
        yt.download()
    except:
        return False
    
    return True

print(download_video("https://www.youtube.com/watch?v=JIPQbgPk4oA"))
