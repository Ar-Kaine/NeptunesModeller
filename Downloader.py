# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 08:47:37 2020

@author: jamie
"""

#Edit this config file to be your input file
config_file = './inputs/downloader_skull.json'

#Run the file without touching anything below here

from NeptunesModeller import Connection
import json

if __name__ == "__main__":
     config = json.load(open(config_file))
     connection = Connection(config['game_id'], config['api_key'])
     connection.toExcel(config['output_location'])