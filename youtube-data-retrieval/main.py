import os
import csv
from datetime import datetime
from googleapiclient.discovery import build
from auth import get_credentials
from storage import upload_to_bucket
from fastapi import FastAPI
import uvicorn

# from youtube_api import YoutubeAPIService

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_IDS = ["UCAcAnMF0OrCtUep3Y4M-ZPw", "UCjRqDyF6BnpE7_FW9TuMZlw", "UCWeg2Pkate69NFdBeuRFTAw"]
LOCAL_STORAGE_PATH = "/app/local_storage"
DEBUG_LOG_FILE = "/app/local_storage/debug.log"

def log_debug_message(message):
    with open(DEBUG_LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")

def get_youtube_data():
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    data = []
    for channel_id in CHANNEL_IDS:
        channel_request = youtube.channels().list(part="snippet,statistics", id=channel_id)
        channel_response = channel_request.execute()
        channel_data = channel_response['items'][0]
        
        # Get the latest video from the channel
        search_request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            type="video",
            order="date",
            maxResults=1
        )
        search_response = search_request.execute()
        
        if search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            video_request = youtube.videos().list(part="statistics,snippet", id=video_id)
            video_response = video_request.execute()
            video_data = video_response['items'][0]
            
            data.append({
                'channel_id': channel_id,
                'channel_title': channel_data['snippet']['title'],
                'channel_description': channel_data['snippet']['description'],
                'subscriber_count': channel_data['statistics']['subscriberCount'],
                'video_count': channel_data['statistics']['videoCount'],
                'video_title': video_data['snippet']['title'],
                'video_description': video_data['snippet']['description'],
                'view_count': video_data['statistics']['viewCount'],
                'likes_count': video_data['statistics'].get('likeCount', 0),
                'comments_count': video_data['statistics'].get('commentCount', 0),
                'publication_date': video_data['snippet']['publishedAt']
            })
    return data

def save_to_csv(data, nb_days, keysearch, local_file_path):
    end_datetime = datetime.datetime.now(datetime.timezone.utc)
    start_datetime = end_datetime - datetime.timedelta(days=nb_days)
    local_file_path = f'{start_datetime.strftime("%Y-%m-%d")}_{end_datetime.strftime("%Y-%m-%d")}_{keysearch}_videos.csv'
    
    fieldnames = [
        'channel_id', 'channel_title', 'channel_description',
        'subscriber_count', 'video_count', 'video_title', 
        'video_description', 'view_count', 'likes_count', 
        'comments_count', 'publication_date'
    ]
    
    with open(local_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            log_debug_message(f"Processing item: {item}")
            filtered_item = {key: item.get(key, '') for key in fieldnames}
            writer.writerow(filtered_item)
    log_debug_message(f"Data saved to {local_file_path}")



app = FastAPI()

@app.get("/trigger-youtube-api-job")
async def retrieve_new_video_data():
    nb_days = 1
    local_credentials_path = 'credentials.json'
    keysearch = "epita"
    credentials = get_credentials(local_credentials_path)
    bucket_name = 'epita-tp1-muchachos' # do not give gs:// ,just bucket name
    end_datetime = datetime.datetime.now(datetime.timezone.utc)
    start_datetime = end_datetime - datetime.timedelta(days=nb_days)
    local_file_path = f'{start_datetime.strftime("%Y-%m-%d")}_{end_datetime.strftime("%Y-%m-%d")}_{keysearch}_videos.csv'
    blob_path = f'daily_search/{local_file_path}'
    project = 'My Fist Project'
    data = get_youtube_data()
    log_debug_message(f"Data retrieved: {data}")
    save_to_csv(data, nb_days=nb_days, keysearch=keysearch, local_file_path=local_file_path)
    upload_to_bucket(project, credentials, bucket_name, blob_path, local_file_path)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
