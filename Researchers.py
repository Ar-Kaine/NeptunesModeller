# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 16:43:47 2021

@author: jamie
"""

import NeptunesModeller as nm
import json

config_file = './inputs/research_config.json'

config = json.load(open(config_file))

players = []

for i in config['api_keys']:
    connection = nm.Connection(config['game_id'], i)
    player = connection.createPlayer(spend = config['spend_ratio'])
    player.funds = config['funds']
    player.spendFunds()
    players.append(player)
    
results = [(p.name, p.total_science, p.researching, p.techs) for p in players]

results.sort(reverse=True, key=lambda x: x[1]) 

for i in results:
    print(i[0], ":", i[1], i[2])
    

    
    











