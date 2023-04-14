from fastapi import FastAPI
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import List
from pydantic import BaseModel


app = FastAPI()

#Spotify API client
client_id = "486ff539243b4134812372998e3e354a"
client_secret = "e2766ab794cd4857a06ffb86e8a760f5"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class SpotifyImage(BaseModel):
    height: int
    width: int
    url: str

class SpotifyAlbum(BaseModel):
    name: str
    album_type: str
    id: str
    images: List[SpotifyImage]
    release_date: str

class SpotifyTrack(BaseModel):
    name: str
    id: str
    album: SpotifyAlbum
    popularity: int

class SpotifyArtist(BaseModel):
    name: str
    id: str
    type: str
    followers: int
    popularity: int
    images: List[SpotifyImage]
    albums: List[SpotifyAlbum]
    top_tracks: List[SpotifyTrack]

@app.get("/artists/{artist_name}")
async def get_artist(artist_name: str):
    # Search for artist by name
    result = sp.search(q=artist_name, type='artist')
    artist_data = result['artists']['items'][0]

    # Get artist's image
    images = [SpotifyImage(**img) for img in artist_data['images']]

    # Get artist's albums
    albums_data = sp.artist_albums(artist_data['id'], album_type='album')['items']
    albums = [SpotifyAlbum(**album) for album in albums_data]

    # Get artist's top tracks
    top_tracks_data = sp.artist_top_tracks(artist_data['id'])['tracks']
    top_tracks = [SpotifyTrack(**track) for track in top_tracks_data]

    # Create SpotifyArtist instance
    artist = SpotifyArtist(
        name=artist_data['name'],
        id=artist_data['id'],
        type=artist_data['type'],
        followers=artist_data['followers']['total'],
        popularity=artist_data['popularity'],
        images=images,
        albums=albums,
        top_tracks=top_tracks
    )

    # Return artist information 
    return artist.dict() 
