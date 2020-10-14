# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 15:20:32 2020

This script is used to forecast whether is is worth purchasing Terraforming
before production, or if you should wait until afterwards.

Modes:
    


@author: jamie
"""
import NeptunesModeller as nm
import json


#Change the config filepath to one that has your Game ID and API Key
# {
#   "game_id": 111111111111111111, 
#   "api_key": "1aaAAaa"
# }
config_file = './inputs/forecaster_roger.json'

#Run the script wihout editting the below

def forecastSpend(player):
    
    funds = player.funds
    results = player.spendFunds(forecast=True)
    funds = funds - sum([i['spent'] for i in results.values()])
    results['funds'] = funds
    results['terra'] = player.techs['terraforming']['level']
    return results

def printResults(result):
     print('Spending with terraforming level:', result['terra'])
     print('   Economy:   ', result['e']['bought'], ' for $', result['e']['spent'], sep='')
     print('   Industry:  ', result['i']['bought'], ' for $', result['i']['spent'], sep='')
     print('   Science:   ', result['s']['bought'], ' for $', result['s']['spent'], sep='')
     print('   Other:     ', 'Spent $', result['o']['spent'], sep='')
     print('Remaining Funds:', result['funds'], sep='')
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
    
    
    #Forecasting results
    results_current = forecastSpend(player)
    
    player.buyTech('terraforming')
    results_terra = forecastSpend(player)
    
    
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
    printResults(results_current)
    printResults(results_terra)
   
    

    
    
    
    
    
    
    # initial_level = player.techs['terraforming']['level']
    # initial_funds = player.funds
    # no_terra = player.buyInfra('e', player.funds, forecast=True)

    # result = player.buyTech('terraforming')
    
    # bought_level = player.techs['terraforming']['level']
    # bought_funds = player.funds
    # with_terra = player.buyInfra('e', player.funds, forecast=True)
    
    # if not result:
    #     conclusion = 'Insufficient funds to buy terraforming'
    # elif (no_terra['bought'] <= with_terra['bought'] and
    #     no_terra['funds']  <= with_terra['funds']):
    #     conclusion = 'Buy terraforming now'
    # else:
    #     conclusion = 'Buy terraforming after production'
    
    # print('Terraforming forecast.')
    # print()
    # print('Without terraforming:')
    # print('Economy Bought: ', no_terra['bought'])
    # print('Funds Remaining: ', no_terra['funds'])
    # if result:
    #     print()
    #     print('With terraforming:')
    #     print('Economy Bought: ', with_terra['bought'])
    #     print('Funds Remaining: ', with_terra['funds'])
    # print()
    # print(conclusion)