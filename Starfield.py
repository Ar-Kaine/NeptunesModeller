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
     
     results = []
     
     for i in connection.stars.values():
         star = {}
         star['uid'] = int(i['uid'])
         star['name'] = i['n']
         star['x'] = float(i['x'])
         star['y'] = float(i['y'])
         star['puid'] = int(i['puid'])
         
         #Visible only - and try/except
         star['r'] = int(i['r'])
         star['ga'] = int(i['ga'])
         star['e'] = int(i['ga'])
         star['i'] = int(i['ga'])
         star['r'] = int(i['ga'])                
         star['st'] = int(i['st'])
                             
         #To add: Wormholes
         
         results.append(star)
         
     output = {"stars" : results}
     json.dump(output, open(config["output_location"],'w'), indent=4)