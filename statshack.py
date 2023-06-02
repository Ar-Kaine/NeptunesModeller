# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 13:45:14 2022

@author: jamie
"""

from scipy.stats import fisher_exact as fe
from pandas import DataFrame as df

data = { ('Outside Center', 'AFK') : [[142 , 402],[449 , 1183]]  , 
        ('Off Corner', 'AFK') : [[231 , 585],[360 , 1000]]  , 
        ('Inside Center', 'AFK') : [[78 , 194],[513 , 1391]]  , 
        ('True Corner', 'AFK') : [[140 , 404],[451 , 1181]]  , 
        ('Outside Center', 'Survived') : [[86 , 458],[329 , 1303]]  , 
        ('Off Corner', 'Survived') : [[161 , 655],[254 , 1106]]  , 
        ('Inside Center', 'Survived') : [[34 , 238],[381 , 1523]]  , 
        ('True Corner', 'Survived') : [[134 , 410],[281 , 1351]]  , 
        ('Outside Center', 'Podium') : [[21 , 523],[81 , 1551]]  , 
        ('Off Corner', 'Podium') : [[33 , 783],[69 , 1291]]  , 
        ('Inside Center', 'Podium') : [[9 , 263],[93 , 1811]]  , 
        ('True Corner', 'Podium') : [[39 , 505],[63 , 1569]]  , 
        ('Outside Center', 'Over 10') : [[50 , 494],[241 , 1391]]  , 
        ('Off Corner', 'Over 10') : [[113 , 703],[178 , 1182]]  , 
        ('Inside Center', 'Over 10') : [[19 , 253],[272 , 1632]]  , 
        ('True Corner', 'Over 10') : [[109 , 435],[182 , 1450]]  , 
        ('Outside Center', 'Winner') : [[4 , 540],[30 , 1602]]  , 
        ('Off Corner', 'Winner') : [[13 , 803],[21 , 1339]]  , 
        ('Inside Center', 'Winner') : [[2 , 270],[32 , 1872]]  , 
        ('True Corner', 'Winner') : [[15 , 529],[19 , 1613]]  } 


data2 = { ('Outside Center', 'AFK') : [[142 , 402],[309 , 779]]  , 
         ('Off Corner', 'AFK') : [[231 , 585],[220 , 596]]  ,
         ('Inside Center', 'AFK') : [[78 , 194],[373 , 987]]  , 
         ('Outside Center', 'Survived') : [[86 , 458],[195 , 893]]  ,
         ('Off Corner', 'Survived') : [[161 , 655],[120 , 696]]  , 
         ('Inside Center', 'Survived') : [[34 , 238],[247 , 1113]]  , 
         ('Outside Center', 'Podium') : [[21 , 523],[42 , 1046]]  , 
         ('Off Corner', 'Podium') : [[33 , 783],[30 , 786]]  , 
         ('Inside Center', 'Podium') : [[9 , 263],[54 , 1306]]  , 
         ('Outside Center', 'Over 10') : [[50 , 494],[132 , 956]]  , 
         ('Off Corner', 'Over 10') : [[113 , 703],[69 , 747]]  , 
         ('Inside Center', 'Over 10') : [[19 , 253],[163 , 1197]]  , 
         ('Outside Center', 'Winner') : [[4 , 540],[15 , 1073]]  , 
         ('Off Corner', 'Winner') : [[13 , 803],[6 , 810]]  , 
         ('Inside Center', 'Winner') : [[2 , 270],[17 , 1343]]  , }




tests =  ['two-sided','less','greater']
finalresults = {'Survived' : {'Outside Center' : {} ,
                              'Off Corner' : {} ,
                              'Inside Center' : {} ,
                              'True Corner' : {}} ,
                'Podium' : {'Outside Center' : {} ,
                              'Off Corner' : {} ,
                              'Inside Center' : {} ,
                              'True Corner' : {}} ,
               'Winner' : {'Outside Center' : {} ,
                              'Off Corner' : {} ,
                              'Inside Center' : {} ,
                              'True Corner' : {}} ,
                'Over 10' : {'Outside Center' : {} ,
                              'Off Corner' : {} ,
                              'Inside Center' : {} ,
                              'True Corner' : {}} ,
                'AFK' :{'Outside Center' : {} ,
                              'Off Corner' : {} ,
                              'Inside Center' : {} ,
                              'True Corner' : {}} 
                }

for k,v in data2.items():
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




finalresults2 = {'Survived' : {'Outside Center' : {} ,
                              'Off Corner' : {} ,
                              'Inside Center' : {}} ,
                'Podium' : {'Outside Center' : {} ,
                              'Off Corner' : {} ,
                              'Inside Center' : {}} ,
               'Winner' : {'Outside Center' : {} ,
                              'Off Corner' : {} ,
                              'Inside Center' : {}} ,
                'Over 10' : {'Outside Center' : {} ,
                              'Off Corner' : {} ,
                              'Inside Center' : {}} ,
                'AFK' :{'Outside Center' : {} ,
                              'Off Corner' : {} ,
                              'Inside Center' : {}} 
                }

for k,v in data2.items():
    a = k[1]
    b = k[0]
    for i in tests:
        results = fe(v,i)[1]
        results = round(results*100,2)
        finalresults2[a][b][i] = results

survived2 = df(finalresults2['Survived']).transpose()
podium2 = df(finalresults2['Podium']).transpose()    
overten2 = df(finalresults2['Over 10']).transpose()
afk2 = df(finalresults2['AFK']).transpose()
winner2 = df(finalresults2['Winner']).transpose()