from pymongo import MongoClient

db_connection = MongoClient("mongodb+srv://asktu:d7iFv8X8wNIuACXJ@cluster0.rukamcb.mongodb.net/AskTuDB?retryWrites=true&w=majority" ,
)

db = db_connection["Sila"]

user_collection = db["users"]

artist_collection = db["artists"]

album_collection = db["albums"]

song_collection = db["songs"]

playlist_collection = db["playlists"]


