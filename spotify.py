import json
from api import client_id as c_id, client_secret as secret, redirect
import spotipy
import spotipy.util as util
import os
import shutil


def to_json(struc):
    """function which converts values returned from SpotifyManager into json
    @param struc: song or playlist returned from spotipy
    @return json representation of that object
    """
    encoder = json.JSONEncoder()
    # TODO format the struc in the way we want to sent to solar
    return encoder.encode(struc)


class SpotifyManager:
    """
    class responsible for handling all spotipy functionality
    contains methods to gather information from particular users spotify
    """

    def __init__(self, username, scope='playlist-read-private'):
        """
        constructor function for SpotifyManager class
        @param username: The spotify username of the person whos information is to be downloaded
        @param scope: string of permissions requested from the user, see spotify developer documentation
        """
        self.username = username
        self.scope = scope
        self.token = util.prompt_for_user_token(self.username, self.scope, client_id=c_id, client_secret=secret,
                                                redirect_uri=redirect)
        self.root_dir = "Song_json/"

    # This is the original download_songs function Matt wrote. I didn't want to delete/break it so I copied it
    # to make my changes and commented it out in case I mess up and need this again
    # def download_songs(self, playlists) :
    #     """
    #     method responsible for extracting song information from a given playlist
    #     TODO save songs in a file, possibly JSON
    #     :param playlist: Array containing playlists to download the songs from
    #     :return: Array containing song information.
    #     """
    #     if self.token :
    #         #init file and spotipy.
    #         sp = spotipy.Spotify(auth =self.token)
    #         song_data = open('songs.json', 'w')
    #         songs_arr = []
    #         songs_dict = {}
    #
    #         #iteratre through playlists, get tracks
    #         for playlist in playlists :
    #             tracks = sp.user_playlist_tracks(self.username, playlist['id'])
    #             for i, track in enumerate(tracks['items']) :
    #                 if track['track']['id'] not in songs_dict :
    #                     features = sp.audio_features(track['track']['id'])[0]
    #                     song_info = {'album' : track['track']['album']['name'],
    #                             'artists' : track['track']['artists'][0]['name'],
    #                             'duration_ms' : track['track']['duration_ms'],
    #                             'episode' : track['track']['episode'],
    #                             'external_urls' : track['track']['external_urls'],
    #                             'id' : track['track']['id'],
    #                             'name' : track['track']['name'],
    #                             'popularity' : track['track']['popularity'],
    #                             'type' : track['track']['type'],
    #                             'playlists' : [playlist['id']],
    #                             'key' : features['key'],
    #                             'mode': features['mode'],
    #                             'acousticness' : features['acousticness'],
    #                             'danceability' : features['danceability'],
    #                             'energy' : features['energy'],
    #                             'instrumentalness' : features['instrumentalness'],
    #                             'liveness' : features['liveness'],
    #                             'speechiness' : features['speechiness'],
    #                             'valence': features['valence'],
    #                             'tempo' : features['tempo']}
    #                     songs_dict[track['track']['id']] = song_info
    #
    #                     # Write individual song to flat json file
    #                     self.write_indiv_json(song_info)
    #                     print(i, ' ', track['track']['artists'][0]['name'], track['track']['name'])
    #                 else :
    #                     songs_dict[track['track']['id']]['playlists'].append(playlist['id'])
    #                     print(i, ' ', track['track']['artists'][0]['name'], track['track']['name'])
    #
    #         #place in dict, convert to json, save json
    #         print(len(songs_dict))
    #         songs_json = to_json(self.song_format(songs_dict))
    #         song_data.write(songs_json)
    #         song_data.close()
    #         return None
    #     else :
    #         print("Can't get token for", self.username)
    #         return None

    def download_songs(self, playlists, output_folder:str):
        """
        method responsible for extracting song information from a given playlist
        Writes the information of every song to its own unique json file
        :param playlist: Array containing playlists to download the songs from
        :return: Array containing song information.
        """
        if self.token :
            #init file and spotipy and create an output folder for all of the song files
            self.create_json_folder(output_folder)
            sp = spotipy.Spotify(auth =self.token)
            song_data = open('songs.json', 'w')
            songs_arr = []
            songs_dict = {}

            #iteratre through playlists, get tracks
            for playlist in playlists :
                print('playlist: ', playlist['name'])
                tracks = sp.user_playlist_tracks(self.username, playlist['id'])
                for i, track in enumerate(tracks['items']):
                    if track['track']['id'] not in songs_dict:
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
                        if not song_info['id'] :
                            print (song_info['name'])
                        songs_dict[track['track']['id']] = song_info
                        print(i, ' ', track['track']['artists'][0]['name'], track['track']['name'])
                    else:
                        songs_dict[track['track']['id']]['playlists'].append(playlist['id'])
                        print(i, ' ', track['track']['artists'][0]['name'], track['track']['name'])

            #place in dict, convert to json, save json
            print(len(songs_dict))
            # Write each individual song to its own json file
            song_file_array = self.write_indiv_json(output_folder, songs_dict)
            print("Number of files we got: ", len(song_file_array))
            return None
        else :
            print("Can't get token for", self.username)
            return None
            
    def write_indiv_json(self, output_folder:str, song_info:dict):
        """
        Takes the dict of the song data that is returned from the API request and then outputs the
        song data for that track to its own json file in the Song_json folder. This is to be used
        when posting song data
        :param song_info: dict of the song data of every song we pulled
        :return: the json string we encoded
        """
        file_list = []

        # for ever song id in the song_info dict, there is another dict full of the song information
        # for that specific song id
        for song_id in song_info.keys():
            file_name = self.root_dir + song_id + ".json"
            file = open(file_name, 'w')
            json_str = to_json(song_info[song_id])
            file.write(json_str)
            file.close()
            file_list.append(file_name)

        return file_list

    def song_format(self, song_dict):
        """
        method that converts song dict into an array of dicts to prep for json
        :param song_dict: dictionay of songs
        :return: dictionary {'song' : song_arr}
        """
        song_arr = []
        for key in song_dict.keys():
            new_song_dict = {'id': key,
                             'info': song_dict[key]}
            song_arr.append(new_song_dict)
        return {'songs' : song_arr}

    def download_user_playlists(self) :
        """
        method responsible for getting information about a users saved playlists
        :return: array containing playlist information
        TODO save playlist information in a file, possibly JSON
        """
        if self.token:
            # init file, spotipy, array, and get playlist info
            playlist_data = open('playlist.json', 'w')
            sp = spotipy.Spotify(auth=self.token)
            playlists_arr = []
            playlists = sp.user_playlists(self.username)

            # iterate through getting indvidual playlist info
            for playlist in playlists['items']:
                print(playlist['name'])
                print('total tracks: ', playlist['tracks']['total'])
                playlists_arr.append(playlist)

            # place in dict, convert to json, save json
            playlists_dict = {'playlist': playlists_arr}
            playlist_json = to_json(playlists_dict)
            playlist_data.write(playlist_json)
            playlist_data.close()
            return playlists_arr
        else:
            print("Can't get token for", self.username)
            return None

    def create_json_folder(self, folder_name: str):
        """
        We need to create an output folder for all of the song json files. We are going to
        make sure that the folder is empty so we don't upload duplicate song information to Solr
        :param folder_name: name of the output folder
        :return: None
        """
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)
        os.makedirs(folder_name)

    # TODO: this function doesn't work with download_songs because the returned data is not the same as user_playlists
    def download_featured_playlists(self):
        """
        Performs the same function as download_user_playlists but instead pulls all of the featured
        playlists from spotify instead of the user playlists
        :return: array containing playlist information
        """
        if self.token:
            # init file, spotipy, array, and get playlist info
            playlist_data = open('playlist.json', 'w')
            sp = spotipy.Spotify(auth=self.token)
            playlists_arr = []
            playlists = sp.featured_playlists(limit=50, offset=0)

            # iterate through getting indvidual playlist info
            while playlists:
                for playlist in playlists['playlists']['items']:
                    print('total tracks: ', playlist['tracks']['total'])
                    playlists_arr.append(playlist)
                playlists = sp.next(playlists['playlists'])

            # place in dict, convert to json, save json
            playlists_dict = {'playlist': playlists_arr}
            playlist_json = to_json(playlists_dict)
            playlist_data.write(playlist_json)
            playlist_data.close()
            return playlists_arr
        else:
            print("Can't get token for", self.username)
            return None

    def create_json_folder(self, folder_name:str):
        """
        We need to create an output folder for all of the song json files. We are going to
        make sure that the folder is empty so we don't upload duplicate song information to Solr
        :param folder_name: name of the output folder
        :return: None
        """
        if os.path.exists(folder_name) :
            shutil.rmtree(folder_name)
        os.makedirs(folder_name)

