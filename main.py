import os 
import shutil
import yaml
from loguru import logger
import argparse
import threading
import time
from datetime import datetime 
start_time = time.time()
import json
from core.crawler import crawl
from core.log.logger import Logger,INFO_PATH  

DS_CONFIG = "./config/general.yaml"

def prepare_workspace(redownload):
    with open(DS_CONFIG, "r") as f:
        config = yaml.safe_load(f)
        for folder in config["directory"]:
            
            folder_path = config["directory"][folder]
            name_folder = os.path.basename(folder_path)
            if redownload and name_folder != "source_data" and os.path.exists(folder_path):
                shutil.rmtree(folder_path)
    
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
    logger.info("Workspace: OK")



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--redownload", action="store_true", help="Khởi chạy lại")
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = get_args()
    prepare_workspace(args.redownload)
    Logger.create_log_path()
    crawl()

    # check_time
    total_time = "0:00:00"
    total_time = datetime.strptime(total_time, "%H:%M:%S")
    with open(INFO_PATH, "r+") as f:
        data = json.load(f)
        list_video = data["videos"]
        for video in list_video:
            num_section = len(video) - 1
            for i in range(0,num_section):
                section = video[f"section_{i:02d}"]
                time_start = datetime.strptime(section[0], "%H:%M:%S") 
                time_end = datetime.strptime(section[1], "%H:%M:%S")
                delta_time = time_end - time_start
                total_time = total_time + delta_time
        total_time = str(total_time)
        logger.info(f"Time video: {total_time.split(' ')[-1]}")
    
    end_time = time.time()
    runtime = end_time - start_time
    logger.success(f"Done in {runtime:.2f} seconds")

