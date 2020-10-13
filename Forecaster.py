# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 15:20:32 2020

This script is used to forecast whether is is worth purchasing Terraforming
before production, or if you should wait until afterwards.

@author: jamie
"""
import NeptunesModeller as nm


#Change the config filepath to one that has your Game ID and API Key
config_file = './inputs/forecaster.json'

#Run the script wihout editting the below
if __name__ == "__main__":
    
    connection = nm.Connection(filename = config_file)
    
    
    
    


