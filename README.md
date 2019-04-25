# spotify_search
CSCE 470 project

## Abstract
Spotify uses a music algorithm in order to group songs into music
playlists. This allows a user to simply choose a song and Spotify will
choose subsequent songs to play after the current one is finished.
However, this algorithm is not very effective at choosing songs that are
similar to the one being played. The algorithm looks at the genre and
relies on other users groupings and playlists. Often times, the songs
are not similar but are still in the same genre, which can lead to a
very jarring transition from a quiet, slow song to a louder, quicker
one. Examples of this can be Come Sail Away by The Styx transitioning to
The Grand Illusion by the same band. These two songs are in the same
genre, the same band, and even in the same album, however, the two songs
are drastically different in style and volume dynamics.

## Project Objective
Our objective is to modify the current Spotify search engine to improve 
playlist lineups. We will still take into account the genre, artist and 
album of a song but do some extra analysis to get more information about 
a song file. We will then create a playlist based off of the song 
metadata of a single song so that we can create a playlist of songs 
similar to the one we analyzed.

## Root Folder
The Project was created under the name Music Search++. This set of Python scripts allows the user to
pull their user and featured Spotify playlists and download the song data. Its not listed here but
we then take that data and push it to Solr 7.7 hosted on a Amazon AWS EC2 Instance. This directory 
also holds the original project abstract (we deviated slightly during the course of the project).
The directory also has encrypt and decrypt scripts to encryp and descrypt the sensitve.zip.enc
file. I has all of our passwords and sensitive information in their but you need to know the
password to decrypt it but the encrypt.sh file can be used to encrypt pretty much any folder or file.
The spotify.py file is what is actually used to pull the Spotify playlists. It downloads the information
and then goes through each one, downloads the songs, and outputs each song into its own json file
to be uploaded to Solr using Solr's post tool.

## Search Folder
Inside the search/ folder, there exists the Python Scripts that allows a user to query the Solr database.

enviroment and dependcies 
python -v 3.7.3
spotipy -v 2.4.4
