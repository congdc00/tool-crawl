from instaloader import Instaloader, Profile 
from glob import glob
import os
import shutil

TMP_FOLDER = "tmp"
SAVE_PATH = "data/input/images/raw_images/instagram"

def crawl_image(profile):
    # L = Instaloader()

    # profile = Profile.from_username(L.context, profile)
    # list_post = profile.get_posts()
    # for post in list_post:
    #     if post.is_video:
    #         continue
    #     L.download_post(post, TMP_FOLDER)

    # list_file = glob(f"{TMP_FOLDER}/*")
    # for file_path in list_file:
    #     if file_path[-3:] != "jpg":
    #         os.remove(file_path)
    save_folder = SAVE_PATH + "/" + profile
    shutil.copytree(TMP_FOLDER, save_folder)

if __name__ == "__main__":
    list_profile = ["baukrysie"]
    total_file = len(list_profile)
    for i, profile in enumerate(list_profile): 
        if os.path.exists(f"{SAVE_PATH}/{profile}"):
            continue
        crawl_image(profile)
