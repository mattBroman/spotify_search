import json
from api import client_id as c_id, client_secret as secret, redirect
import spotipy
import spotipy.util as util


def to_json(struc) :
    """function which converts values returned from SpotifyManager into json
    @param struc: song or playlist returned from spotipy
    @return json representation of that object
    """
    encoder = json.JSONEncoder()
    #TODO format the struc in the way we want to sent to solar
    return encoder.encode(struc)

class SpotifyManager :
    """
    class responsible for handling all spotipy functionality
    contains methods to gather information from particular users spotify
    """

    def __init__(self, username, scope = 'playlist-read-private') :
        """
        constructor function for SpotifyManager class
        @param username: The spotify username of the person whos information is to be downloaded
        @param scope: string of permissions requested from the user, see spotify developer documentation
        """
        self.username = username
        self.scope = scope
        self.token = util.prompt_for_user_token(self.username, self.scope, client_id = c_id, client_secret = secret, redirect_uri=redirect)

    def download_songs(self, playlists) :
        """
        method responsible for extracting song information from a given playlist
        TODO save songs in a file, possibly JSON
        @param playlist: Array containing playlists to download the songs from
        @return Array containing song information.
        """
        if self.token :
            #init file and spotipy.
            sp = spotipy.Spotify(auth =self.token)
            song_data = open('songs.json', 'w')
            songs_arr = []
            songs_dict = {}

            #iteratre through playlists, get tracks
            for playlist in playlists :
                tracks = sp.user_playlist_tracks(self.username, playlist['id'])
                for i, track in enumerate(tracks['items']) :
                    if track['track']['id'] not in songs_dict :
                        features = sp.audio_features(track['track']['id'])[0]
                        song_info = {'album' : track['track']['album']['name'],
                                'artists' : track['track']['artists'][0]['name'],
                                'duration_ms' : track['track']['duration_ms'],
                                'episode' : track['track']['episode'],
                                'external_urls' : track['track']['external_urls'],
                                'id' : track['track']['id'],
                                'name' : track['track']['name'],
                                'popularity' : track['track']['popularity'],
                                'type' : track['track']['type'],
                                'playlists' : [playlist['id']],
                                'key' : features['key'],
                                'mode': features['mode'],
                                'acousticness' : features['acousticness'],
                                'danceability' : features['danceability'],
                                'energy' : features['energy'],
                                'instrumentalness' : features['instrumentalness'],
                                'liveness' : features['liveness'],
                                'speechiness' : features['speechiness'],
                                'valence': features['valence'],
                                'tempo' : features['tempo']}
                        songs_dict[track['track']['id']] = song_info
                        print(i, ' ', track['track']['artists'][0]['name'], track['track']['name'])
                    else :
                        songs_dict[track['track']['id']]['playlists'].append(playlist['id'])
                        print(i, ' ', track['track']['artists'][0]['name'], track['track']['name'])
            
            #place in dict, convert to json, save json
            print(len(songs_dict))
            songs_json = to_json(self.song_format(songs_dict))
            song_data.write(songs_json)
            song_data.close()
            return None
        else :
            print("Can't get token for", self.username)
            return None

    def song_format(self, song_dict) :
        """
        method that converts song dict into an array of dicts to prep for json
        @param song_dict: dictionay of songs
        @return dictionary {'song' : song_arr}   
        """
        song_arr = []
        for key in song_dict.keys() :
            new_song_dict = {'id' : key,
                             'info' : song_dict[key] }
            song_arr.append(new_song_dict)
        return {'songs' : song_arr}         
    def download_user_playlists(self) :
        """
        method responsible for getting information about a users saved playlists
        @return array containing playlist information
        TODO save playlist information in a file, possibly JSON
        """
        if self.token :
            #init file, spotipy, array, and get playlist info
            playlist_data = open('playlist.json', 'w')
            sp = spotipy.Spotify(auth=self.token)
            playlists_arr = []
            playlists = sp.user_playlists(self.username)

            #iterate through getting indvidual playlist info
            for playlist in playlists['items']:
                print(playlist['name'])
                print('total tracks: ', playlist['tracks']['total'])
                playlists_arr.append(playlist)
            
            #place in dict, convert to json, save json
            playlists_dict = {'playlist' : playlists_arr }
            playlist_json = to_json(playlists_dict)
            playlist_data.write(playlist_json)
            playlist_data.close()
            return playlists_arr
        else:
            print ("Can't get token for", self.username )
            return None

if __name__ == '__main__' :
    import sys
    sm = SpotifyManager(sys.argv[1])
    playlist_arr = sm.download_user_playlists()
    tracks_arr = sm.download_songs(playlist_arr)


