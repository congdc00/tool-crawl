import ffmpeg
import datetime 
import os
from core.log.logger import Logger
def convert_time(time_string: str):
    time_object = datetime.datetime.strptime(time_string, "%H:%M:%S")
    seconds = time_object.second + time_object.minute * 60 + time_object.hour * 3600
    return seconds

def split(input_path,index_sections ,sections):

    is_split = False

    for i, section in enumerate(sections):
        start_time = convert_time(section[0])
        end_time = convert_time(section[1])

        # output name
        list_tmp = input_path.split(".")
        output_path = f".{list_tmp[1]}"
        format = list_tmp[2]
        output_name = output_path + f"_{int(index_sections[i]):02d}" + f".{format}"
        Logger.write_log(f"[Split] {output_name}")
        
        # cut video
        ffmpeg.input(input_path, ss=start_time, to=end_time).output(output_name).run(quiet = True, overwrite_output=True)
        is_split = True
    
    if is_split:
        if os.path.exists(input_path):
            os.remove(input_path)
            Logger.write_log(f"[Delete] {input_path}")
    

