import random
import copy
import leaders
import conflicts
import cards
import board

import datavis
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
        self.hasRevealed = False

        self.maxTroops = 12 #16 for influence tracks though not relevant now
        self.deployedTroops = 0
        self.garrisonedTroops = 3
        self.maxAgents = 2
        self.agents = 2
        self.isHighCouncil = False

        self.intrigueCards = []
        self.avDeck = []
        self.hand = []
        self.inPlay = []
        self.discard = []

        #self.alliances = [] #might be better in game instance
        self.repFrem = 0
        self.repBene = 0
        self.repSpac = 0
        self.repEmpr = 0


        self.tempName = str(id(self))
        def __repr__(self):
            return self.tempName

class Game: #to simulate one game
    def __init__(self, numPlr, verbose=False):
        self.players = []
        self.numplayers = numPlr
        self.firstTurnMarker = random.randint(0, numPlr-1)
        self.conflictOrder = conflicts.init_conflicts()
        self.intrigueOrder = cards.init_intrigues()
        self.imperiumOrder = cards.init_imperium_deck()
        self.arrakisLiaisons = cards.init_reserve_AL()
        self.spiceMustFlow = cards.init_reserve_TSMF()
        self.board = board.Board()
        self.mentatAvailable = True
        self.currentTurn = -1 #0 based

        self.imperiumRow = []
        for i in range(5):
            goToRowCard = self.imperiumOrder.pop()
            self.imperiumRow.append(goToRowCard)

        self.highestScore = 0
        #self.leadingPlr = -1
        self.verbose = verbose

        self.winner = None

        self.stringMappings = {"Water":"water",
                            "Spice":"spice",
                            "Sol":"sols",
                            "Troop":"garrisonedTroops",
                            "Persuasion":"persuasion",
                            "Sword":"combatPower",
                            "InflF":"repFrem",
                            "InflB":"repBene",
                            "InflS":"repSpac",
                            "InflE":"repEmpr",
                            "VP":"vp"
                            }

        self.functionMappings = {"Draw": drawCard,
                                "Intrigue": self.drawIntrigue
                                 }

    def resolveEffects(self, player, effectsList, multiplier = 1):
        if player == None:
            return
        if effectsList == None:
            return
        for effectString in effectsList:
            numValue = int(effectString[0])
            effect = effectString[1:]
            mappedEffect = self.stringMappings.get(effect)
            functionEffect = self.functionMappings.get(effect)
            if mappedEffect:
                playerItemAmt = getattr(player, mappedEffect)
                setattr(player, mappedEffect, playerItemAmt+(numValue*multiplier))

            elif functionEffect:
                functionEffect(player, numValue)

    def checkBoardspaceCost(self, player, space):
        isOK = True
        spaceCost = space.cost
        if spaceCost != None:
            for effectString in spaceCost:
                numValue = int(effectString[0])
                effect = effectString[1:]
                mappedEffect = self.stringMappings.get(effect)
                if mappedEffect:
                    playerItemAmt = getattr(player, mappedEffect)
                    if playerItemAmt - numValue < 0:
                        isOK = False
                        break #formerly raise warning
                    else:
                        pass
        specialReq = space.specialReq
        if specialReq:
            for effectString in specialReq:
                numValue = int(effectString[0])
                effect = effectString[1:]
                mappedEffect = self.stringMappings[effect] #only for ST so whatever
                if mappedEffect:
                    playerItemAmt = getattr(player, mappedEffect)
                    if playerItemAmt - numValue < 0:
                        isOK = False
                        break#raise UserWarning("Special req fail")
                    else:
                        pass
        return isOK

    def promptPlayer(self, player, choice): #Play card effect? Trash? Resolve board or card first?
        def promptBoardCardOrder(player):
            pass
        def promptChooseImperium(player):
            print("which imperium card do you want - 0-4 IMP row 6 for AL 7 for TSMF and 9 nope")
            for index in range(len(self.imperiumRow)): #will now not break
                print(str(index) + ":" + self.imperiumRow[index].title + " - " + str(self.imperiumRow[index].persuasionCost))
            if self.arrakisLiaisons:
                print(self.arrakisLiaisons[0].title + " - " + str(self.arrakisLiaisons[0].persuasionCost))
            if self.spiceMustFlow:
                print(self.spiceMustFlow[0].title + " - " + str(self.spiceMustFlow[0].persuasionCost))
            print("you have " + str(player.persuasion) + " persuasion")
            userInput = int(input())

            if userInput == 9:
                return False
            else:
                try:
                    mappings = {6: self.arrakisLiaisons[0],
                        7: self.spiceMustFlow[0]
                        }
                    if mappings.get(userInput):
                        self.buyImperiumCard(player, mappings[userInput])
                    else:
                        self.buyImperiumCard(player, self.imperiumRow[userInput])
                except:
                    print("not a valid choice")
        def promptDeployTroops(player, predetermined=None):
            userInput = int(input("how many dudes do you want to deploy"))


        if choice == "shop":
            keepShopping = True
            while player.persuasion > 0 and keepShopping:
                shop = promptChooseImperium(player)
                if shop == False: 
                    keepShopping = False
        elif choice == "troop":
            promptDeployTroops(player)
                
    def deployTroops(self, player, number, maxDeployable):
        if player.garrisonedTroops < number:
            raise UserWarning("not enough troop") #warnings here, trycatch in prompts
        if number > maxDeployable:
            raise UserWarning("can't deploy that man")
        player.deployedTroops += number
        player.garrisonedTroops -= number
        player.combatPower += number*2


    def playCard(self, player, card, boardSpace):
        if not card in player.hand:
            raise UserWarning("Invalid move")
        if player.agents == 0:
            raise UserWarning("No agents")
        if boardSpace.isOccupied and card.title != "Kwisatz Haderach":
            raise UserWarning("Space already taken")
        if not boardSpace.access in card.locationAccess:
            raise UserWarning("Card can't go there")
        if not self.checkBoardspaceCost(player, boardSpace):
            raise UserWarning("Can't afford boardspace")

        self.resolveEffects(player, boardSpace.cost, -1)

        startingTroops = player.garrisonedTroops
        
        player.agents -= 1
        player.hand.remove(card)
        player.inPlay.append(card)
        boardSpace.isOccupied = True

        if boardSpace.flag != None:
            self.resolveEffects(boardSpace.flag, boardSpace.flagReward) #flag points to plr

        self.resolveEffects(player, boardSpace.reward)
        self.resolveEffects(player, card.onPlay)
        #resolve board effects
        #resolve card effects -- Prompt to decide order?
        troopsGainedOnTurn = player.garrisonedTroops - startingTroops
        #can prompt here, or return num deployable and have model call deploy function for however many valid
        #can also just prompt model at prompting function to get a value
        if boardSpace.isCombat:
            return troopsGainedOnTurn
        return -2

    def playIntrigue(self, player, card):
        self.resolveEffects(player, card.cost)
        self.resolveEffects(player, card.effects)
        
    def reveal(self, player):
        for card in player.hand:
            card.revealed = True

        player.inPlay.extend(player.hand)
        player.hand.clear()

        if player.isHighCouncil:
            player.persuasion += 2
        for card in player.hand: #prompt: order of reveal effects
            if card.revealed == True:
                #resolve card reveal effect
                self.resolveEffects(player, card.onReveal)
                card.revealed = False

        if player.deployedTroops == 0: #no troops -> no swords
            player.combatPower = 0

        #imperium row shopping - next needs robust prompting function > shop, deploy > combat resolution

        player.discard.extend(player.inPlay)
        player.inPlay.clear()
        player.hasRevealed = True
        player.persuasion = 0

    def resolveConflict(self): #missing intrigue actions, some conflict rewards
        #intrigue
        combatPowers = {}
        for player in self.players:
            if player.combatPower != 0 and player.deployedTroops > 0:
                combatPowers[player] = player.combatPower

        def calculateCurrentLeadingPower():
            currentLeaders = []
            if combatPowers:
                delayedPopList = []
                currentLeadingPwr = max(combatPowers.values())
                for player in combatPowers:
                    if player.combatPower == currentLeadingPwr:
                        currentLeaders.append(player)
                        #combatPowers.pop(player)
                        delayedPopList.append(player)
                for player in delayedPopList:
                    combatPowers.pop(player)
            return currentLeaders
        
        leadingPlrs = calculateCurrentLeadingPower()
        runnerUpPlrs = calculateCurrentLeadingPower()
        lastPlacePlrs = calculateCurrentLeadingPower()

        firstTied = len(leadingPlrs) > 1
        secondTied = len(runnerUpPlrs) > 1
        thirdTied = len(lastPlacePlrs) > 1
        firstPlace = leadingPlrs[0] if leadingPlrs else None
        secondPlace = runnerUpPlrs[0] if runnerUpPlrs else None
        lastPlace = lastPlacePlrs[0] if lastPlacePlrs else None

        currentCombat = self.conflictOrder[self.currentTurn]
        isFourPlrGame = self.numplayers >= 4

        if not isFourPlrGame: #BEWARE TERRIBLE IF STATEMENT AHEAD!!!!
            if firstTied:
                for player in leadingPlrs:
                    self.resolveEffects(player, currentCombat.rewards2)
            else:
                self.resolveEffects(firstPlace, currentCombat.rewards1)
                if secondTied:
                    for player in runnerUpPlrs:
                        self.resolveEffects(secondPlace, currentCombat.rewards3)
                else:
                    self.resolveEffects(secondPlace, currentCombat.rewards2)
        else:
            if firstTied:
                for player in leadingPlrs:
                    self.resolveEffects(player, currentCombat.rewards2)
                if secondTied:
                    pass #get zilch
                else:
                    if len(leadingPlrs) < 3: #dubious but for now
                        self.resolveEffects(secondPlace, currentCombat.rewards3)
            else:
                self.resolveEffects(firstPlace, currentCombat.rewards1)
                if secondTied:
                    for player in runnerUpPlrs:
                        self.resolveEffects(player, currentCombat.rewards3)
                    #nothing for last
                else:
                    self.resolveEffects(secondPlace, currentCombat.rewards2)
                    if thirdTied:
                        pass #zilch
                    else:
                        self.resolveEffects(lastPlace, currentCombat.rewards3)

        #intrigue - postcombat rewards

        for player in self.players:
            player.deployedTroops = 0
            player.combatPower = 0

    def buyImperiumCard(self, player, card):
        if player.persuasion < card.persuasionCost:
            raise UserWarning("not enough persuasion")
        player.persuasion -= card.persuasionCost
        if card in self.arrakisLiaisons:
            self.arrakisLiaisons.remove(card)
        elif card in self.spiceMustFlow:
            self.spiceMustFlow.remove(card)
        else:
            self.imperiumRow.remove(card)
            self.updateImperiumRow()
        player.discard.append(card)
        self.resolveEffects(player, card.purchaseEffect)
        
    def updateImperiumRow(self):
        if len(self.imperiumRow) < 5:
            if len(self.imperiumOrder) > 0:
                newCardDrawn = self.imperiumOrder.pop()
                self.imperiumRow.append(newCardDrawn)
                return True
            else:
                return False


    def setupRound(self):
        #for boardSpot in self.board.boardSpaces:
         #   boardSpot.isOccupied = False
        for player in self.players: #do that all end of turn
            #player.hasRevealed = False
            #player.agents = player.maxAgents
            drawCard(player, 5)

        self.firstTurnMarker = (self.firstTurnMarker + 1) % self.numplayers
        self.currentTurn += 1


    def cleanupRound(self): #makers, recall, endgame
        for duneSpace in self.board.yellowSpaces:
            if duneSpace.isMaker and not duneSpace.isOccupied:
                duneSpace.currentMaker += 1

        for player in self.players: #can lump with bottom loop for efficiency
            self.highestScore = max(self.highestScore, player.vp)
        if self.highestScore >= 10 or self.currentTurn == 9: #VP reached or out of conflicts
            return self.endgame()
        else:
            for boardSpot in self.board.boardSpaces:
                boardSpot.isOccupied = False
            for player in self.players:
                player.hasRevealed = False
                player.agents = player.maxAgents
            return False


    def endgame(self):
        #play all endgame intrigues
        #ex. Prompt all players to play whichever intrigues they want endgame now

        selSort = [] #selection sort arr
        for player in self.players:
            selSort.append(player)

        def comparePlrTies(player1, player2): #return True if player1 > player2, False if player2 > player1, None if perfectly equal???
            if player1.vp != player2.vp:
               return player1.vp > player2.vp
            else: #vp == vp
                if player1.spice != player2.spice:
                    return player1.spice > player2.spice
                if player1.sols != player2.sols:
                    return player1.sols > player2.sols
                if player1.water != player2.water:
                    return player1.water > player2.water
                if player1.garrisonedTroops != player2.garrisonedTroops:
                    return player1.garrisonedTroops > player2.garrisonedTroops
                #all else fails and somehow tied which should never happen
                return None

        for i in range(1, len(selSort)):
            prevPlrInd = i - 1
            while(prevPlrInd >= 0 and comparePlrTies(selSort[i], selSort[prevPlrInd])):
                tempPlrRef = selSort[prevPlrInd]
                selSort[prevPlrInd] = selSort[i]
                selSort[i] = tempPlrRef
                prevPlrInd -= 1
                i -= 1

        self.winner = selSort[0]
        return True

    def checkRevealStatuses(self):
        revealedMap = {}
        for player in self.players:
            revealedMap[player] = player.hasRevealed
        return revealedMap

    def playThroughTurn(self):
        self.setupRound()
        #player turns\ amd reveal
        currentPlayer = self.firstTurnMarker
        while False in self.checkRevealStatuses().values():
            if self.players[currentPlayer].hasRevealed == False:
                self.superMysteriousRealAIDecision(self.players[currentPlayer])
            #deploy troops needed
            currentPlayer = (currentPlayer + 1) %4
        self.resolveConflict()
        gameStatus = self.cleanupRound()
        if gameStatus:
            print("winner: " + str(self.winner) + " with VP: " + str(self.winner.vp))

    def superMysteriousRealAIDecision(self, player, decisionID=None):
        def decideTurnAndAct():
            randomChance = random.randint(1, 10)
            if randomChance <= 9 and player.agents > 0:
                playAgentTurn()
            else:
                revealTurn()

        def playAgentTurn():
            randomCard = None
            randomSpace = None
            attempts = 0
            while randomSpace == None and attempts < 500:
                randomCard = player.hand[random.randint(0, len(player.hand)-1)]
                boardSpaces = list(self.board.boardSpaceRefs.values())
                selectRandom = random.choice(boardSpaces)
                if selectRandom.isOccupied == False and self.checkBoardspaceCost(player, selectRandom) and selectRandom.access in randomCard.locationAccess :
                    randomSpace = selectRandom
                attempts += 1
            if randomSpace:
                playCard = self.playCard(player, randomCard, randomSpace) 
                deployables = playCard + 2
                numToDeploy = random.randint(0, min(deployables, player.garrisonedTroops))
                if randomSpace.isCombat:
                    self.deployTroops(player, numToDeploy , deployables) #BANDAID solution!! replace with proper prompting at prompting function
                self.vprint(player.tempName + " plays " + randomCard.title + " to " + randomSpace.name + " and deploys " + str(numToDeploy))
            else:
                revealTurn()
        def revealTurn():
            self.vprint(player.tempName + " reveals " + str(player.hand))
            self.reveal(player)
            

        decideTurnAndAct()

    def drawIntrigue(self, player, number):
        for i in range(number):
            intrigueCard = self.intrigueOrder.pop()
            player.intrigueCards.append(intrigueCard)

    def setupPlayers(self):
        isFourPlrGame = self.numplayers == 4
        for i in range(self.numplayers):
            plr = Player(None, 1)
            self.players.append(plr)
            if isFourPlrGame:
                plr.vp = 1
            shuffleDiscard(plr)

    def vprint(self, toPrint):
        #if game is set to verbose print, print
        if self.verbose:
            print(toPrint)

    def getGameState(self, relativePlayer): #Rudimentary implementation - skipping other player info
        playerStatsNonHidden = []
        playerStatsHidden = []
        playerAvailableCardInfo = []
        playerAttributes = vars(relativePlayer)
        hiddenList = ["intrigueCards", "avDeck", "hand"]
        annoyingList = ["inPlay", "discard"]
        for key in playerAttributes:
            if key in hiddenList:
                playerStatsHidden.append(playerAttributes[key])
            elif key in annoyingList:
                playerAvailableCardInfo.append(playerAttributes[key])
            else:
                playerStatsNonHidden.append(playerAttributes[key])

        turnMarker = self.firstTurnMarker
        cTurn = self.currentTurn
        currentConflict = self.conflictOrder[cTurn]
        boardInfo = self.board.boardSpaceRefs

        return playerStatsHidden, playerAvailableCardInfo, playerStatsNonHidden, boardInfo, cTurn, currentConflict, turnMarker
        #still needs info on SMFs, imperium row, arrakis liaisons, mentat


