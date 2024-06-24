from src.crawl.youtube.videos import get_channel_id, get_videos_id, get_video_url
from src.crawl.youtube.thumbs import download_thumb
from src.utils.load_data.youtube import load_info
from src.utils.history import Historian
from tqdm import tqdm
import os
# config
from loguru import logger
import yaml

SAVE_DATA_PATH = "data/output/"
SOURCE_CHANELS = "data/source/thumb-youtube/furniture.txt"


if __name__ == "__main__":
    
    

    historian = Historian(mode="thumbs_youtube")
    logger.info(f"Load subjects")
    subjects = load_info(SOURCE_CHANELS)
    
    # Subject
    num_new_videos = 0
    total_subject = len(subjects.keys())
    
    
    for i, (subject, list_chanel_id)  in enumerate(subjects.items()):
        logger.info(f"[{i}/{total_subject}] Crawling subject: {subject}")
        sub_folder_path = os.path.join(SAVE_DATA_PATH,subject)
        os.makedirs(sub_folder_path, exist_ok=True)
        
        # Chanel_ID
        for channel_id in tqdm(list_chanel_id):
            
            if "@" in channel_id:
                
                channel_id = channel_id[1:]
                name_channel = channel_id
                channel_id = get_channel_id(channel_id)
            else:
                name_channel = channel_id
            
            subsub_folder_path = os.path.join(sub_folder_path,name_channel)
            os.makedirs(subsub_folder_path, exist_ok=True)
            try:
                videos_id = get_videos_id(channel_id)
            except:
                videos_id = []
                logger.warning(f"No videos in chanel {channel_id}")
            
            # Video
            for video_id in videos_id:
                if not historian.is_exist(channel_id, video_id):
                    video_url = get_video_url(video_id)
                    download_thumb(video_url, subsub_folder_path)
                    
                    historian.add(channel_id, video_id)
                    historian.save()
                    num_new_videos += 1

    
    logger.success(f"Crawled new {num_new_videos}")
