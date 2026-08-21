import requests
import json
API_KEY = "AIzaSyAuZjjAeUoA2MBbUUTykr272gHJ9AqJ5Zw"
CHANNEL_HANDLE = "MrBeast"
url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
response = requests.get(url)
data = response.json()
print(json.dumps(data, indent=4))


channel_items = data["items"][0]
channel_playlists = channel_items["contentDetails"]["relatedPlaylists"]["uploads"] 
print(channel_playlists)