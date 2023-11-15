from glob import glob
import os
import json
from loguru import logger
from core.downloader import download
from core.cutter import split
from core.log.logger import Logger, INFO_PATH 

LANGUAGE = "vietnamese"
VIDEO_PATH = f"./source_data/videos/{LANGUAGE}/"
OUTPUT_PATH = f"./data/videos/{LANGUAGE}/"
TYPE_VIDEO = ["youtube",]

def get_select_source_link(source_video):
    list_link_video = glob(f"{source_video}/*")
    list_link_video_choice = []        
    for link_video in list_link_video:
        for type_video in TYPE_VIDEO:
            if type_video in link_video:
                list_link_video_choice.append(link_video)
                break
    return list_link_video_choice

def del_sections(video_root_path, index_sections):
    tmp = video_root_path.split(".")
    for index_section in index_sections:
        video_target_path = f".{tmp[1]}_{index_section:02d}.{tmp[2]}"
        if os.path.exists(video_target_path):
            os.remove(video_target_path)
        Logger.write_log(f"[Change] Delete {video_target_path}")

def reindex(video_root_path, index_sections_root, index_sections_target):
    tmp = video_root_path.split(".")
    for index_section_root, index_section_target in zip(index_sections_root, index_sections_target):
        video_section_root_path = f".{tmp[1]}_{index_section_root:02d}.{tmp[2]}" 
        video_section_target_path = f".{tmp[1]}_{index_section_target:02d}.{tmp[2]}"
        os.rename(video_section_root_path, video_section_target_path)
        Logger.write_log(f"[Change] Reindex {video_section_root_path.split('/')[-1]} to {video_section_target_path.split('/')[-1]}")
def get_action(info_video, info_log_path):
    index_sections_del = []
    index_sections_root = []
    index_sections_target = []
    index_sections_need_split = []
    sections_need_split = []
    skip_split = []
    
    if not os.path.exists(info_log_path):
        sections_need_split = info_video["sections"]
        index_sections_need_split = []
        for i in range(len(info_video["sections"])):
            index_sections_need_split.append(f"{i:02d}")
        return index_sections_del, [index_sections_root, index_sections_target], [index_sections_need_split, sections_need_split]

    with open(info_log_path, "r") as f:
        info_json = json.load(f)
        dictionary = info_json["videos"]
        is_new = True
        for content in dictionary:
            if content["url"] == info_video["url"]:
                is_new = False

                if is_new == False:
                # checkdel
                    for i in range(len(content)-1):
                        is_del = True
                        section = content[f"section_{i:02d}"]
                        section_start = section[0]
                        section_end = section[1]
                        for j, info_section in enumerate( info_video["sections"]):
                            s_start = info_section[0]
                            s_end = info_section[1]
                            if section_start == s_start and section_end == s_end:
                                # check reindex
                                if i != j:
                                    index_sections_root.append(i)
                                    index_sections_target.append(j)
                                elif i == j:
                                    skip_split.append(i)
                                is_del = False
                                break

                        if is_del:
                            index_sections_del.append(i)

                # check create section
                for i, info_section in enumerate(info_video["sections"]):
                    if i in index_sections_target or i in skip_split:
                        continue
                    index_sections_need_split.append(i)
                    sections_need_split.append([info_section[0],info_section[1]])
                
                break
        if is_new:
            sections_need_split = info_video["sections"]
            index_sections_need_split = list(range(len(info_video["sections"])))

    return index_sections_del,[index_sections_root, index_sections_target], [index_sections_need_split, sections_need_split]

def crawl():

    # check workspace
    list_folder = OUTPUT_PATH.split("/")
    for i in range(1, len(list_folder)):
        target_path = "/".join(list_folder[:i])
        if not os.path.exists(target_path):
            os.mkdir(target_path)

    list_source_video = glob(f"{VIDEO_PATH}*")
    total_source = len(list_source_video)
    for index_video, source_video in enumerate(list_source_video, start=1): 
        
        logger.info(f"[{index_video}/{total_source}] Author: {os.path.basename(source_video)}")

        # checkfolder
        name_folder = os.path.basename(source_video)
        target_path = f"{OUTPUT_PATH}{name_folder}"
        if not os.path.exists(target_path):
            os.mkdir(target_path)

        list_link_video = get_select_source_link(source_video)
        for i, link_video in enumerate(list_link_video, start=1):
            print(f"Craw from {link_video.split('_')[-1].split('.')[0]}")
            with open(link_video, "r") as f:   
                data = json.load(f)
                list_video_info = data["videos"]
            
            for j, video_info in enumerate(list_video_info, start=1):
                print(f"[{j}/{len(list_video_info)}]")

                Logger.write_log(f"--------------------------")
                Logger.write_log(f"Url: {video_info['url']}")

                index_sections_del,[index_sections_root, index_sections_target], [index_sections_need_split, sections_need_split] = get_action(video_info, INFO_PATH)
                
                output_path = f"{target_path}/{i}{j:03d}.mp4"
                if len(index_sections_need_split) > 0:
                    download(video_info["url"], output_path)
                    Logger.write_log(f"[Download] Done")
                                 
                del_sections(output_path, index_sections_del) 
                reindex(output_path, index_sections_root, index_sections_target)
                split(output_path,index_sections_need_split ,sections_need_split)

                Logger.update_info(video_info["url"], index_sections_del, [index_sections_root, index_sections_target], [index_sections_need_split, sections_need_split])
        
        
    

            
    
    
    
    

