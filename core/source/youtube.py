from yt_dlp import YoutubeDL
import time

def download_video (video_url, target_path):



    list_tmp = target_path.split(".")
    output_path = f".{list_tmp[1]}"
    format = list_tmp[2]
    ydl_opts = {
        "quiet": True,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best", #format,
        "outtmpl": f"{output_path}.%(ext)s",
        "restrictfilenames": True,
    }
    
    start_time = time.time()

    try:
        with YoutubeDL(ydl_opts) as ydl:
            is_done = ydl.download([video_url])
    except:
        return "False"

    end_time = time.time()
    runtime = end_time - start_time
  
    if runtime < 3:
        return "Skip"
    else:
        return "Done"
