import os
import csv
import psycopg2
from datetime import datetime

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
LOCAL_STORAGE_PATH = "/app/local_storage"
DEBUG_LOG_FILE = "/app/local_storage/debug.log"

def log_debug_message(message):
    with open(DEBUG_LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")

def get_latest_csv():
    csv_files = [f for f in os.listdir(LOCAL_STORAGE_PATH) if f.endswith('.csv')]
    if not csv_files:
        return None
    return max(csv_files, key=lambda x: os.path.getctime(os.path.join(LOCAL_STORAGE_PATH, x)))

def process_csv(filename):
    data = []
    with open(os.path.join(LOCAL_STORAGE_PATH, filename), 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def insert_into_db(data):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    
    created_videos = 0
    updated_videos = 0
    
    for row in data:
        log_debug_message(f"Processing row: {row}")
        
        cursor.execute(
            """
            INSERT INTO channel (id, title, description)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description
            """,
            (row['channel_id'], row['channel_title'], row['channel_description'])
        )
        
        cursor.execute(
            """
            INSERT INTO video (channel_id, view_count, subscriber_count, video_count, video_title, video_description, likes_count, comments_count, publication_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row['channel_id'], row['view_count'], row['subscriber_count'],
                row['video_count'], row['video_title'], row['video_description'],
                row['likes_count'], row['comments_count'], row['publication_date']
            )
        )
        created_videos += 1
    
    cursor.execute(
        """
        INSERT INTO import_task (date_start, date_end, created_videos, updated_videos, status)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (datetime.now(), datetime.now(), created_videos, updated_videos, 'succeeded')
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    log_debug_message(f"Data inserted into database. Created videos: {created_videos}, Updated videos: {updated_videos}")

def run_processing_job():
    latest_csv = get_latest_csv()
    if latest_csv:
        log_debug_message(f"Processing CSV file: {latest_csv}")
        data = process_csv(latest_csv)
        insert_into_db(data)
    else:
        log_debug_message("No CSV file found")

if __name__ == "__main__":
    run_processing_job()
