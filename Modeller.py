# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:05:03 2020

@author: jamie
"""

from NeptunesModeller import Model

config = {'output' : './outputs/teams_test.csv'}
teams = "./inputs/team_spending.xlsx"


if __name__ == "__main__":
    
    model = Model.loadFromFile(config, teams)
    model.runModel(config['output'])
