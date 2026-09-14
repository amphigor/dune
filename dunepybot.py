import dune
from botutils import duneBot
import datavis
import numpy as np

def main():
    agent = duneBot(gamma = 0.99, epsilon = 1.0, batch_size = 64, output_size = 4, input_dims = [8], learnrate = 0.003)
    scores, eps_history = [], []
    n_games = 500

    print(agent.input_dims)

    for i in range(n_games):
        score = 0
        done = False
        environment = dune.trainingSetup(4)
        botPlayer = environment.players[0]
        observation = getGameStateBot(environment, botPlayer)
        while not done:
            action = agent.chooseAction(observation)
            print(action)


            agent.learn()
        scores.append(score)
        eps_history.append(agent.epsilon)

        avg_score = np.mean(scores[-100:])

        #numpy print stuff out
        
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
        maxHandSize = 15 #probably won't exceed in a game
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
            state.append(element)
        else: #currently in event that leader = None
            state.append(0) #give leaders ids too, 0 - 4, 0 being no leader
    hand = handReader(relativePlr.hand)
    state += hand
    print(state)
    state = np.array(state, dtype=int)
    print(state)
    return state

main()
