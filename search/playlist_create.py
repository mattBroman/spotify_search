import spotipy as sp
import api

class Playlist_Create:

    def __init__(self, username:str, playlist:str, description:str):
        self.username
        self.token = None
        self.username = username
        self.playlist = playlist
        self.description = description

    def authenticate(self):
        if self.username is None:
            print("ERROR: Must input a username!!")
            return
        return

