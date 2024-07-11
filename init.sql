CREATE TABLE IF NOT EXISTS channel (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS video (
    id SERIAL PRIMARY KEY,
    channel_id VARCHAR(255) REFERENCES channel(id),
    view_count BIGINT,
    subscriber_count INTEGER,
    video_count INTEGER,
    video_title VARCHAR(255),
    video_description TEXT,
    likes_count INTEGER,
    comments_count INTEGER,
    publication_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS import_task (
    id SERIAL PRIMARY KEY,
    date_start TIMESTAMP,
    date_end TIMESTAMP,
    created_videos INTEGER,
    updated_videos INTEGER,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
