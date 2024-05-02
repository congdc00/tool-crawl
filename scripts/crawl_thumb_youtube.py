from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pythumb import Thumbnail
from tqdm import tqdm
import requests
import os
# config
from loguru import logger
api_key='AIzaSyArrDaKne-G_649UGiN3sMCq6F25xzTUQk'
file_path = 'data/input/source/YoutubeChannels.txt'
SAVE_DATA_PATH = "data/input/images/raw_images/thumb-youtube"

youtube=build(
    'youtube',
    'v3',
    developerKey=api_key
)

def is_short(id_video):
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

def get_videos(type_id, channel_id):
    print("Download from ", channel_id)
    if type_id == "name":
        url = f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={channel_id}&type=channel&key={api_key}'
        d = requests.get(url).json()
        channel_id = d['items'][0]['snippet']['channelId']
    
    request = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    )

    response=request.execute()
    etag = response['etag']
    request = youtube.channels().list(
            part='contentDetails',
            id=etag
        )
    playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos = []
    next_page_token = None

    while True:
        playlist_items_response=youtube.playlistItems().list(
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
    video_urls = []
    for video in videos:
        video_id = video['snippet']['resourceId']['videoId']
        if is_short(video_id):
            continue
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_urls.append(video_url)

    return video_urls

if __name__ == "__main__":

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        channel = line.strip()

        if "@" in channel:
            channel = channel[1:]
            type_name = "name"
        elif channel == "":
            break
        elif channel[0] == "#":
            continue
        else:
            type_name = "id"

        folder_path = SAVE_DATA_PATH + "/" + channel
        if os.path.exists(folder_path):
            continue
        os.makedirs(folder_path, exist_ok=True)
        try:
            list_videos = get_videos(type_name, channel)
        except:
            continue
        for link in tqdm(list_videos):
            t = Thumbnail(link)
            t.fetch()
            try:
                t.save(f'{folder_path}')
            except:
                continue

    logger.info("Crawl done")
