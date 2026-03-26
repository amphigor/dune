import random
import leaders
import conflicts
import cards
#vars
numplayers = None
players = []
firstTurnMarker = 0
#structs
class Player:
    def __init__(self, leader, water):
        self.leader = leader
        self.water = water
        self.sols = 0 # NO BANDS WHATSOEVER
        self.spice = 0 #no spice
        self.vp = 0
        self.combatPower = 0
        self.persuasion = 0

        self.maxTroops = 16
        self.deployedTroops = 0
        self.maxAgents = 2
        self.agents = 2
        self.isHighCouncil = False

        self.intrigueCards = []
        self.avDeck = []
        self.hand = []
        self.inPlay = []
        self.discard = []

        self.alliances = [] #might be better in game instance
        self.repFrem = 0
        self.repBene = 0
        self.repSpac = 0
        self.repEmpr = 0

def shuffleDiscard(player):
    if len(player.avDeck) == 0:
            #case 1: game just started, initialize
            if len(player.discard) == 0 and len(player.hand) == 0:
                random.shuffle(cards.allStartingCards)
                player.avDeck = cards.allStartingCards
            else:
                #case 2: discard empty because you drew too many
                if len(player.discard) == 0:
                    pass
                else: #case 3: ran out of deck from drawing so shuffle discard
                    player.avDeck = random.shuffle(player.discard)
                    player.discard = []

def drawCard(player, numToDraw):
    for i in range(numToDraw):
        if len(player.avDeck) == 0:
            shuffleDiscard(player)
        if len(player.avDeck) > 0:
            poppedCard = player.avDeck.pop() #Switch to deque before head hurts
            player.hand.append(poppedCard)

def discardHand(player):
    for card in player.inPlay:
        player.discard.append(card)
    player.inPlay = []

def setup():
    print("dune: imperium")
    print("insert num people - default 4")
    npinput = input()
    if npinput == "":
        numplayers = 4
    else:
        numplayers = max(int(npinput), 4)
    # do leader selection sometime
    leaderpack = leaders.init_leaders()
    # add option to choose!
    
    for i in range(numplayers):
        players.append(Player(None, 1))
        if numplayers == 4:
            players[i].vp = 1
    print(players)
    
    #setup conflict
    conflictList = conflicts.init_conflicts()

    #setup intrigue, imperium piles
    intrigueDeck = cards.init_intrigues()
    imperiumDeck = cards.init_imperium_deck() #needs Arrakis Liaison/SMF implementation

    for player in players:
        shuffleDiscard(player) #setup - Beware, cards all point to same card in memory for all plr
        print(player.avDeck)
    print("OK!")

setup()