def shuffleDiscard(player):
    if len(player.avDeck) == 0:
            #case 1: game just started, initialize
            if len(player.discard) == 0 and len(player.hand) == 0:
                random.shuffle(cards.allStartingCards)
                startingDeck = copy.deepcopy(cards.allStartingCards)
                player.avDeck = startingDeck
            else:
                #case 2: discard empty because you drew too many
                if len(player.discard) == 0:
                    pass
                else: #case 3: ran out of deck from drawing so shuffle discard
                    random.shuffle(player.discard)
                    player.avDeck = player.discard
                    player.discard = []

def drawCard(player, numToDraw):
    for i in range(numToDraw):
        if len(player.avDeck) == 0:
            shuffleDiscard(player)
        if len(player.avDeck) > 0:
            poppedCard = player.avDeck.pop() #Switch to deque before head hurts
            player.hand.append(poppedCard) #alternate: negative index for last item of list

def setup():
    print("dune: imperium")
    print("insert num people - default 4")
    npinput = input()
    if npinput == "":
        numplayers = 4
    else:
        numplayers = max(int(npinput), 4)

    game = Game(numplayers)
    # do leader selection sometime
    # leaderpack = leaders.init_leaders()
    # add option to choose!
    
    game.setupPlayers()

    game.getGameState(0)
    game.resolveEffects(game.players[0], ["1Intrigue"], 1)
    game.checkBoardspaceCost(game.players[0], game.board.boardSpaceRefs.get("Arrakeen"))
    game.players[0].persuasion = 7
    #game.promptPlayer(game.players[0], "shop")
    #for i in range(9):
     #   game.setupRound()
      #  for j in range(game.numplayers):
       #     game.players[j].combatPower = random.randint(0, 20)
        #    game.players[j].deployedTroops = 1
       # game.resolveConflict()
    for i in range(10):
        game.playThroughTurn()
        if game.winner != None:
            break
    topScore = 0

    scoreDistr = dict()

    for games in range(2000):
        result = simulateGame(numplayers)
        topScore = max(topScore, result)
        scoreDistr[result] = scoreDistr.get(result, 0) + 1
    print("top score: " + str(topScore))
    print("OK!")
    datavis.bplot(scoreDistr.keys(), scoreDistr.values())

def simulateGame(numplrs):
    game = Game(numplrs)
    game.setupPlayers()
    for i in range(10):
        game.playThroughTurn()
        if game.winner != None:
            break
    #print("game simulated")
    return game.winner.vp

def trainingSetup(nmplrs):
    game = Game(nmplrs, True)
    game.setupPlayers()
    return game


#setup()