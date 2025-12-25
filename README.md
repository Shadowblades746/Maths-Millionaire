# Maths millionaire
### Video Demo: https://youtu.be/WAMkmm6zFkk
### Website: https://shadowblades746.github.io/Maths-Millionaire/

### -Description-

#### In this program, there is one simple goal: to get as rich as possible!

**Note:** `project.py` is the original desktop version that uses CSV files for data storage. `game.py` and `index.html` are new files created to work as a playable website using browser localStorage for persistent data storage.

### -commands-

#### commands allow you to choose where you want to go. you can go to the welcome screen by suffixing "_w". below are all the commands that you need:

- /home - this brings you back home
- /games - this brings you to the games
- /market - this brings you to the market
- /money - this brings you to the money market
- /pv - this brings you to the profile viewer

### -you have three funds namely-

- your wallet: which should be seen as temporary storage as it has no perks
- your bank: which gains interest at a rate of 10% per day! so ensure to use it
- the blockchain: which stores bitcoin so if you like the idea of crypto then go use it

### -games-

- there are maths games which allow you to earn money by solving simple math problems
- there are three main difficulties so ensure to choose wisely based on your skill level
- you can try your luck at either addition, subtraction, multiplication or division

### -rank system-

- you get a higher rank based on how good you do in the games which depends on your score
- your score is added to your rank level every time you complete one of the games
- when playing games, the higher your rank level, the more money you earn per game

### -market-

- there is a market which allows you to buy and sell items to add to your collection
- you can even go to the black market which allows you to buy and sell special items

### -money market-
#### here you can do things like:

- deposit money from your wallet to your bank account
- withdraw money from your bank account
- convert money from your bank to the blockchain
- check all of your balances

### -profile viewer-

- you can check all of your stats here
- your bank balance
- your inventory
- your rank

### -backend-

there are feeder classes for each element which do all the behind the scenes work. the main classes for each element just use the methods of the feeder classes in order to do all the operations while abstracting away any unnecessary information. there is a command system that allows you to get around the program which the user operates at the end of each action. if the user does anything that isn't allowed, an error is raised which will prompt the reader to rerun the program and give a brief description of the error. I had to include 3 filler functions as the pontifications did not allow me to embed my functions within classes.

### -the code explained-

#### -Commands-

Calls the relevant function when a command is run.

#### -money converter-

Converts bitcoin to pounds and pounds to bitcoin using API to get the current exchange rates.

#### -funds-

**Desktop Version (project.py):** The fiat bank has functions that deposit, withdraw, check balance, add interest and save balance which each do what they do by going into a csv file and changing the numbers. The blockchain and wallet both inherit from this class but save into a different csv file.

**Website Version (game.py):** The fiat bank has functions that deposit, withdraw, check balance, add interest and save balance which each do what they do by using browser localStorage to persist data. The blockchain and wallet both use the same approach but save into different localStorage keys.

#### -money market-

This class has a welcome message with instructions and allows the user to input what they want to do, calling the relevant functions to do what the user wanted.

#### -games-

**Desktop Version (project.py):** Has a function that sets the game mode and difficulty, a function that saves your rank to a csv file, a multiplier function which grants the user a prize based on his score, a set integer multiplier and the users rank. There are functions for addition, subtraction, division, and multiplication which printout 10 simple sums for the user to answer depending on the difficulty level these can be up to 3 digits long.

**Website Version (game.py):** Has a function that sets the game mode and difficulty, a function that saves your rank to browser localStorage, a multiplier function which grants the user a prize based on his score, a set integer multiplier and the users rank. There are functions for addition, subtraction, division, and multiplication which printout 10 simple sums for the user to answer depending on the difficulty level these can be up to 3 digits long.

#### -game house-

This class prints out a welcome message and lets the user select the difficulty and mode for their math game and then deposits the money into the bank for the user.

#### -shops-

**Desktop Version (project.py):** This class has an initialisation function which initialises the list of items on sale with the price along with a graphic version of the list. There are functions to get the item name, get the price and with this info it can use csv files to store any item you buy and take away any item you sell. It also has 4 different functions depending on whether you are buying or selling from the shop or the black market which will in turn call the relevant functions. There are 2 information functions which print the items and their prices graphically.

**Website Version (game.py):** This class has an initialisation function which initialises the list of items on sale with the price along with a graphic version of the list. There are functions to get the item name, get the price and with this info it uses browser localStorage to store any item you buy and take away any item you sell. It also has 4 different functions depending on whether you are buying or selling from the shop or the black market which will in turn call the relevant functions. There are 2 information functions which print the items and their prices graphically.

#### -market-

This class prints out a welcome message and lets the user input what they want to do in the market and then calls the relevant functions.

#### -profile viewer-

This class prints out a welcome message and has three functions to grab the users rank, inventory and funds, printing it all out graphically.

#### -welcome-

This class prints out a welcome message and adds the daily interest if it hasn't already been added that day.
