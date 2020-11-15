# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:05:03 2020

@author: jamie
"""

from NeptunesModeller import Model
import json


#Change these to the filepaths for your teams and config templates
config = "./inputs//modeller_10k10.json"
teams = "./inputs/team_science.xlsx"


#Run this script without changing anything below
if __name__ == "__main__":
    
    config = json.load(open(config,'r'))
    
    model = Model.loadFromFile(config, teams)
    results = model.runModel(config['output'])
