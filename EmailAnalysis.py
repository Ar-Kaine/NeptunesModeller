# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 16:03:13 2021

@author: jamie
"""


import pandas as pd

datasource = "./outputs/email_dump.json"

data = pd.read_json(datasource)
game_details = pd.Series((zip(data.Id, data.Name, data.GameSize)))
game_details = game_details.unique()


