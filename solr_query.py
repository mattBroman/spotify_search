# import urllib.request
import json
import requests

class Solr_Query:

    def __init__(self):
        self.solr_link = "http://52.14.160.147:8983/solr/SpotifyDB/select?q="
        self.search_type = None
        self.query = None
        self.connection = None
        self.jsonwt = "\"&wt=json"  # song title search postfix to specify json format

    def set_search_type(self, search_type:str):
        """
        Sets the search type for the class. Determines if we search for a song
        :param search_type: Must either be 'songs', 'artists' or 'id'.
        :return: None
        """
        if search_type == "songs" or search_type == "artists" or search_type == "id":
            self.search_type = search_type
            return

    def set_query(self, query_element):
        """
        Sets the parameter for what we are actually searching for. It will correspond to
        the search type, which must be set prior to using this function
        :param query: either song name, artist name, or id to search for
        :return:
        """

        if self.search_type is None:
            print("ERROR: NEED TO INITIALIZE THE SEARCH TYPE")
            return

        if self.search_type == "songs":
            # search for any song name containing that search string
            self.query = "name:\"*" + query_element.strip() + "*"
        elif self.search_type == "artists":
            self.query = "artists:\"*" + query_element.strip() + "*"
        elif self.search_type == "id":
            self.query = "id:\"" + query_element.strip()
        else:
            print("ERROR: SEARCH TYPE IS NOT ONE OF THE APPROVED TYPES!")
            return

        # Append the json specifier to the end of our search string
        self.query += self.jsonwt.strip()

        return self.query.strip()

    def exec_query(self, query:str):
        """
        Actually executes our query. The functions set_search_type and set_query MUST be
        called before this function for it to work properly.
        :param query: Complete query String
        :return: dict: json response
        """

        url = self.solr_link.strip() + query.strip()
        # print("Search URL: ", url)
        response = requests.get(url)

        return response.json()

    def print_results(self, results:dict):
        for song in results['response']['docs']:
            # Every value in the dict is returned as a list
            # output =
            print(song['id'].strip() + ": ", song['name'][0].strip())







