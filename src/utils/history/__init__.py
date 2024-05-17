
from loguru import logger
import json
import os
THUMBS_YOUTUBE = "data/history/youtube/thumbs_crawled.json"
IMAGES_IG = "data/history/instagram/imgs_post.json"

def get_source(mode):
    if mode == "thumbs_youtube":
        return THUMBS_YOUTUBE
    elif mode == "imgs_ig":
        return IMAGES_IG
  
    logger.error(f"Don't have mode {mode}")
    return ""

def get_content(source_path):
    if os.path.exists(source_path):
        with open(source_path, 'r') as file:
            content = json.load(file)
    else:
        content = {}
    
    return content

class Historian:
    
    
    def __init__(self, mode) -> None:
        
        self.mode = mode
        self.source_path = get_source(mode)
        self.content = get_content(self.source_path)
        
        
            
    def is_exist(self, key, value):
        if key in self.content and value in self.content[key]:
            return True
        else:
            return False
    
    def add(self, key, value):
        if key in self.content:
            self.content[key].append(value)
        else:
            self.content[key] = [value]
    
    def save(self):
        with open(self.source_path, 'w') as file:
            json.dump(self.content, file, indent=4)
        
        
        
        
if __name__ == "__main__":
    h = Historian(mode="thumbs_youtube")
    h.add("thu nghiem", "ok2")
    h.save()