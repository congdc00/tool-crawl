import time
import os
import json 

INFO_PATH = "./log/info.json"

def find_index(info_json, key, value):
    dictionary = info_json["videos"]
    for i, content in enumerate(dictionary):
        if content[key] == value:
            return i 
    return None

class Logger():
    
    log_path = ""

    @staticmethod
    def create_log_path():
        now = time.time()
        time_now = time.strftime("%Y%m%d_%H_%M_%S", time.localtime(now))
        name_file = f"{time_now}.txt"
        Logger.log_path = f"./log/system/{name_file}"
        os.mknod(Logger.log_path)

    def get_log_path():
        return Logger.log_path

    def write_log(content):
        with open(Logger.log_path, "r+") as f:  
           f.seek(0,2)
           f.write(f"{content}\n")
            
    def update_info(url, info_del, info_reindex, info_split):
        
        if not os.path.exists(INFO_PATH):
            os.mknod(INFO_PATH)
            with open(INFO_PATH, "w") as f:
                template = {}
                i_sections = info_split[0]
                value_sections = info_split[1]
                template["url"] = url
                for i_section, value_section in zip(i_sections, value_sections):
                    template[f"section_{i_section}"] = value_section
                json.dump({"videos": [template]}, f)

                return "" 

        
        with open(INFO_PATH, "r") as f:
            history = dict(json.load(f))
            index = find_index(history, "url", url)
            if index == None:
                history["videos"].append({"url": url})
                index = -1
        
        with open(INFO_PATH, "w") as f:
            # del
            for i_section in info_del:
                del history["videos"][index][f"section_{i_section:02d}"]

            # reindex
            i_sections_old = info_reindex[0]
            i_sections_new = info_reindex[1]
            for i_section_old,i_section_new in zip(i_sections_old, i_sections_new):
                history["videos"][index][f"section_{int(i_section_new):02d}"] = history["videos"][index][f"section_{int(i_section_old):02d}"]
                del history["videos"][index][f"section_{int(i_section_old):02d}"]

            # split 
            i_sections = info_split[0]
            value_sections = info_split[1]
            for i_section, value_section in zip(i_sections, value_sections):
                history["videos"][index][f"section_{i_section:02d}"] = value_section


            json.dump(history, f)
