import spotipy
import spotipy.util as util
from api import client_id as c_id, client_secret as secret, redirect


class Playlist_Create:

	def __init__(self, username: str, playlist: str, description: str, scope='playlist-read-private'):
		self.username = username.strip()
		self.playlist = playlist
		self.description = description
		self.scope = 'playlist-read-private playlist-modify-public'
		self.token = None

	def authenticate(self, write=False):
		"""
		Use the username to get a token to use
		:param write: boolean to determine if we are reading or writing
		:return: the token string
		"""
		if self.username is None:
			print("ERROR: Must input a username!!")
			return
		u = self.username.strip()

		print("Authenticating user: ", u)
		self.token = util.prompt_for_user_token(u, self.scope, client_id=c_id, client_secret=secret,
													redirect_uri=redirect)


		return self.token

	def unpack_song_data(self, song: dict):
		"""
		Helper function. Basically just cleans up what is in the dictionary to shorten code
		since many elements in the song dict are acutually lists with one element
		:param song: dictionary of song data for ONE song
		:return:
		"""
		song_dict = {}
		song_dict['target_liveness'] = song['liveness'][0]
		song_dict['target_key'] = song['key'][0]
		song_dict['target_mode'] = song['mode'][0]
		song_dict['target_acousticness'] = song['acousticness'][0]
		song_dict['target_danceability'] = song['danceability'][0]
		song_dict['target_energy'] = song['energy'][0]
		song_dict['target_speechiness'] = song['speechiness'][0]
		song_dict['target_valence'] = song['valence'][0]
		song_dict['target_tempo'] = song['tempo'][0]
		song_dict['target_instrumentalness'] = song['instrumentalness'][0]

		return song_dict

	def get_similar_songs(self, song_info: dict):
		"""
		Uses the spotipy recommendations function to find similar songs based off of all of the
		information from the song that is passed in.
		:param song_info: should only have the information for ONE song
		:return:
		"""

		if len(song_info['response']['docs']) != 1:
			print("ERROR: Only one song should be returned for this")
			return

		if self.token: # if we have an authenticated token
			song_id = [song_info['response']['docs'][0]['id']]
			song = song_info['response']['docs'][0]
			song = self.unpack_song_data(song)

			# TODO: Authentication is messed up so i have to come back to test this
			sp = spotipy.Spotify(auth=self.token)
			response = sp.recommendations(seed_tracks=song_id, kwargs=song)

			return response
		else:
			print("Can't get token for", self.username)
			return None

	def get_song_ids(self, song_data:dict):
		"""
		Extracts the song ID's from the response of get_similar_songs()
		:param song_data: dictionary response from get_similar_songs()
		:return: list of song ID's
		"""

		id_list = []
		for track in song_data['tracks']:
			id_list.append(track['id'].strip())

		return id_list

	def create_playlist(self):
		"""
		Used to actually create the playlist. The playlist must be created before any songs
		can be added
		:return: name of the playlist
		"""

		if self.playlist is None:
			print("ERROR:Must specifiy the name of the playlist!")
			return

		# make sure that we have modify priveleges
		self.authenticate(True)

		if self.token:
			sp = spotipy.Spotify(auth=self.token)
			desc = self.description
			user = sp.current_user()
			playlist_id = sp.user_playlist_create(user['id'], self.playlist, public=True)
			playlist_id = playlist_id['id']
			print("Returned Playlist: ", playlist_id)

			return playlist_id
		else:
			print("Can't get token for", self.username)
			return None

	def add_songs(self, playlist_id:str, song_ids:list):
		"""
		Takes the list of songs that is returned from get_similar_songs() and uploads
		them to the playlist that was created in create_playlist()
		:param playlist_id: playlist ID returned from create_playlists()
		:param song_ids: list of song ID's returned from get_similar_songs()
		:return:
		"""
		if type(song_ids) != list:
			print("ERROR: Need list of song ID!!")
			return

		if self.token:
			sp = spotipy.Spotify(auth=self.token)
			sp.user_playlist_add_tracks(sp.current_user()['id'], playlist_id, song_ids, position=None)
		else:
			print("Can't get token for", self.username)
			return None







