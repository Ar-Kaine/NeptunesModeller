# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:05:03 2020

@author: jamie
"""

from NeptunesModeller import Model
import json


#Change these to the filepaths for your teams and config templates
config = "./config templates/modeller_template.json"
teams = "./inputs/team_other.xlsx"


#Run this script without changing anything below
if __name__ == "__main__":
    
    config = json.load(open(config,'r'))
    
    model = Model.loadFromFile(config, teams)
    model.runModel(config['output'])
