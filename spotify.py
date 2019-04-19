from api import client_id as c_id, client_secret as secret, redirect
import spotipy
import spotipy.util as util


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

    def download_songs(self, tracks) :
        """
        method responsible for extracting song information from a given playlist
        TODO save songs in a file, possibly JSON
        @param tracks: dictionary from returned from spotify api containing information about a given playlists tracks
        """
        for i, item in enumerate(tracks['items']) :
            track = item['track']
            print(i, track['artists'][0]['name'], track['name'])
            
    def download_playlists(self) :
        """
        method responsible for getting information about a users saved playlists
        TODO save playlist information in a file, possibly JSON
        """
        if self.token :
            sp = spotipy.Spotify(auth=self.token)
            playlists = sp.user_playlists(self.username)
            for playlist in playlists['items']:
                print(playlist['name'])
                print('total tracks: ', playlist['tracks']['total'])
                results = sp.user_playlist(self.username, playlist['id'])
                tracks = results['tracks']
                self.download_songs(tracks)
                while tracks['next'] :
                    tracks = sp.next(tracks)
                    self.download_songs(tracks)
        else:
            print ("Can't get token for", username )

if __name__ == '__main__' :
    import sys
    sm = SpotifyManager(sys.argv[1])
    sm.download_playlists()


