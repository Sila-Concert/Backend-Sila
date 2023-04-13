from pymongo import MongoClient

db_connection = MongoClient("mongodb://localhost:27017")

db = db_connection["Sila"]

user_collection = db["users"]

artist_collection = db["artists"]

album_collection = db["albums"]

song_collection = db["songs"]

playlist_collection = db["playlists"]


