# NeptunesModeller
This is a collection of scripts for modelling, predicting or managing connections to Neptune's pride.

The various tools in here use libraries that come as standard as part of the Anacondas distribution of Python. If you are not a python expert and want to use any of these tools, you will find it easiest if you install Anacondas as everything should run smoothly if you do. 

This is very much a work in progress. Speak to me in Discord (Kaine) or elsewhere if you want more detail.

##NeptunesModeller
This is the main engine that drives other scripts. Running this file will do nothing: it is the common code used by the other files. 

##Forecaster
The forecaster is currently setup to answer a single question: should I buy terraforming before I invest in economy, or should I wait to buy terraforming after production?

The user needs to save a config.json file somewhere, with a game ID and API key so it can read their data. In the script, change the filepath for the config file to match your file, then run the script. The results will be printed to the console. 


