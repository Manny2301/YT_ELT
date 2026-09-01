import requests
import json
import os
from datetime import date
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
maxResults = 50
def get_playlist_id():
    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        channel_items = data["items"][0]
        channel_playlists = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlists)
        return channel_playlists
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching playlist ID: {e}")
        return None

def get_video_ids(playlist_id):
    video_ids = []
    pageToken = None
    base_url =f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}"
    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data.get('items',[]):
                video_ids.append(item["contentDetails"]["videoId"])
            pageToken = data.get("nextPageToken")
            if not pageToken:
                break
        return video_ids

    except requests.exceptions.RequestException as e:
        raise e


def batch_list(video_ids_lst, batch_size=50):
   
   for video_id in range(0, len(video_ids_lst), batch_size):
        yield video_ids_lst[video_id:video_id + batch_size]

f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id=v1ELS84GQu8&key=[YOUR_API_KEY]"

def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_ids_lst, batch_size=50):
   
       for video_id in range(0, len(video_ids_lst), batch_size):
        yield video_ids_lst[video_id:video_id + batch_size]


   
    try:
        for batch in batch_list(video_ids,maxResults):
            video_ids_str = ",".join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for item in data.get("items", []):
            video_id = item["id"]
            snippet = item["snippet"]
            statistics = item["statistics"]
            contentDetails = item["contentDetails"]
            video_data = {
                "video_id": video_id,
                "title": snippet["title"],
                "published_at": snippet["publishedAt"],
                "duration": contentDetails["duration"],
                "view_count": statistics.get("viewCount", None),
                "like_count": statistics.get("likeCount", None),
                "comment_count": statistics.get("commentCount", None)
                
                    
            }

            extracted_data.append(video_data)
        return extracted_data
        
    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(extracted_data):
    file_path=f"./data/YT_data_{date.today()}.json"

    with open(file_path, "w",encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, indent=4, ensure_ascii=False)
    

if __name__== "__main__":
    playlistId = get_playlist_id()
    videoIds = get_video_ids(playlistId)
    video_data=extract_video_data(videoIds)
    save_to_json(video_data)

    
    

