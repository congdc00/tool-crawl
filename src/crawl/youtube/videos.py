from yt_dlp import YoutubeDL
import time
from googleapiclient.discovery import build

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import requests
import os
import yaml
from loguru import logger

SAVE_DATA_PATH = "data/input/images/raw_images/thumb-youtube"
CONFIG_PATH  = "env/config.yaml"

with open(CONFIG_PATH, 'r') as file:
    config = yaml.safe_load(file)

api_key = config.get('api_key')[0].get('youtube')
youtube_dev=build(
    'youtube',
    'v3',
    developerKey=api_key
)

def is_short(id_video):
    ''' Kiểm tra xem có phải video Youtube Short không
    '''
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/shorts/{id_video}"

    payload = ""
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    content = response.json()
    height = int(content['height'])
    width = int(content['width'])

    if height < width:
        return False
    else:
        return True
    
def get_channel_id(channel_name):
    ''' Lấy channel_id theo tên kênh
    '''
    url = f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={channel_name}&type=channel&key={api_key}'
    d = requests.get(url).json()
    channel_id = d['items'][0]['snippet']['channelId']
    return channel_id

def get_videos_id(channel_id):
    ''' Lấy danh sách toàn bộ các videos youtube từ một kênh
    '''
    
    request = youtube_dev.channels().list(
        part='contentDetails',
        id=channel_id
    )

    response=request.execute()
    etag = response['etag']
    request = youtube_dev.channels().list(
            part='contentDetails',
            id=etag
        )
    playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos = []
    next_page_token = None

    while True:
        playlist_items_response=youtube_dev.playlistItems().list(
                    #part='contentDetails',
                    part='snippet',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
        ).execute()

        videos += playlist_items_response['items']
        next_page_token = playlist_items_response.get('nextPageToken')
        if not next_page_token:
            break
        
    video_ids = []
    for video in videos:
        video_id = video['snippet']['resourceId']['videoId']
        if not is_short(video_id):
            video_ids.append(video_id)

    return video_ids

def get_video_url(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"

def download_video (video_url, target_path):
    list_tmp = target_path.split(".")
    output_path = f".{list_tmp[1]}"
    format = list_tmp[2]
    ydl_opts = {
        "quiet": True,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best", #format,
        "outtmpl": f"{output_path}.%(ext)s",
        "restrictfilenames": True,
    }
    
    start_time = time.time()

    try:
        with YoutubeDL(ydl_opts) as ydl:
            is_done = ydl.download([video_url])
    except:
        return "False"

    end_time = time.time()
    runtime = end_time - start_time
  
    if runtime < 3:
        return "Skip"
    else:
        return "Done"
