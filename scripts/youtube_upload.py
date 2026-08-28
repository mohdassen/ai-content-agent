import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

VIDEO = os.getenv('VIDEO_FILE', 'video.mp4')
TITLE = os.environ['YT_TITLE']
DESCRIPTION = os.getenv('YT_DESCRIPTION', '')
PRIVACY = os.getenv('YT_PRIVACY', 'private')
TAGS = [x.strip() for x in os.getenv('YT_TAGS', '').split(',') if x.strip()]

creds = Credentials(
    token=None,
    refresh_token=os.environ['YT_REFRESH_TOKEN'],
    token_uri='https://oauth2.googleapis.com/token',
    client_id=os.environ['YT_CLIENT_ID'],
    client_secret=os.environ['YT_CLIENT_SECRET'],
    scopes=['https://www.googleapis.com/auth/youtube.upload'],
)

youtube = build('youtube', 'v3', credentials=creds)
body = {
    'snippet': {
        'title': TITLE,
        'description': DESCRIPTION,
        'tags': TAGS,
        'categoryId': '28'
    },
    'status': {
        'privacyStatus': PRIVACY,
        'selfDeclaredMadeForKids': False
    }
}
request = youtube.videos().insert(
    part='snippet,status',
    body=body,
    media_body=MediaFileUpload(VIDEO, chunksize=-1, resumable=True)
)
response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f'Upload progress: {int(status.progress()*100)}%')
video_id = response['id']
print(f'YOUTUBE_VIDEO_ID={video_id}')
print(f'https://www.youtube.com/watch?v={video_id}')
