# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 08:47:37 2020

The downloader handles connecting to the API and downloads the data to Excel.

The config file should have the api_key, game_id and output_location fields. 

Data is currently almost untouched from the original API format. The only changes are:

Players:
1) Removal of the "war" and "count down to war" fields to a separate sheet (player_war)
2) Main player progress on technologies moved to a separate sheet  (player_technology)
3) Research levels have been split out to just so each tech level against a player

Stars:
1) Addition of a "distance" field to stars, which is the distance of the star to the centre

All other fields are in their original format. 


@author: jamie
@author: Kaine
"""

#Edit this config file to be your input file
config_file = './inputs/downloader_taucaph.json'

#Run the file without touching anything below here

from NeptunesModeller import Connection
import json

if __name__ == "__main__":
     config = json.load(open(config_file))
     connection = Connection(config['game_id'], config['api_key'])
     connection.toExcel(config['output_location'])