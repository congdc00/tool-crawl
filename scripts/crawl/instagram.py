from instaloader import Instaloader, Profile 
from glob import glob
import os
import shutil
from src.utils.history import Historian
from src.utils.load_data.youtube import load_info
from loguru import logger
from tqdm import tqdm
from pathlib import Path
SAVE_DATA_PATH = "data/output/"
SOURCE_PROFILE= "data/source/instagram/girl.txt"
TMP_PATH = "tmp"
def crawl_image(profile, historian, sub_folder_path):
    
    profile_path = os.path.join(sub_folder_path, profile)
    os.makedirs(profile_path, exist_ok=True)
    
    
    
    L = Instaloader(quiet=True, download_comments=False, download_geotags=False, download_videos=False, save_metadata=False, compress_json=False)

    profile = Profile.from_username(L.context, profile )
    list_post = profile.get_posts()
    num_new_post = 0
    os.makedirs(TMP_PATH, exist_ok=True)
    for post in tqdm(list_post):
        if post.is_video or historian.is_exist(post.owner_id, post.shortcode):
            continue
        L.download_post(post, TMP_PATH)
        historian.add(post.owner_id, post.shortcode)
        historian.save()
        num_new_post += 1
        break

    # clear folder
    list_file = glob(f"{TMP_PATH}/*")
    for file_path in list_file:
        if not Path(file_path).suffix != ".jpg":
            dist_path = file_path.replace(TMP_PATH, profile_path)
            print(f"move {file_path} to {dist_path}")
            shutil.move(file_path, dist_path)
    shutil.rmtree(TMP_PATH)
    return num_new_post
    
if __name__ == "__main__":
    
    historian = Historian(mode="imgs_ig")
    
    logger.info(f"Load subjects")
    profiles = load_info(SOURCE_PROFILE)
    
    logger.info(f"Download")
    total_file = len(profiles)
    num_new_post = 0
    for i, (subject, list_profile)  in enumerate(profiles.items()):
        logger.info(f"Crawling subject: {subject}")
        sub_folder_path = os.path.join(SAVE_DATA_PATH,subject)
        os.makedirs(sub_folder_path, exist_ok=True)
    
        for profile in tqdm(list_profile):
            logger.info(f"[{i}/{total_file}] Crawling profile: {profile}")
            
            num_new_post += crawl_image(profile, historian, sub_folder_path)

    logger.success(f"Crawled new {num_new_post}")