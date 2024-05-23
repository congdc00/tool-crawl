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
    
        if content == "":
            continue
        elif content[0] == "#":
            key_process = content[2:]
            subjects[key_process] = []
            continue

        subjects[key_process].append(content)
    
    return subjects
    

