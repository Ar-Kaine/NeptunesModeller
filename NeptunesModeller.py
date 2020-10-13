# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 14:34:05 2020

@author: jamie
"""
import requests
import math
import pandas as pd
import csv
import json
import copy
import random
import statistics


INFRATYPES = {'i' : 'Industry',
              'e' : 'Economy',
              's' : 'Science'}

INFRACOST =  {'e' : 500,
              'i' : 1000,
              's' : 4000} 

#Default Values

DEFAULT_TECH = {'scanning':     {'level': 1, 'research': 0, 'brr': 144}, 
                'propulsion':   {'level': 1, 'research': 0, 'brr': 144}, 
                'terraforming': {'level': 1, 'research': 0, 'brr': 144}, 
                'research':     {'level': 1, 'research': 0, 'brr': 144}, 
                'weapons':      {'level': 1, 'research': 0, 'brr': 144}, 
                'banking':      {'level': 1, 'research': 0, 'brr': 144}, 
                'manufacturing':{'level': 1, 'research': 0, 'brr': 144}}

DEFAULT_STARS = [{'c': 0.0, 'e': 5, 'i': 5, 's': 1, 'r': 55, 'ga': 0, 'nr': 50, 'st': 10},  
                 {'c': 0.0, 'e': 0, 'i': 0, 's': 0, 'r': 40, 'ga': 0, 'nr': 35, 'st': 10}, 
                 {'c': 0.0, 'e': 0, 'i': 0, 's': 0, 'r': 30, 'ga': 0, 'nr': 25, 'st': 10}, 
                 {'c': 0.0, 'e': 0, 'i': 0, 's': 0, 'r': 20, 'ga': 0, 'nr': 15, 'st': 10}]

PRODUCTION = 20

TECHNOLOGIES = ('scanning',
                'propulsion',
                'terraforming',
                'research',
                'weapons',
                'banking',
                'manufacturing')


SPEND = {'e' : 2 , 'i' : 3, 's' : 5 , 'o' : 3}

class Connection:
    '''Handles connecting to the API to extract real data from the system'''
    def __init__(self, game_id=None, api_key=None, filename=None):
        '''Parses the API information and stores it in the connection. 
        
        Most lists are stored as attributes, time and game settings as dictionaries'''
        if game_id and api_key:
            self.game_id = game_id
            self.api_key = api_key
        elif filename:
            config = json.load(open(filename, 'r'))
            self.game_id = config['game_id']
            self.api_key = config['api_key']
 
        data = self.getData()
        
        self.name = data.pop('name')
        self.fleets = data.pop('fleets')
        self.players =  data.pop('players')
        
        self.stars = data.pop('stars')
        
        for i in self.stars.values():
            x = float(i['x'])
            y = float(i['y'])
            i['distance'] = math.sqrt(x * x + y * y)


        self.time = {'start_time' : data.pop('start_time'),
                     'now' : data.pop('now'),
                     'production_counter' : data.pop('production_counter'),
                     'production_rate' : data.pop('production_rate'),
                     'productions' : data.pop('productions'),
                     'tick' : data.pop('tick'),
                     'tick_fragment' : data.pop('tick_fragment'),
                     'tick_rate' : data.pop('tick_rate'),
            }

        self.settings = data

    def getData(self):
        '''Returns Dict object for all game data'''

        root = "https://np.ironhelmet.com/api"
        
        params = {"game_number" : self.game_id,
                 "code" : self.api_key,
                 "api_version" : "0.1"}
            
        return requests.post(root, params).json()['scanning_data']
    
    
    def toExcel(self):
        '''Writes the data from the connection to a multi-sheet excel document. Not implemented'''
        #to implement
        raise NotImplementedError('not implemented')
        
    def createPlayer(self,spend=SPEND,priorities=None):
        '''Returns a PlayerModel representing the active player'''
        #'researching' is a value only on the active player
        active_player = [i for i in self.players.values() if 'researching' in i.keys()][0]
        
        if not priorities:
            priorities = [active_player['researching']]
            
        player_stars = self.getPlayerStars(active_player['uid'])
        
        max_ships = max([i['total_strength'] for i in self.players.values()])
        max_weapons = max([i['tech']['weapons']['level'] for i in self.players.values()])
        
        game = Game(production = self.time['production_rate'],
                    model_ships = max_ships,
                    model_level = max_weapons)
            
        player = PlayerModel(team = None,
                             game = game,
                             name = active_player['alias'],
                             stars = player_stars,
                             techs = active_player['tech'],
                             priorities = priorities,
                             funds = active_player['cash'],
                             spend = spend,
                             carriers = active_player['total_fleets'],
                             )
        
        return player
        
    def getPlayerStars(self, puid):
        return [v for k,v in self.stars.items() if v['puid'] == puid]
        
        
        
class Game:
    
    def __init__(self, production = 20, model_ships = 10000, model_level = 10):
        self.players = []
        self.production = production
        self.model =  ( model_level, model_ships)
        self.alliances = {}
        
    def addPlayer(self,team,  name, priorities=None, spend=None, funds = 500, target_stars=50):
        '''adds a new player with name to the game'''
        
        if not priorities:
            priorities = DEFAULT_TECH.keys()
        if not spend:
            spend = SPEND
        self.players.append(PlayerModel(team = team,
                                        name = name, 
                                        game = self, 
                                        priorities = priorities, 
                                        researching = priorities[0],
                                        target_stars = target_stars,
                                        funds = funds,
                                        spend = spend))
                    
    def setTech(self, level, techs = DEFAULT_TECH.keys()):
        for i in self.players:
            i.setTech(level, techs)
    
    def addStar(self, player = None, i = 0, s = 0):
        
        quality = random.choice(('bad','good'))
        if quality == 'bad':
            if random.randint(1,10) == 1:
                resources = 1
            else:
                resources = random.randint(2,13)
        else:
            resources = random.randint(14,49)
            
        star = {'c': 0.0, 'e': 0, 'i': i, 's': s, 'r': resources, 'ga': 0, 'nr': resources, 'st': 0}
        
        if player:
            player.addStar(star)
        else:
            for i in self.players:
                if i.target_stars > len(i.stars):
                    i.addStar(star)
                
    def addShips(self, ships):
        for i in self.players:
            i.addShips(ships)
    
    def addFunds(self, funds):
        for i in self.players:
            i.addFunds(funds)
            
    def spendFunds(self):
        for i in self.players:
            i.spendFunds()
            
    def createModel(self, level, ships):
        self.model =  ( level, ships)
        for p in self.players:
            p.refresh() #TODO refactor
            
    def modelStrength(self, player):
        
        def battle(defenderTech, defenderShips, attackerTech, attackerShips):
            while True:
                attackerShips -= defenderTech + 1
                if attackerShips <= 0:
                    attackerShips = 0
                    return (defenderShips, attackerShips)
                defenderShips -= attackerTech
                if defenderShips <= 0:
                    defenderShips = 0
                    return (defenderShips, attackerShips)
            
    
        results = battle(self.model[0], 
                         self.model[1],
                         player.techs['weapons']['level'], 
                         player.total_strength)
        return results[1] - results[0]
    
    def tick(self):
        if len(self.players) > 0:
            for i in self.players:
                i.tick()
                
    def production(self):
        for i in self.players:
            i.runProduction()
            
    def shareTech(self):   #TODO Costs for sharing tech
        for player_giving in self.players:
            for player_receiving in self.players:
                if player_giving.team == player_receiving.team:
                    for tech, values in player_giving.techs.items():
                        level = values['level']
                        if player_receiving.techs[tech]['level'] < level:
                            player_receiving.techs[tech]['level']  = level
            
    def advanceDay(self):
        for p in self.players:
            for i in range(self.production):
                p.tick()
            p.spendFunds()
            p.runProduction()
        self.shareTech()
                       
            
class PlayerModel:
    
    def __init__(self, team, name, game, 
                 stars = DEFAULT_STARS , researching='scanning', 
                 techs = DEFAULT_TECH, priorities=TECHNOLOGIES, 
                 funds = 300, spend=SPEND, carriers = 1,
                 target_stars = 50):
        self.team = team
        self.name = name
        self.game = game
        self.funds = funds
        self.stars = copy.deepcopy(stars)
        self.techs = copy.deepcopy(techs)
        self.priorities = copy.deepcopy(priorities)
        self.spend = spend
        self.researching = researching
        self.target_stars = target_stars
        self.refreshTotals()
        self.refreshStars()

        
    def __str__(self):
        result = ''
        result += 'team:' + str(self.team) + ', '
        result += 'name:' + str(self.name) + ', '
        result += 'research:' + str(self.researching) + ', '
        result += 'total_strength:' + str(self.total_strength) +  ', '
        result += 'total_science:' + str(self.total_science) + ', '
        result += 'total_economy:' + str(self.total_economy) + ', '
        result +=  'total_industry:' +  str(self.total_industry)
        
        return result
    
    def __repr__(self):

        return str(self.toDict())
    
    def toDict(self):
        rep = {'team'           : self.team,
               'name'           : self.name,
               'total_stars'    : self.total_stars,
               'star_quality'   : self.star_quality,
               'model_stength'  : self.model_strength,
               'total_strength' : self.total_strength,
               'funds'          : self.funds,
               'total_science'  : self.total_science,
               'total_economy'  : self.total_economy,
               'total_industry' : self.total_industry,
               'researching'    : self.researching,
               'scanning'       : self.techs['scanning']['level'],
               'propulsion'     : self.techs['propulsion']['level'],
               'terraforming'   : self.techs['terraforming']['level'],
               'research'       : self.techs['research']['level'],
               'weapons'        : self.techs['weapons']['level'],
               'banking'        : self.techs['banking']['level'],
               'manufacturing'  : self.techs['manufacturing']['level']}
        return rep
    
    def addStar(self, star):
        keys = ['c','e','i', 's', 'r', 'ga', 'nr', 'st']
        
        if all(i in keys for i in star.keys()):
            self.stars.append(copy.deepcopy(star))
        else:
            raise TypeError('Keys incorrect for star')
            
        self.refreshStars()
    
    
    def setTech(self, level, techs = DEFAULT_TECH.keys()):
        '''Sets technologies in techs to level. Does not affect researched amount'''
        for i in techs:
            self.techs[i]['level'] = level
            self.techs[i]['research'] = 0
        if 'terraforming'  in techs:
            self.refreshStars()
        self.refresh()
    
    def buyTech(self, tech):
        '''Buys the next level of technology if funds are available'''
        current_level = self.techs[tech]['level']
        tech_cost = current_level * 15
        if tech_cost <= self.funds:
            self.funds -= tech_cost
            self.setTech(current_level + 1, [tech])
            self.refresh()
            return True
        return False
        
        
    def addShips(self, ships):
        '''Adds a number of ships evenly distributed amongst the stars'''
        shipsPerStar = ships // len(self.stars)
        for i in self.stars:
            i['st'] += shipsPerStar
        self.stars[0]['st'] += ships % len(self.stars)
        self.refresh()
        
    def addFunds(self, funds):
        self.funds += funds
     
    def refresh(self):
        self.refreshStars()
        self.refreshTotals()
    
    def refreshTotals(self):
        '''Refreshes total numbers based upon star data'''
        self.total_strength = sum([i['st'] for i in self.stars])
        self.total_science  = sum([i['s'] for i in self.stars])
        self.total_economy  = sum([i['e'] for i in self.stars])
        self.total_industry = sum([i['i'] for i in self.stars])
        self.total_stars = len(self.stars)
        self.star_quality = statistics.mean([i['nr'] for i in self.stars])
        self.model_strength = self.game.modelStrength(self)
   

    def refreshStars(self):
        '''Refreshes star resources based on natural resources and terraforming level'''
        for i in self.stars:
            i['r'] = i['nr'] + (5 * self.techs['terraforming']['level'])
    
    
    def tick(self):
        '''Performs a tick for the player'''
        for i in self.stars:
            self.tickStar(i)
        self.researchTech()
        self.refresh()
        
        
    def tickStar(self, star):
        '''Star produces everything'''
        manufacturing = self.techs['manufacturing']['level']
        industry = star['i']
        production = round((industry * (manufacturing + 5)) / self.game.production + star['c'],2)
        star['st'] += int(production)
        star['c'] = production % 1
        

    def researchTech(self):
        '''Research technology for a tick'''
        
        current = self.techs[self.researching]
        threshold = current['level'] * current['brr']
        current['research'] += self.total_science
        
        
        if current['research'] >= threshold:
            current['level'] += 1
            current['research'] = current['research'] - threshold
            
            priorities = [(i, self.techs[i]['level']) for i in self.priorities]
            priorities.sort(key = lambda x : x[1])
            self.researching = priorities[0][0]
            
    def priceInfra(self, infratype, star):
        '''Returns the price for the next level of infrastructure'''
        cost = INFRACOST
        resources = star['r']
        level = star[infratype] + 1
        return int((cost[infratype] * (1 / resources)) * level)
    
    
    def buyInfra(self, infratype, funds, stars = None, bought = 0, forecast=False): #TODO Bug: Forecast doesn't work
        '''Buys the chepeast infratype until it runs out of funds, returning remaining funds'''

        
        if forecast:
          
            dup = copy.deepcopy(self)

            return dup.buyInfra(infratype, funds, stars, bought)
        
        if funds > self.funds:
            funds = self.funds
        
        if stars == None:
            stars = self.stars
        
        stars = sorted(stars, key = lambda x : self.priceInfra(infratype, x))
        
        cost = self.priceInfra(infratype, stars[0])
        
        if funds <= cost:
            return {'funds' : funds, 'bought' : bought}
        else:
            stars[0][infratype] += 1
            funds -= cost
            bought += 1
            self.funds -= cost
            self.refresh()
            return self.buyInfra(infratype, funds, stars, bought)
        

        
    def spendFunds(self):
        '''Spends all funds according to the spending priorities set''' 
        #Uses total funds if no number has been provided
                 
        spending = copy.deepcopy(self.spend)
        total_priorities = sum(spending.values())
        ratio = self.funds // total_priorities
        
        results = {}
        
        for k,v in spending.items():
            spending[k] = v * ratio
        
        #handles Other
        spent = spending.pop('o')
        bought = 0
        results['o'] = {'bought': bought, 'spent' : spent}
        
        #handles normal infra
        for k,v in spending.items():
            purchase = self.buyInfra(k,v)
            total_spend = v - purchase['funds']         
            results[k] = {'bought' : purchase['bought'], 'spent' : total_spend}
        
        #buys econ with the remaining funds
        remaining_funds = self.funds
        purchase = self.buyInfra('e', self.funds)
        total_spend = remaining_funds - purchase['funds']       
        results['e']['bought' ] += purchase['bought']
        results['e']['spent'] += total_spend
        
        self.refresh()
        return results
        
     

    def runProduction(self):
        income = self.total_economy * 10
        self.funds += income
        
        
        self.refresh()
        

class Model:
    def __init__(self,                
                 teams,
                 production_rate = 20,
                 production_number= 40,
                 model = {"weapons" : 10, "ships" : 10000},
                 tech_level = 3,
                 ships = 100,
                 max_stars = 500,
                 new_stars = 5):
        self.teams = teams
        self.production_rate = production_rate
        self.production_number = production_number
        self.model = model
        self.tech_level = tech_level
        self.ships = ships
        self.max_stars = max_stars
        self.new_stars = new_stars
        self.last_run = None


    def runModel(self, filepath):  
    
        game = Game(production = self.production_rate)
        self.last_run = game
        game.createModel(self.model['weapons'], self.model['ships'])
      
        for k,v in self.teams.items():
            team = k
            for i in v:
                name = i['name']
                priorities = i['researching']
                spend = i['spending']
                funds = i['funds']
                target_stars = i['stars']
                game.addPlayer(team, name, priorities, spend, funds, target_stars=target_stars)

                
        game.setTech(self.tech_level)

       
        for i in range(self.max_stars): #TODO maximum stars is currently manual
            game.addStar()
        
        game.addShips(self.ships)
        game.spendFunds()
        
        results = []
        for i in range(self.production_number):
            game.advanceDay()
            for p in game.players:
                entry = p.toDict()
                entry['Production'] = i
                results.append(entry)
                
        pd.DataFrame(results).to_csv(filepath)
        
  


