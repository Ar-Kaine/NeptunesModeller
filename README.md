# NeptunesModeller
This is a collection of scripts for modelling, predicting or managing connections to Neptune's pride.

The various tools in here use libraries that come as standard as part of the Anacondas distribution of Python. If you are not a python expert and want to use any of these tools, you will find it easiest if you install Anacondas as everything should run smoothly if you do. 

This is very much a work in progress. Speak to me in Discord (Kaine) or elsewhere if you want more detail.

## NeptunesModeller
This is the main engine that drives other scripts. Running this file will do nothing: it is the common code used by the other files. 

## Forecaster
The Forecaster allows you to set your spending priorities and see what you can build by spending all of your cash. 

Spending priorities are setup as a ratio of e (economy), i (industry), s (science) and o (other). If you want to do it as cash rather than ratio, just do the maths so the total adds up to your total funds. This assumes you are always building in the least expensive location

The Forecaster will print the results for what you will build, at what price and how much is remaining, for both your current terraforming level and the next one up. This assumes you bought the level, so funds for purchasing that level will be subtracted. 

