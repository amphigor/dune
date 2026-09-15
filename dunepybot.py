import dune
from botutils import duneBot
import datavis
import numpy as np

from botutils import MAX_HAND_SIZE

def main(): #input_dims originally 
    agent = duneBot(gamma = 0.99, epsilon = 1.0, batch_size = 64, output_size = 4, input_dims = [65], learnrate = 0.003)
    scores, eps_history = [], []
    n_games = 500 

    print(agent.input_dims)

    for i in range(n_games):
        score = 0
        done = False
        environment = dune.trainingSetup(4)
        botPlayer = environment.players[0]
        #observation = getGameStateBot(environment, botPlayer)
        while not done: #while game not over, play turns
            environment.setupRound()
            while False in environment.checkRevealStatuses().values():
                playUntilBotTurn(environment, botPlayer)

                successfullyPlayed = False
                while not successfullyPlayed:
                    observation = getGameStateBot(environment, botPlayer)
                    boardspace, card, numDeploy = agent.chooseAction(observation)
                    print(boardspace, card, numDeploy)
                    reward = 0
                    try:
                        environment.playBotMoveWrapper(botPlayer, boardspace, card, numDeploy)
                        successfullyPlayed = True
                        reward += 4
                    except:
                        reward -= 1
                    finally:
                        newObservation = getGameStateBot(environment, botPlayer)
                        score += reward
                        agent.storeTransition(observation, action, reward, newObservation, False) #should be actions for 2nd prm
                        agent.learn()

                #agent.learn() #Which one?
            environment.resolveConflict()
            gameStatus = environment.cleanupRound()
            if gameStatus:
                done = True
            #agent.learn()
        scores.append(score)
        eps_history.append(agent.epsilon)

        avg_score = np.mean(scores[-100:])
        print("game" + i + " avg score " + avg_score + " eps " + agent.epsilon)
    #done
    datavis.lplot(n_games, scores)
        
def playUntilBotTurn(game, bot):
    while game.players[game.currentPlayerTurn] != bot:
        if game.players[game.currentPlayerTurn].hasRevealed == False:
            game.superMysteriousRealAIDecision(game.players[game.currentPlayerTurn])
            game.currentPlayerTurn = (game.currentPlayerTurn + 1) % game.numplayers

def getGameStateBot(game, relativePlr):
    def boardStateReader(board):
        boardRep = []
        for boardspace in board.keys():
            if board[boardspace].isOccupied:
                boardRep.append(1)
            else:
                boardRep.append(0)
        return boardRep

    def handReader(hand):
        maxHandSize = MAX_HAND_SIZE #probably won't exceed in a game
        handRep = []
        for card in hand:
            id = card.id
            handRep.append(id)
        while len(handRep) < maxHandSize:
            handRep.append(-1)
        return handRep

    hd, avl, nonhd, board, ct, conflict, turnmark = game.getGameState(relativePlr)
    #conflictHash = sum(hash(item) for item in conflict.rewards1+conflict.rewards2+conflict.rewards3) % 1027
    #for item in conflict.rewards1: print(item)
    state = [turnmark, conflict.id, ct] + boardStateReader(board)
    for element in nonhd:
        if element:
            state.append(int(element))
        else: #currently in event that leader = None
            state.append(0) #give leaders ids too, 0 - 4, 0 being no leader
    hand = handReader(relativePlr.hand)
    state += hand
    print(state)
    state = np.array(state, dtype=float)
    print(state)
    print(len(state))
    return state

main()
