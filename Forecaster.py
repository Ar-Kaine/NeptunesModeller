# -*- coding: utf-8 -*-
"""and 
Created on Tue Oct 13 15:20:32 2020

This script is used to forecas what infrastructure you will be able to build
when spending your funds

Config File:
 #Change the config filepath to one that has your Game ID and API Key. The 
play#file needs to be a .json file that looks like this (you can create it in any
#text editor)
# {
#   "game_id": 111111111111111111, 
#   "api_key": "1aaAAaa",
#   "spend_ratio" : {"e": 3, "i": 3, "s": 3, "o": 1}
# }
    
@author: jamie
"""

#Change this field to the filepath you need
config_file = './inputs/forecaster_general.json'
terra_levels = 2


#Run the script wihout editting the below
import NeptunesModeller as nm
import json
import copy


def forecastSpend(player,terra=0):
    '''Runs a forecast of the spend for the player'''
    
    player = copy.deepcopy(player)
    
    for i in range(terra):
        player.buyTech('terraforming')
    
    funds = player.funds
    results = player.spendFunds(forecast=True)
    funds = funds - sum([i['spent'] for i in results.values()])
    results['funds'] = funds
    results['terra'] = player.techs['terraforming']['level']
    return results

def printResults(result):
     '''Prints results from the spending forecast'''
    
     print('Spending with terraforming level:', result['terra'])
     print('   Economy:   ', result['e']['bought'], ' for $', result['e']['spent'], sep='')
     print('   Industry:  ', result['i']['bought'], ' for $', result['i']['spent'], sep='')
     print('   Science:   ', result['s']['bought'], ' for $', result['s']['spent'], sep='')
     print('   Other:     ', result['o']['bought'], ' for $', result['o']['spent'], sep='')
     print('   Remaining: $', result['funds'], sep='')
     print()
               
if __name__ == "__main__":
    
    config = json.load(open(config_file))

    connection = nm.Connection(config['game_id'], config['api_key'])
    player = connection.createPlayer(spend = config['spend_ratio'])
    
    #The below is a test model instead of an active game. Replace the config
    # details to run a test model instead
    
    # game = nm.Game()
    
    # game.addPlayer('No team', 'Test',funds=10000, priorities = ['terraforming'])
    # for i in range(50):
    #     game.addStar()
    # for i in range(10):
    #     game.advanceDay()
    # player = game.players[0]
    
    
    
    
    #Printing results to console
    print('Running Forecaster. Config settings:')
    print('Game:', connection.name)
    print('Player:', player.name)
    print()
    print('Spending Priorities:')
    print('   Economy: ', config['spend_ratio']['e'])
    print('   Industry:', config['spend_ratio']['i'])
    print('   Science: ', config['spend_ratio']['s'])
    print('   Other:   ', config['spend_ratio']['o'])    
    print()
    
    for i in range(terra_levels):
        printResults(forecastSpend(player,i))

