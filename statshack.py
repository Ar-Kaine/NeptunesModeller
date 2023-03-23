# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 13:45:14 2022

@author: jamie
"""

from scipy.stats import fisher_exact as fe
from pandas import DataFrame as df

data = { ('Off Center', 'AFK') : [[43 , 113],[200 , 584]]  , 
        ('Off Corner', 'AFK') : [[107 , 309],[136 , 388]]  , 
        ('True Center', 'AFK') : [[54 , 154],[189 , 543]]  , 
        ('True Corner', 'AFK') : [[39 , 121],[204 , 576]]  , 
        ('Off Center', 'Survived') : [[23 , 133],[182 , 602]]  , 
        ('Off Corner', 'Survived') : [[80 , 336],[125 , 399]]  , 
        ('True Center', 'Survived') : [[56 , 152],[149 , 583]]  , 
        ('True Corner', 'Survived') : [[46 , 114],[159 , 621]]  , 
        ('Off Center', 'Podium') : [[12 , 144],[109 , 675]]  , 
        ('Off Corner', 'Podium') : [[55 , 361],[66 , 458]]  , 
        ('True Center', 'Podium') : [[41 , 167],[80 , 652]]  , 
        ('True Corner', 'Podium') : [[13 , 147],[108 , 672]]  ,
        ('Off Center', 'Over 10') : [[3 , 153],[66 , 718]]  , 
        ('Off Corner', 'Over 10') : [[19 , 397],[50 , 474]]  ,
        ('True Center', 'Over 10') : [[15 , 193],[54 , 678]]  , 
        ('True Corner', 'Over 10') : [[32 , 128],[37 , 743]]  ,
        ('Off Center', 'Winner') : [[1 , 155],[17 , 767]]  , 
        ('Off Corner', 'Winner') : [[6 , 410],[12 , 512]]  , 
        ('True Center', 'Winner') : [[6 , 202],[12 , 720]]  ,
        ('True Corner', 'Winner') : [[5 , 155],[13 , 767]]  } 






tests =  ['two-sided','less','greater']
finalresults = {'Survived' : {'Off Center' : {} ,
                              'Off Corner' : {} ,
                              'True Center' : {} ,
                              'True Corner' : {}} ,
                'Podium' : {'Off Center' : {} ,
                              'Off Corner' : {} ,
                              'True Center' : {} ,
                              'True Corner' : {}} ,
               'Winner' : {'Off Center' : {} ,
                              'Off Corner' : {} ,
                              'True Center' : {} ,
                              'True Corner' : {}} ,
                'Over 10' : {'Off Center' : {} ,
                              'Off Corner' : {} ,
                              'True Center' : {} ,
                              'True Corner' : {}} ,
                'AFK' :{'Off Center' : {} ,
                              'Off Corner' : {} ,
                              'True Center' : {} ,
                              'True Corner' : {}} 
                }

for k,v in data.items():
    a = k[1]
    b = k[0]
    for i in tests:
        results = fe(v,i)[1]
        results = round(results*100,2)
        finalresults[a][b][i] = results

survived = df(finalresults['Survived']).transpose()
podium = df(finalresults['Podium']).transpose()    
overten = df(finalresults['Over 10']).transpose()
afk = df(finalresults['AFK']).transpose()
winner = df(finalresults['Winner']).transpose()