# TODO: this function doesn't work with download_songs because the returned data is not the same as user_playlists
    def download_featured_playlists(self):
        """
        Performs the same function as download_user_playlists but instead pulls all of the featured
        playlists from spotify instead of the user playlists
        :return: array containing playlist information
        """
        if self.token:
            # init file, spotipy, array, and get playlist info
            playlist_data = open('playlist.json', 'w')
            sp = spotipy.Spotify(auth=self.token)
            playlists_arr = []
            playlists = sp.featured_playlists(country="US")['playlists']
            #print(playlists['playlists'])

            # iterate through getting indvidual playlist info
            for playlist in playlists['items']:
                print(playlist['name'])
                print('total tracks: ', playlist['tracks']['total'])
                playlists_arr.append(playlist)

            # place in dict, convert to json, save json
            playlists_dict = {'playlist': playlists_arr}
            playlist_json = to_json(playlists_dict)
            playlist_data.write(playlist_json)
            playlist_data.close()
            return playlists_arr
        else:
            print("Can't get token for", self.username)
            return None


if __name__ == '__main__' :
    import sys
    sm = SpotifyManager(sys.argv[1])
    output_folder = sys.argv[2]
    # playlist_arr = sm.download_user_playlists()
    playlist_arr = sm.download_featured_playlists()
    tracks_arr = sm.download_songs(playlist_arr, output_folder)