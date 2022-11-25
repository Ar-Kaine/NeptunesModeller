# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 20:45:11 2022

@author: jamie
"""

#Edit this config file to be your input file
config_file = './inputs/starfield.json'

#Run the file without touching anything below here

from NeptunesModeller import Connection
import json

if __name__ == "__main__":
     config = json.load(open(config_file))
     connection = Connection(config['game_id'], config['api_key'])
