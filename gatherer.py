import os
import json
import time
import requests
from lor_deckcodes import LoRDeck

# Default port will always be 21337, will assume no one has changed it for now
localHost = 'http://localhost:21337'
secretKey = ''

#Information we want to store
playerName = ''
opponentName = ''
activeDeck = ''
cardsInDeck = {}
regions = []
screenDimensions = {}
rectangles = {}
oldRectangles = []
rectangleLog = 0
expWins = 0
expLosses = 0

previousState = 'Offline'

#Loop forever
def Main():
	GetSecretKey()

	global previousState, previousExpeditionState
	while(1):
		gameState = GetActiveDeck()[0]
		if gameState == 'Offline':
			OfflineState()
			previousState = 'Offline'
		elif gameState == None:
			MenuState()
			previousState = 'Menus'
		else:
			InGameState()
			previousState = 'InGame'
		time.sleep(5)

def OfflineState():
	if previousState == 'InGame':
		# If the next state is Offline assume the player lost
		UploadGameStatistics(False)
	return

def MenuState():
	if previousState == 'InGame':
		UploadGameStatistics(GetGameResult())
	return

def InGameState():
	global rectangles, rectangleLog, oldRectangles

	if previousState != 'InGame':
		AssignStaticValues()
	else:
		rect = GetCardPositions()
		if len(rectangles.keys()) == 0 or rect != oldRectangles:
			rectangles.update({f"frame{rectangleLog}" : rect})
			rectangleLog = rectangleLog + 1
			oldRectangles = rect
	return

def AssignStaticValues():
	global playerName, opponentName, screenDimensions, activeDeck, cardsInDeck, expWins, expLosses, regions
	playerName, opponentName, screenDimensions = GetGameInfo()
	activeDeck, cardsInDeck = GetActiveDeck()
	regions = []
	deck = LoRDeck.from_deckcode(activeDeck)
	for card in list(deck):
		if card[4:6] == "DE" and "Demacia" not in regions:
			regions.append("Demacia")
		elif card[4:6] == "FR" and "Freljord" not in regions:
			regions.append("Freljord")
		elif card[4:6] == "IO" and "Ionia" not in regions:
			regions.append("Ionia")
		elif card[4:6] == "NX" and "Noxus" not in regions:
			regions.append("Noxus")
		elif card[4:6] == "PZ" and "Piltover & Zaun" not in regions:
			regions.append("Piltover & Zaun")
		elif card[4:6] == "SI" and "Shadow Isles" not in regions:
			regions.append("Shadow Isles")
	regions = sorted(regions)
	expWins, expLosses = GetExpeditionInfo()

def UploadGameStatistics(localPlayerWon):
	global rectangleLog
	allRegions = ''
	newExpWins = 0
	newExpLosses = 0
	
	if GetCardCount(activeDeck) < 40:
		gameMode = 'Expedition'
	else:
		gameMode = 'Normal'

	if localPlayerWon and gameMode == 'Expedition':
		newExpWins = expWins + 1
		newExpLosses = expLosses
	elif gameMode == 'Expedition':
		newExpWins = expWins
		newExpLosses = expLosses + 1
	
	for region in regions:
		allRegions += region + " + "

	data = [("player", playerName),
        ("opponent", opponentName),
		("gameMode", gameMode),
		("expeditionWins", newExpWins),
		("expeditionLosses", newExpLosses),
        ("deckCode", activeDeck),
		("regions", allRegions[:-3]),
        ("win", localPlayerWon),
		("secretKey", secretKey),
		("replay", json.dumps(rectangles))]
	
	requests.post(url = "https://loroverseer.herokuapp.com/addGame/", data = data)
	rectangleLog = 0
	

# Accessed using http://localhost:{port}/static-decklist
# Returns:
# String DeckCode (Gives us the deck code so we can monitor deck winrates)
# Dictionary{string cardname:int amount} CardsInDeck (Faster to use this to grab cards and factions then to to use the deck code and loop through it)
# Above values return null if the player is not in an active game. We can therefore use it to know if the player is in a game
def GetActiveDeck():
	#with open('activeDeck.json') as f:
	#	results = json.load(f)
	requestLink = localHost + '/static-decklist'
	try:
		r = requests.get(requestLink)
	except:
			return "Offline", "Offline"
	results = r.json()
	return results['DeckCode'], results['CardsInDeck']


# Accessed using http://localhost:{port}/positional-rectangles
# GetGameInfo returns:
# String Player Name (Local player name useful to make sure we are tracking the right player)
# String OpponentName (His opponent, useful for match history)
# Dictionary{string:integer} Screen (Width and Height of the players screen, will probably have to resize all those to a default)
# GetCardPositions returns:
# Array of dictionaries{string:integer} Rectangles (Gives information such as card ID, code, and positions relative to the screen size)
# Recommended to only call every second. Depending on how it works will either call ever second or every 5 seconds
# Either way will only store the information if the rectangles have different positions then the previous one
def GetGameInfo():
	#with open('cardPositions.json') as f:
	#	results = json.load(f)
	requestLink = localHost + '/positional-rectangles'
	try:
		r = requests.get(requestLink)
	except:
		return "Offline", "Offline", "Offline"
	results = r.json()
	return results['PlayerName'], results['OpponentName'], results['Screen']

def GetExpeditionInfo():
	#with open('expedition.json') as f:
	#	results = json.load(f)
	requestLink = localHost + '/expeditions-state'
	try:
		r = requests.get(requestLink)
	except:
		return 0, 0
	results = r.json()
	return results['Wins'], results['Losses']

def GetCardPositions():
	#with open('cardPositions.json') as f:
	#	results = json.load(f)
	requestLink = localHost + '/positional-rectangles'
	try:
		r = requests.get(requestLink)
	except:
		return "Offline"
	results = r.json()
	return results['Rectangles']

# Accessed using http://localhost:{port}/game-result
# Returns: 
# Integer GameID (Not very useful since it resets whenever client resets)
# Boolean LocalPlayerWon (Returns if the player won or lost the game)
# Going to call this function when GetActiveDeck returns null so we know who won and with what deck
def GetGameResult():
	#with open('gameResult.json') as f:
	#	results = json.load(f)
	requestLink = localHost + '/game-result'
	try:
		r = requests.get(requestLink)
	except:
		return "Offline"
	results = r.json()
	return results['LocalPlayerWon']

def GetCardCount(deck):
	unpackedDeck = LoRDeck.from_deckcode(deck)
	cardCount = 0

	for card in list(unpackedDeck):
		cardCount += int(card[0])
	return cardCount

def GetSecretKey():
	global secretKey

	if os.path.isfile('.secretKey'):
		f = open(".secretKey", "r") 
		secretKey = f.read()
	else:
		print("To get the most our of LoR Overseer, create an account in order to track your personal stats")
		print("If you do not yet have an account, you can register here: https://loroverseer.herokuapp.com/register/")
		print("If you already have an account, simply copy paste the secret key on your profile page: https://loroverseer.herokuapp.com/profile/")
		newSecretKey = input("Secret Key: ")

		f = open(".secretKey","w")
		f.write(newSecretKey)
		secretKey = newSecretKey
		f.close
		print("Success")

Main()