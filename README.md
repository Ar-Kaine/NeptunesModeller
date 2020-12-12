# NeptunesModeller
This is a collection of scripts for modelling, predicting or managing connections to Neptune's pride.

The various tools in here use libraries that come as standard as part of the Anacondas distribution of Python. If you are not a python expert and want to use any of these tools, you will find it easiest if you install Anacondas as everything should run smoothly if you do. 

This is very much a work in progress. Speak to me in Discord (Kaine) or elsewhere if you want more detail.

Apart from NeptunsModeller, each of the tools in this library has been setup so you can run it using configuration files - either .json or .cab (or both). There are templates in the templates folder. You will need to change the code to point at the right file, but that's it.

## NeptunesModeller
This is the main engine that drives other scripts. Running this file will do nothing: it is the common code used by the other files. 

If you want to create your own tool using this code, reference this library.

## Forecaster
The Forecaster allows you to set your spending priorities and see what you can build by spending all of your cash. 

Spending priorities are setup as a ratio of e (economy), i (industry), s (science) and o (other). If you want to do it as cash rather than ratio, just do the maths so the total adds up to your total funds. This assumes you are always building in the least expensive location

The Forecaster will print to the console results for what you will build, at what price and how much is remaining, for both your current terraforming level and the next one up. This assumes you bought the level, so funds for purchasing that level will be subtracted. 

## Downloader
The downloader handles connecting to the API and downloads the data to Excel.

The config file should have the api_key, game_id and output_location fields. 

Data is currently almost untouched from the original API format. The only changes are:

Players:
1) Removal of the "war" and "count down to war" fields to a separate sheet (player_war)
2) Main player progress on technologies moved to a separate sheet  (player_technology)
3) Research levels have been split out to just so each tech level against a player

Stars:
1) Addition of a "distance" field to stars, which is the distance of the star to the centre

### Downloader: Known Issues
1) The error messages when a connection has failed are not  clear. If you get a "scanning_data" key error, it means your API key/Game ID combo did not work. You may need to regenerate an API key.




All other fields are in their original format. 

## Modeller
The modeller is used to model potential scenarios, such as which tech is best or the best division of spending.

At it's core is the concept of "model strength". This is a simple calculation of "weapons level * total ship number", which gives an easy comparison between players of how well their full fleet would perform in combat. 

Users will need to create an excel file with the relevant team information, and a config file with the settings for the model.

### Modeller: Known issues:
1) Config file is currently overriding certain information (starting techs and stars)
2) Some redundant information is in the config file and not used
