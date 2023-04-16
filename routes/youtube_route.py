# pip3 install google-api-python-client

#client id = 609992228344-n2cljdiihm2mm050psieumeek19l4dud.apps.googleusercontent.com
#client secret = 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

from typing import Union
from fastapi import FastAPI
from googleapiclient.discovery import build

app = FastAPI()

api_key = 'AIzaSyCkjFgBIIxvxOcrbzbphdSOgI8bpXCOa5g'

youtube = build('youtube', 'v3', developerKey=api_key)

categoryID='10'

@app.get("/artists_yt/{artist_name}")
async def get_data(artist_name: str):

    #default of result is the first video on feed from search
    #could change to order by viewCount so result will be the most view from keyword
    search=youtube.search().list(
        part='snippet,id',
        q=artist_name,
        maxResults='1',
        type='video',
        regionCode='TH',
        videoCategoryId=categoryID).execute()

    channel_name = search['items'][0]['snippet']['channelTitle']
    channel_Id = search['items'][0]['snippet']['channelId']
    video_Id = search['items'][0]['id']['videoId']
    video_name = search['items'][0]['snippet']['title']

    #channel data
    channel_detail = youtube.channels().list(
        part = 'statistics',
        id = channel_Id
    ).execute()

    ch_sub = channel_detail['items'][0]['statistics']['subscriberCount']

    ch_view = channel_detail['items'][0]['statistics']['viewCount']

    ch_videoCount = channel_detail['items'][0]['statistics']['videoCount']

    video = youtube.videos().list(
        part = 'statistics',
        id = video_Id).execute()

    #show view count from the first search's result 
    #could add likeCount ,commentCount 
    stat = video['items'][0]['statistics']['viewCount']

    return artist_name,video_name,stat ,channel_name,ch_sub,ch_view
