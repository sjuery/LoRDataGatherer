<h3 align="center">Legends Of Runeterra Data Gatherer</h3>

---

<p align="center"> Simple Python data gatherer for the new League of Legends card game legends of runeterra.
    <br> 
</p>


## 📝 Table of Contents
- [Problem Statement](#problem_statement)
- [Idea / Solution](#idea)
- [Dependencies / Limitations](#limitations)
- [Future Scope](#future_scope)
- [Setting up a local environment](#getting_started)
- [Usage](#usage)
- [Authors](#authors)

## 🧐 Problem Statement <a name = "problem_statement"></a>
Riot Games organised a quick hackathon like event to test out their API for their game "Legends of Runeterra". Our task was to create anything we wanted using their API so they could find any flaws and advantages the system had and figure out how to improve it. This competition lasted from November 11th at 10 AM PST until November 22nd at 10 AM PST. The end result will be graded on the following:
- DIFFICULTY: How difficuly was it to create it
- CLARITY/PRESENTATION: How easy is it for someone to pickup and use your product
- POLISH: How close is the project to a finished product
- DOCUMENTATION: How well documented is it (Hense this readme 🧐)

## 💡 Idea / Solution <a name = "idea"></a>
The legends of runettera client broadcasts all of its client data to "http://localhost:21337". Since my plan was to create a website that collects as much information as possible (https://github.com/sjuery/lorOverseer), I needed to send all of this data to my website. This is where LoRDataGatherer comes in. Whenever a player finishes a game, it collects all the required information and sends it for processing to the website (https://loroverseer.herokuapp.com/).

Here is all the information that can be gathered from the API (More info on the official website https://developer.riotgames.com/docs/lor#game-client-api):
http://localhost:21337/static-decklist:
- DeckCode (a string telling us what deck the host is currently playing )
- CardsInDeck(a dictionary with every card in above mentioned deck)
http://localhost:21337/positional-rectangles
- PlayerName (a string with the Username of the host)
- OpponentName (a string with the Username of his opponent)
- Screen (a dictionary with the width and height of the players screen)
- rectangles (an array of dictionaries with information such as what card is on what screen coordinate)
http://localhost:21337/expeditions-state
- IsActive (bool telling us if the player has an active expedition)
- State (string that returns what the player is doing with the expedition)
- Record (array of strings[Either win, or loss] indicating in what order the host won/lost their games)
- Deck (array of strings with the cardCode of every card in deck)
- Games (integer with the total amount of games)
- Wins (integer with the amount of wins)
- Losses (integer with the amount of losses)
http://localhost:21337/game-result
- GameID (an integer with the ID of the game [resets everytime the client restarts])
- LocalPlayerWon (a boolean indicating if the host won or lost the match)

The LoRDataGatherer loops forever until closed and can detect when the player is in an active game by using the 'static-decklist' part of the API because the DeckCode will only be returned if a the player is currently in a game.

Once the app knows the player is in an active game, it sets all of the data that will not change throughout the games entire duration such as:
- PlayerName
- OpponentName
- DeckCode
- Regions
- Screen Size
- Expedition wins,losses,total games...
And once that is done, it adds every rectangle information found in the positional-rectangles part of the API to a dictionary (Does this every 5 seconds if the rectangles have changed position)

Once the DeckCode finally returns null again, all of the information collected gets sent to my website using a post request. And the app begins searching for its next available game. 

## ⛓️ Dependencies / Limitations <a name = "limitations"></a>
The python version of the project has the following dependencies:
- JSON
- Requests
- lor_deckcodes
All of which can be installed using pip

I have however also included a rar with an executable that will be able to run without the need of Python or any of the above dependencies.

## 🚀 Future Scope <a name = "future_scope"></a>
Gonna fill this in after the project is over

## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development 
and testing purposes.

### Prerequisites

```
If you download the RaR there are no Prerequisites, however, if you want to run the Python version:
Python 3.8 (Only version I tested it on but im sure it works on 3.7)
The dependencies found here [Dependencies](#limitations)
```

### Installing

To install and run the project with the rar file:

```
1) Download the project
2) Unrar the rar file named gatherer.rar
3) Extract it wherever you want
4) Open the gatherer folder
5) run the gatherer.exe file
```

To install and run the project with the .py file

```
1) Clone the repo (https://github.com/sjuery/LoRDataGatherer.git)
2) cd into the directory
3) pip install 'nameOfDependencies'
4) python gatherer.py
```

## 🎈 Usage <a name="usage"></a>
Once the app is running it will prompt you for a secret key. In order to get your secret key:
1) Create an account if you haven't already (https://loroverseer.herokuapp.com/register/)
2) Login to your account (https://loroverseer.herokuapp.com/login/)
3) Head over to your profile (https://loroverseer.herokuapp.com/profile/)
4) Copy and paste the SecretKey from the website to the console.
5) Press enter
6) Play Legends Of Runeterra
7) Track your stats on your profile page


## ⛏️ Built With <a name = "tech_stack"></a>
- [Python](https://www.python.org/) - Python
- [LoRDeckCodes](https://github.com/Rafalonso/LoRDeckCodesPython) - LoRDeckCodes

## ✍️ Authors <a name = "authors"></a>
- [@sjuery](https://github.com/sjuery)
