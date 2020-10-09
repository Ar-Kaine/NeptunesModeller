# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:05:03 2020

@author: jamie
"""

import NeptunesModeller

#These are the teams you are modelling. Teams are made up of as many players as you want.
teams = {'Manufacturing Lead' : [                                               #Team name
                {'name'       : 'Big Manu',                                     #Any name you recognise
                  'researching': ['manufacturing'],                              #Techs they will research
                  'stars'      : 50 ,                                            #number of stars will have in addition to starting stars           
                  'funds'      : 1000,                                           #starting cash  
                  'spending'   :  {'e' : 3 , 'i' : 3, 's' : 3 , 'o' : 2}},       #ratio of spending priorities
                {'name'       : 'Normal Terra',    
                  'researching': ['terraforming'], 
                  'stars'      : 25 ,        
                  'funds'      : 500,  
                  'spending'   :  {'e' : 3 , 'i' : 3, 's' : 3 , 'o' : 2}},
                {'name'       : 'Normal weapons',    
                  'researching': ['weapons'], 
                  'stars'      : 25 ,        
                  'funds'      : 500,  
                  'spending'   :  {'e' : 3 , 'i' : 3, 's' : 3 , 'o' : 2}}],
    #New team
          'Weapons Lead'       : [       
                {'name'       : 'Big Weapons',                                     
                  'researching': ['weapons'],                              
                  'stars'      : 50 ,                                            
                  'funds'      : 1000,                                           
                  'spending'   :  {'e' : 3 , 'i' : 3, 's' : 3 , 'o' : 2}},       
                {'name'       : 'Normal Terra',    
                  'researching': ['terraforming'], 
                  'stars'      : 25 ,        
                  'funds'      : 500,  
                  'spending'   :  {'e' : 3 , 'i' : 3, 's' : 3 , 'o' : 2}},
                {'name'       : 'Normal Manu',    
                  'researching': ['manufacturing'], 
                  'stars'      : 25 ,        
                  'funds'      : 500,  
                  'spending'   :  {'e' : 3 , 'i' : 3, 's' : 3 , 'o' : 2}}],
          #New Team
        'Terra Lead'       : [       
                {'name'       : 'Big Terra',                                     
                  'researching': ['terraforming'],                              
                  'stars'      : 50 ,                                            
                  'funds'      : 1000,                                           
                  'spending'   :  {'e' : 3 , 'i' : 3, 's' : 3 , 'o' : 2}},       
                {'name'       : 'Normal Manu',    
                  'researching': ['manufacturing'], 
                  'stars'      : 25 ,        
                  'funds'      : 500,  
                  'spending'   :  {'e' : 3 , 'i' : 3, 's' : 3 , 'o' : 2}},
                {'name'       : 'Normal weapons',    
                  'researching': ['weapons'], 
                  'stars'      : 25 ,        
                  'funds'      : 500,  
                  'spending'   :  {'e' : 3 , 'i' : 3, 's' : 3 , 'o' : 2}}]}
  
# teams = {'Econ Heavy'       : [       
#                 {'name'       : 'Big Terra',                                     
#                   'researching': ['terraforming'],                              
#                   'stars'      : 50 ,                                            
#                   'funds'      : 1000,                                           
#                   'spending'   :  {'e' : 6 , 'i' : 3, 's' : 3 , 'o' : 2}},       
#                 {'name'       : 'Normal Manu',    
#                   'researching': ['manufacturing'], 
#                   'stars'      : 25 ,        
#                   'funds'      : 500,  
#                   'spending'   :  {'e' : 6 , 'i' : 3, 's' : 3 , 'o' : 2}},
#                 {'name'       : 'Normal weapons',    
#                   'researching': ['weapons'], 
#                   'stars'      : 25 ,        
#                   'funds'      : 500,  
#                   'spending'   :  {'e' : 6 , 'i' : 3, 's' : 3 , 'o' : 2}}],
#     #New team
#     'Industry Heavy'          :  [       
#                 {'name'       : 'Big Terra',                                     
#                   'researching': ['terraforming'],                              
#                   'stars'      : 50 ,                                            
#                   'funds'      : 1000,                                           
#                   'spending'   :  {'e' : 3 , 'i' : 6, 's' : 3 , 'o' : 2}},       
#                 {'name'       : 'Normal Manu',    
#                   'researching': ['manufacturing'], 
#                   'stars'      : 25 ,        
#                   'funds'      : 500,  
#                   'spending'   :  {'e' : 3 , 'i' : 6, 's' : 3 , 'o' : 2}},
#                 {'name'       : 'Normal weapons',    
#                   'researching': ['weapons'], 
#                   'stars'      : 25 ,        
#                   'funds'      : 500,  
#                   'spending'   :  {'e' : 3 , 'i' : 6, 's' : 3 , 'o' : 2}}],
#           #New Team
#         'Science Heavy'       : [       
#                 {'name'       : 'Big Terra',                                     
#                   'researching': ['terraforming'],                              
#                   'stars'      : 50 ,                                            
#                   'funds'      : 1000,                                           
#                   'spending'   :  {'e' : 3 , 'i' : 3, 's' : 6 , 'o' : 2}},       
#                 {'name'       : 'Normal Manu',    
#                   'researching': ['manufacturing'], 
#                   'stars'      : 25 ,        
#                   'funds'      : 500,  
#                   'spending'   :  {'e' : 3 , 'i' : 3, 's' : 6 , 'o' : 2}},
#                 {'name'       : 'Normal weapons',    
#                   'researching': ['weapons'], 
#                   'stars'      : 25 ,        
#                   'funds'      : 500,  
#                   'spending'   :  {'e' : 3 , 'i' : 3, 's' : 6 , 'o' : 2}}]}      
if __name__ == "__main__":
    
    model = NeptunesModeller.Model(teams, production_number=80)
    model.runModel('output2.csv')
