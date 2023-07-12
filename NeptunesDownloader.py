# -*- coding: utf-8 -*-
"""
A quick and easy script for downloading data from Neptune's Pride, designed
to be used by non-coders.

1) You will need to have an instance of Python installed
2)  
"""






import requests
import pandas as pd


def getData(game_id, api_key):
        '''Access the Neputune's Pride API and returns the JSON result
        
        This provides the API data as is with no changes or edits to the format.
        Get the game number from your in game url and the api key can
        be generated for that game in the options page
        '''

        root = "https://np.ironhelmet.com/api"
        
        params = {"game_number" : game_id,
                 "code" : api_key,
                 "api_version" : "0.1"}
            
        return requests.post(root, params).json()
    
    
def saveData(game_data, filepath):
       
