# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 14:34:05 2020

S
@auhor: Kaine
"""
import requests
import math
import pandas as pd
import json
import copy
import random
import statistics
import odf


#Game settings information and conversions used across different objects
INFRATYPES = {'i' : 'Industry',
              'e' : 'Economy',
              's' : 'Science',
              'o' : 'Other'}

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


SPEND = {'e' : 2 , 'i' : 2, 's' : 2, 'o' : 1}

class Connection:
    '''Handles connecting to the API to extract real data from the system
    
    Connection can either be passed a game_id or api_key, or a .json file
    with the information in. The data that is pulled from the API will be in 
    a very similar format to the original API data, except that each type
    of data (e.g. players, stars, settings) is split into a separate attribute
    
    '''
    def __init__(self, game_id=None, api_key=None, filename=None):
        '''Parses the API information and stores it in the connection. 
        
        Most lists are stored as attributes, time and game settings as dictionaries'''
        if game_id and api_key:
            self.game_id = game_id
            self.api_key = api_key
        if game_id and api_key==None:
            self.game_id = game_id
            self.api_key = None
        elif filename:
            config = json.load(open(filename, 'r'))
            self.game_id = config['game_id']
            try:
                self.api_key = config['api_key']
            except KeyError:
                self.api_key = None
 
        data = self.getData()
        
        self.name = data['name']
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
        '''Access the Neputune's Pride API and returns the JSON result
        
        This provides the API data as is with no changes or edits to the format.
        The data will by and large reflect the details in the Connection object,
        but this can be used if you prefer the raw format for whatever reason.
        It will use the same details as the Connection was set up with to access
        the data.
        
        '''
        
        if self.api_key == None:
            
            root = "https://nptriton.qry.me/game/" + str(self.game_id) + "/full"
            return requests.post(root).json()
    
        else:
            
            root = "https://np.ironhelmet.com/api"
            
            params = {"game_number" : self.game_id,
                     "code" : self.api_key,
                     "api_version" : "0.1"}

            return requests.post(root, params).json()['scanning_data']
    
    
    def toExcel(self, filepath):
        '''Writes the data from the connection to a multi-sheet excel document. 
        '''
        stars = pd.DataFrame(self.stars).transpose()
        players = copy.deepcopy(self.players)
        
        for i in players.values():
            techs = i.pop('tech')
            for k,v in techs.items():
                i[k] = v['level']
                
            if 'war' in i.keys():
                i.pop('countdown_to_war')
                i.pop('war')

        players = pd.DataFrame(players).transpose()
        
        timeset = copy.deepcopy(self.settings)
        timeset.update(copy.deepcopy(self.time))
        timeset = pd.Series(timeset)
        
        puid = str(self.settings['player_uid'])
        
        if puid != "-1":
            
            techs = pd.DataFrame(self.players[puid]['tech']).transpose()
            
            #Parses the war information which is spread in weird ways
            war = []
            
            for k in self.players[puid]['war']:
                row = {'player_id' : k ,
                       'war' : self.players[puid]['war'][k],
                       'countdown_to_war' : self.players[puid]['countdown_to_war'][k]}
                war.append(row)
            war = pd.DataFrame(war)
        
        fleets = pd.DataFrame(self.fleets).transpose()
        
        writer = pd.ExcelWriter(filepath)

        timeset.to_excel(writer,'settings')        
        stars.to_excel(writer, 'stars')
        players.to_excel(writer, 'players')
        fleets.to_excel(writer, 'fleets')
        
        try:
            techs.to_excel(writer, 'player_technology')
            war.to_excel(writer, 'player_war')
        except AttributeError:
            pass

        
        writer.save()
    
    
    
    def createPlayer(self,player=None, spend=SPEND,priorities=None):
        '''Returns a PlayerModel representing the active player
        
        The created PlayerModel willl match to the game settings, stars and
        technologies (including progress) that exist in the current game. 
        
        Spend can be used to set spending priorities if you plan to model or forecast:
        a dictionary with the ratio of spending type (e,i,s,o) should be provided.
        If spend is not set on creation, it will have spending priorities set to
        equal across the different infrastructure types. 
        
        Priorities sets the research priorities for the player. If not provided
        it will assume the player is sticking with the same technology. If this
        is not true, provide a list of the technologies that the player will 
        research - they will always research the lowest tech. 
        
        '''
        
        if player == None:
            #'researching' is a value only on the active playe
            active_player = [i for i in self.players.values() if 'researching' in i.keys()][0]
            
        else:
            active_player = self.players[str(player)]
            main_player = [i for i in self.players.values() if 'researching' in i.keys()][0]
            dif = [i for i in main_player.keys() if i not in active_player.keys()]
            for i in dif:
                active_player[i] = copy.deepcopy(main_player[i])
            
        
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
        '''Returns a list of stars owned by the player with the ID provided'''
        return [v for k,v in self.stars.items() if v['puid'] == puid]
        
        
        
class Game:
    
    def __init__(self, production = 20, model_ships = 10000, model_level = 10):
        self.players = []
        self.production = production
        self.model =  ( model_level, model_ships)
        self.alliances = {}
        self.production_count = 0
        
    def addPlayer(self,team,  name, priorities=None, spend=None, funds = 500, target_stars=50, growth_modifier = 1):
        '''adds a new player with name to the game'''
        
        if not priorities:
            priorities = list(DEFAULT_TECH.keys())
        if not spend:
            spend = SPEND
        self.players.append(PlayerModel(team = team,
                                        name = name, 
                                        game = self, 
                                        priorities = priorities, 
                                        researching = priorities[0],
                                        target_stars = target_stars,
                                        funds = funds,
                                        spend = spend,
                                        growth_modifier = growth_modifier))
                    
    def setTech(self, level, techs = DEFAULT_TECH.keys()):
        for i in self.players:
            i.setTech(level, techs)
    
    def addStar(self, player = None, e = 0, i = 0, s = 0, growth=False):
        '''Generates a star and adds it to player, or an identical star to each player
        
        If the player is already at their target stars, it will not add a star unless growth is set to True
        '''
        
        
        quality = random.choice(('bad','good'))
        if quality == 'bad':
            if random.randint(1,10) == 1:
                resources = 1
            else:
                resources = random.randint(2,13)
        else:
            resources = random.randint(14,49)
            
        star = {'c': 0.0, 'e': e, 'i': i, 's': s, 'r': resources, 'ga': 0, 'nr': resources, 'st': 0}

        
        if player:
            if growth:
                player.target_stars += 1
            player.addStar(star)
        else:
            for i in self.players:
                if growth:
                    i.target_stars += 1
                if i.target_stars > len(i.stars):
                    i.addStar(star)
                    
                    
    def growStars(self, x, growth_type = 'conquest'):
        '''Adds x new stars to each player. x is modified by the player growth modifier'''
        
        max_mod = int(max([i.growth_modifier for i in self.players]))
        for i in self.players:
            i.target_stars += (x * i.growth_modifier)
            if growth_type == 'conquest':
                all_stars = [copy.deepcopy(j) for i in self.players for j in i.stars ]
                eco = int(statistics.mean(i['e'] for i in all_stars))
                ind = int(statistics.mean(i['i'] for i in all_stars))
                sci = int(statistics.mean(i['s'] for i in all_stars))
         
            elif growth_type == 'new':
                eco = 0
                ind = 0
                sci = 0
            else:
                raise ValueError('Unknown value for growth_type: use "conquest" or "new"')
            
            for r in range(x * max_mod):
                self.addStar(i=ind, s=sci, growth=False)
                #TODO add econ cash gain
        
                
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
        
        #Old model strength - to be removed
        # def battle(defenderTech, defenderShips, attackerTech, attackerShips):
        #     while True:
        #         attackerShips -= defenderTech + 1
        #         if attackerShips <= 0:
        #             attackerShips = 0
        #             return (defenderShips, attackerShips)
        #         defenderShips -= attackerTech
        #         if defenderShips <= 0:
        #             defenderShips = 0
        #             return (defenderShips, attackerShips)
            
    
        # results = battle(self.model[0], 
        #                  self.model[1],
        #                  player.techs['weapons']['level'], 
        #                  player.total_strength)
        # return results[1] - results[0]
        return player.techs['weapons']['level']* player.total_strength
    
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
        self.production_count += 1
                       
            
class PlayerModel:
    
    def __init__(self, team, name, game, 
                 stars = DEFAULT_STARS , 
                 researching='scanning', 
                 techs = DEFAULT_TECH, priorities=TECHNOLOGIES, 
                 funds = 300, spend=SPEND, carriers = 1,
                 target_stars = 6,
                 ships = 50,
                 growth_modifier = 1):
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
        self.refresh()
        self.spend_history = []
        self.growth_modifier = growth_modifier

        
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
               'ships_per_tick' : self.ships_per_tick,
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
            
        self.refresh()
    
    
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
        tech_cost = current_level * 25
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
        if self.game == None:
            ticks = 20
        else:
            ticks = self.game.production
            
        tech = self.techs['manufacturing']['level']
        self.ships_per_tick = (self.total_industry * ( 5 + tech) / ticks)
    
    
    def refreshTotals(self):
        '''Refreshes total numbers based upon star data'''
        self.total_strength = sum([i['st'] for i in self.stars])
        self.total_science  = sum([i['s'] for i in self.stars])
        self.total_economy  = sum([i['e'] for i in self.stars])
        self.total_industry = sum([i['i'] for i in self.stars])
        self.total_stars = len(self.stars)
        try:
            self.star_quality = statistics.mean([i['nr'] for i in self.stars])
        except statistics.StatisticsError:
            self.star_quality = 0
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
    
    
    def buyInfra(self, infratype, funds, stars = None, bought = 0, forecast=False): 
        '''Buys the cheapest infratype until it runs out of funds, returning remaining funds'''
        
        if forecast == True:
            dup = copy.deepcopy(self)
            return dup.buyInfra(infratype, funds, stars, bought)
        
        
        if funds > self.funds:
            funds = self.funds
            
        if infratype == 'o':
            self.funds -= funds
            return {'type' : infratype, 'funds' : 0, 'bought' : 0}
        
        if stars == None:
            stars = self.stars
        
        stars = sorted(stars, key = lambda x : self.priceInfra(infratype, x))
        
        cost = self.priceInfra(infratype, stars[0])
      
        #TODO add spend history entry
        if funds < cost:
            return {'type' : infratype, 'funds' : funds, 'bought' : bought}
        else:
            stars[0][infratype] += 1
            funds -= cost
            bought += 1
            self.funds -= cost
            self.refresh()
         
            return self.buyInfra(infratype, funds, stars, bought)
        

        
    def spendFunds(self, forecast = False, remainder='e'):
        '''Spends all funds according to the spending priorities set''' 
        #TODO Uses total funds if no number has been provided
        #TODO expect bug is from using funds not self.funds

        if forecast == True:
            player = copy.deepcopy(self)
            return player.spendFunds(forecast=False)

        total_priorities = sum(self.spend.values())
        ratio = self.funds // total_priorities
        
        results = {}
        
        for k,v in self.spend.items():
            funds = ratio * v
            purchase = self.buyInfra(k, funds)
            results[k] = {'bought' : purchase['bought'], 
                          'spent'  : funds - purchase['funds']}        
        #Remainder spend 
        funds = self.funds
        purchase = self.buyInfra(remainder, funds)
        results[remainder]['bought'] += purchase['bought']
        results[remainder]['spent'] += funds - purchase['funds']
  
        self.refresh()
        
        history_entry = [{'production' : self.game.production_count,
                         'type'       : k,
                         'bought'     : v['bought'],
                         'spent'      : v['spent']}
                         
                         for k,v in results.items()
                         ]
        self.spend_history.append(history_entry)
        
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
                 tech_level = 1,
                 ships = 100,
                 star_growth = 5,
                 growth_type = 'new',
                 runs = 1):
        self.teams = teams
        self.production_rate = production_rate
        self.production_number = production_number
        self.model = model
        self.tech_level = tech_level
        self.ships = ships
        self.star_growth = star_growth
        self.growth_type = growth_type
        self.last_run = None
        self.runs = runs

    @staticmethod
    def loadFromFile(config, teams, engine='openpyxl'):
        '''Returns a Model using settings from config and teams files'''
        
        #Helper function to convert comma sep fields to tuple
        def convert_priorities(string):
            result = string.split(sep=",")
            result = [i.replace(' ', '') for i in result]
            result = tuple(result)
            return result
        
        
        teams = pd.read_excel(teams, 
                              converters = {'priorities' : convert_priorities},
                              engine = engine)
        
        teams = teams.transpose().to_dict()
        teams = [v for v in teams.values()]
        
        for i in teams:
            spend = {}
            for k in INFRATYPES.keys():
                spend[k] = i.pop(k)
            i['spend'] = spend


        return Model(teams = teams,
                     production_rate = config['production_rate'],
                     production_number= config['production_number'],
                     model = config['model'],
                     tech_level = config['tech_level'],
                     ships = config['ships'],
                     star_growth = config['star_growth'],
                     growth_type = config['growth_type'],
                     runs = config['runs'])
        
    def runModel(self, filepath):  
        '''Runs a scenario based upon the model settings and saves the results to the filepath'''
        results = []
        for run in range(self.runs):
            game = Game(production = self.production_rate)
            self.last_run = game
            game.createModel(self.model['weapons'], self.model['ships'])
          
            for i in self.teams:
                team = i['team']
                name = i['name']
                priorities = i['priorities']
                spend = i['spend']
                funds = i['funds']
                target_stars = i['stars']
                growth_modifier= i['growth']
                game.addPlayer(team, name, priorities, spend, funds, 
                               target_stars = target_stars,
                               growth_modifier = growth_modifier)

                    
            game.setTech(self.tech_level)
    
           
            for i in range(500): 
                game.addStar()
            
            game.addShips(self.ships)
            game.spendFunds()
            
            
            for i in range(self.production_number):
                game.growStars(self.star_growth, self.growth_type)
                        
                game.advanceDay()
                for p in game.players:
                    entry = p.toDict()
                    entry['Production'] = i
                    entry['Run'] = run
                    for h in p.spend_history[-1]:
                            entry[h['type'] + ' Bought'] = h['bought']
                            entry[h['type'] + ' Spent'] = h['spent']
                            try:
                                entry[h['type'] + ' Average'] =  h['spent'] / h['bought']
                            except ZeroDivisionError:
                                entry[h['type'] + ' Average'] = 0
                    results.append(entry)
                    
        pd.DataFrame(results).to_csv(filepath)
        return results
  


