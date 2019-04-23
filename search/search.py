#!/usr/bin/env python3

import argparse
import sys
from solr_query import *


"""
    Usage:  python3 search.py --s/--song <song_name> 
            python3 search.py --a/--artist <artist> 
            
            python3 search.py --i/--id <song_id> 
"""

"""
This file uses the Solr interfacing functions in solr_query.py in order to create a fully featured 
command line application. The user will either specify a song or artist to search up. In both cases,
the results will be output in the command line window. The results from both artist and song searches 
will be the name of the song, the Song's ID (for creating playlists) and the URI for the song so it
can be opened up on the 
"""

def search_by_song(song:str):
    pass

def search_by_artist(artist:str):
    pass

def search_by_id(id:str):
    pass

def create_playlist(playlist:str, id:str):
    pass

def print_search_results(results):
    pass

def main():
    """
    Takes the command line arguments and calls the correct function accordingly
    :return:
    """
    description = "Utility to search for spotify by song, artist or song ID and to create playlists based off of song ID's"
    usage = "search.py [-h] [-s SONG | -a ARTIST | -i ID] [-p PLAYLIST & -i ID & -d DESCRIPTION]"
    parser = argparse.ArgumentParser(description=description, usage=usage)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--song", nargs=1, required='--argument' in sys.argv, help="Search for a song by name")
    group.add_argument("-a", "--artist", nargs=1, required='--argument' in sys.argv, help="Search for songs from an Artist\n")
    group.add_argument("-i", "--id", nargs=1, required='--argument' in sys.argv, help="Search for song based on ID or create playlist based off of song ID")
    parser.add_argument("-p", "--playlist", nargs = 1, required='--id' in sys.argv, help="Name of the playlist to be created. MUST be used with -i/--id")
    parser.add_argument("-d", "--description", nargs = 1, required='--argument' in sys.argv, help="Playlist Description. Must be used with -i and -p")
    args = parser.parse_args()
    # print(args)

    solr = Solr_Query()

    response = None

    if args.song:
        print("Searching for song:", args.song[0].strip())
        song_name = args.song[0].strip()
        solr.set_search_type("songs")
        query = solr.set_query(song_name)
        response = solr.exec_query(query)
        solr.print_search_results(response)


    if args.artist:
        print("Searching for songs by artist: ", args.artist[0].strip())
        artist = args.artist[0].strip()
        solr.set_search_type("artists")
        query = solr.set_query(artist)
        response = solr.exec_query(query)
        solr.print_search_results(response)

    if args.id:
        print("Searching for song with ID:", args.id[0].strip())
        id = args.id[0].strip()
        solr.set_search_type("id")
        query = solr.set_query(id)
        response = solr.exec_query(query)
        solr.print_search_results(response)

    # Still trying to figure this one out. The getmorelike this funcionality is harder than we thought
    if args.playlist and args.id and args.description:
        print("Creating a playlist based off of song ID:", args.id[0].strip())
    elif args.playlist and not args.id:
        parser.error("Must input a song ID to create a playlist with!")
    elif args.playlist and not args.description:
        parser.error("Must input a playlist description")

    print("\nDone!")



if __name__ == '__main__' :
    main()
