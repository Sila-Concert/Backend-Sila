
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

    return artist_name,video_name,stat ,channel_name,ch_sub,ch_view,ch_videoCount

@app.get("/comment_yt/{artist_name}")
async def get_comment(artist_name: str):
    search = youtube.search().list(
        part='snippet,id',
        q=artist_name,
        maxResults='1',
        type='video',
        regionCode='TH',
        videoCategoryId=categoryID).execute()

    video_Id = search['items'][0]['id']['videoId']
    video_name = search['items'][0]['snippet']['title']

    # could select to show comment from video or from channel
    # could add searchTerms to show comment with keyword e.g.'consert'

    # show from video
    result_num = 5
    comment_top = youtube.commentThreads().list(
        part='snippet',
        videoId = video_Id,
        maxResults = result_num,
        order = 'relevance',
        textFormat = 'plainText'
    ).execute()

    comment_result=[]

    # show only comments's text
    for i in range(result_num):
        comment_result.append(comment_top['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay'])
    
    return  video_name,comment_result
    


@app.get("/popular")

def get_chart():

    request = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        regionCode="TH",
        videoCategoryId="10",
        maxResults="10"
    )
    response = request.execute()

    # show only videos's name 
    # could change to show other
    chart =[]
    for i in range(10):
        chart.append(response['items'][i]['snippet']['title'])

    return chart
