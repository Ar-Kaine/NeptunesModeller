# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 07:38:28 2020

@author: jamie
"""

from NeptunesModeller import Game
import copy

#Run this script without changing anything below
if __name__ == "__main__":
    
    game = Game()
    game.addPlayer('team 1', 'player 1')
    game.addPlayer('team2', 'player 2')
    game.players[0].target_stars = 6
    
    for i in range(10):
        game.addStar()

    for i in game.players:
        print(i.name, 'stars: ', len(i.stars), 'Target:', i.target_stars)
    

    for i in range(10):
        game.addStar(growth=True)
    
    
    for i in game.players:
        print(i.name, 'stars: ', len(i.stars), 'Target:', i.target_stars)
    
    all_stars = [copy.deepcopy(j) for i in game.players for j in i.stars ]
    
