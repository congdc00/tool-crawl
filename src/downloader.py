
from core.source.youtube import download_video
from core.log.logger import Logger

def download(link_video, target_path):
    status = download_video(link_video, target_path)
    if status == "Skip" or status =="False":
        return False
    else:
        return True
