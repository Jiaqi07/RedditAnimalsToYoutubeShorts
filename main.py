import praw
from redvid import Downloader
import moviepy.editor as mp
import os
import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

r = praw.Reddit(client_id="---", client_secret="----",
                user_agent="Jiaqi07")

reddit = Downloader(max_q=True)
redditYoutube = []
i = 1

for submission in r.subreddit("aww").top(time_filter="day"):
    if submission.is_video and submission.score > 4000 and submission.media["reddit_video"]["duration"] < 60:
        print(str(submission.title) + ': ' + str(submission))

        reddit.url = submission.url
        reddit.max = True
        reddit.download()

        clip = mp.VideoFileClip(reddit.file_name)
        rclip = clip.resize((1080, 1920))  # convert to youtube shorts format
        rclip.write_videofile('Clip ' + str(i) + '.mp4')

        os.remove(str(reddit.file_name))

        i += 1
        redditYoutube.append(submission)


time, i = (0, 1)
for video in redditYoutube:
    # YOUTUBE UPLOADER
    CLIENT_SECRET_FILE = 'ClientSecretFile.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    upload_date_time = datetime.datetime(2022, 6, 25, 15+time, 0, 0).isoformat() + '.000Z'
    time += 1
    request_body = {
        'snippet': {
            'categoryI': 15,
            'title': str(video.title) + ' #shorts',
            'description': 'Source: ' + str(video.url) + '\nHope you enjoy and consider dropping a like, comment, and a sub!\nAll clips '
                                       'are taken from reddit!',
            'tags': ['Cat', 'Animal', 'Memes', 'Cute', 'Funny', 'Happy', 'Dogs', 'Zoo','Nature', 'Game', 'Furry', 'Pets', 'Love', 'Chill', 'Human', 'Family', 'Minecraft', 'Reddit', 'Subscribe']
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': True
    }

    mediaFile = MediaFileUpload('Clip ' + str(i) + '.mp4')

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    os.remove('Clip ' + str(i) + '.mp4')
    i += 1
