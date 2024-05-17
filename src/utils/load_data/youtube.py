from src.crawl.youtube.videos import get_channel_id
from tqdm import tqdm
import time


def load_info(file_path, type="subject"):
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    key_process = ""
    subjects = {}

    for line in tqdm(lines):
        content = line.strip()
        if "@" in content:
            channel_name = content[1:]
            channel_id = get_channel_id(channel_name)
            
        elif content == "":
            continue
        elif content[0] == "#":
            key_process = content[2:]
            subjects[key_process] = []
            continue
        else:
            channel_id = content
        subjects[key_process].append(channel_id)
    
    return subjects
    

