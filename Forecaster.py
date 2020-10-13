# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 15:20:32 2020

This script is used to forecast whether is is worth purchasing Terraforming
before production, or if you should wait until afterwards.


@author: jamie
"""
import NeptunesModeller as nm


#Change the config filepath to one that has your Game ID and API Key
# {
#   "game_id": 111111111111111111, 
#   "api_key": "1aaAAaa"
# }
config_file = './inputs/forecaster_roger.json'

#Run the script wihout editting the below
if __name__ == "__main__":
    

    connection = nm.Connection(filename = config_file)
    player = connection.createPlayer()
    
    #The below is a test model instead of an active game
    # game = nm.Game()
    
    # game.addPlayer('No team', 'Test',funds=10000, priorities = ['terraforming'])
    # for i in range(50):
    #     game.addStar()
    # for i in range(10):
    #     game.advanceDay()
        
    
    # player = game.players[0]
    
    initial_level = player.techs['terraforming']['level']
    initial_funds = player.funds
    no_terra = player.buyInfra('e', player.funds, forecast=True)

    result = player.buyTech('terraforming')
    
    bought_level = player.techs['terraforming']['level']
    bought_funds = player.funds
    with_terra = player.buyInfra('e', player.funds, forecast=True)
    
    if not result:
        conclusion = 'Insufficient funds to buy terraforming'
    elif (no_terra['bought'] <= with_terra['bought'] and
        no_terra['funds']  <= with_terra['funds']):
        conclusion = 'Buy terraforming now'
    else:
        conclusion = 'Buy terraforming after production'
    
    print('Terraforming forecast.')
    print()
    print('Without terraforming:')
    print('Economy Bought: ', no_terra['bought'])
    print('Funds Remaining: ', no_terra['funds'])
    if result:
        print()
        print('With terraforming:')
        print('Economy Bought: ', with_terra['bought'])
        print('Funds Remaining: ', with_terra['funds'])
    print()
    print(conclusion)