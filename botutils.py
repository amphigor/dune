import torch
from torch import nn
from torch import optim
from torch.nn import functional as F

import numpy as np

device = torch.accelerator.current_accelerator() if torch.accelerator.is_available() else "cpu"
NUM_BOARD_SPACES = 22
MAX_HAND_SIZE = 21
MAX_DEPLOYABLE = 12

class dnetwork(nn.Module):
    def __init__(self, input_dims, l1_dims, l2_dims, outpt_dims, learnrate):
        super().__init__()
        self.input_dims = input_dims
        self.l1_dims = l1_dims
        self.l2_dims = l2_dims
        self.outpt_dims = outpt_dims

        self.l1 = nn.Linear(*input_dims, l1_dims)
        self.l2 = nn.Linear(l1_dims, l2_dims)
        #self.l3b = nn.Linear(l2_dims, outpt_dims) #for rollback just remove this and replace with l3 only
        self.l3b = nn.Linear(l2_dims, NUM_BOARD_SPACES) # 22 board spaces
        self.l3c = nn.Linear(l2_dims, MAX_HAND_SIZE) # 16 is cleaner, but practical max is 21 cards in hand
        self.l3d = nn.Linear(l2_dims, MAX_DEPLOYABLE) # hard cap of 12 deployable troops

        self.optimizer = optim.Adam(self.parameters(), lr = learnrate)
        self.loss = nn.MSELoss()
        self.device = device
        self.to(device)

    def forward(self, state):
        print(state.dtype)
        x = F.relu(self.l1(state))
        x = F.relu(self.l2(x))
        #actions = self.l3(x)
        boardspace = self.l3b(x)
        card = self.l3c(x)
        numofguystodrop = self.l3d(x)
        #return as tuple below
        return boardspace, card, numofguystodrop #potential: reveal/no reveal, card to buy, optional effects, intrigue, debug info
        #will need to calculate loss for second too, see discuss.pytorch.org/t/a-model-with-multiple-outputs/10440

class duneBot(): #rewards, exploration rate, 
    def __init__(self, gamma, epsilon, learnrate, input_dims, batch_size, output_size,
                 max_mem = 100000, eps_end = 0.01, eps_dec = 5e-4):
        self.gamma = gamma
        self.epsilon = epsilon
        self.learnrate = learnrate
        self.input_dims = input_dims
        self.batch_size = batch_size
        self.max_mem = max_mem
        self.eps_end = eps_end
        self.eps_dec = eps_dec
        self.mem_cntr = 0

        self.network = dnetwork(input_dims, 256, 256, output_size, learnrate)

        self.card_action_space = [i for i in range(MAX_HAND_SIZE)]#[i for i in range(output_size)]
        self.board_aspace = [i for i in range(NUM_BOARD_SPACES)]
        self.deploy_aspace = [i for i in range(MAX_DEPLOYABLE)]

        self.state_mem = np.zeros((self.max_mem, *input_dims), np.float32)
        self.new_state_mem = np.zeros((self.max_mem, *input_dims), np.float32)

        self.action_mem = np.zeros(self.max_mem, dtype=np.int32)
        self.reward_mem = np.zeros(self.max_mem, dtype=np.float32)
        self.term_mem = np.zeros(self.max_mem, dtype=np.bool)

    def storeTransition(self, state, action, reward, next_state, done):
        index = self.mem_cntr % self.max_mem
        self.state_mem[index] = state
        self.new_state_mem[index] = next_state
        self.reward_mem[index] = reward
        self.action_mem[index] = action
        self.term_mem[index] = done

        self.mem_cntr += 1

    def chooseAction(self, observation):
        if np.random.random() > self.epsilon:
            state = torch.tensor([observation]).to(self.network.device) #Potential failure point - print dtype
            boardspace, card, numDeploy = self.network.forward(state)
            boardspace = torch.argmax(boardspace).item() #optimal choices?
            card = torch.argmax(card).item()
            numDeploy = torch.argmax(numDeploy).item()
        else:
            boardspace = np.random.choice(self.board_aspace)
            card = np.random.choice(self.card_action_space) 
            numDeploy = np.random.choice(self.deploy_aspace)
        return boardspace, card, numDeploy

    def learn(self):
        if self.mem_cntr < self.batch_size: #if not enough mems to learn
            return #alternative: fill up mem with random choices

        self.network.optimizer.zero_grad()
        last_mem = min(self.mem_cntr, self.max_mem)
        batch = np.random.choice(last_mem, self.batch_size, replace=False)
        batch_index = np.arange(self.batch_size, dtype=np.int32)

        state_batch = torch.tensor(self.state_mem[batch]).to(self.network.device)
        new_state_batch = torch.tensor(self.new_state_mem[batch]).to(self.network.device)
        reward_batch = torch.tensor(self.reward_mem[batch]).to(self.network.device)
        terminal_batch = torch.tensor(self.term_mem[batch]).to(self.network.device)

        action_batch = self.action_mem[batch]

        q_eval = self.network.forward(state_batch)[batch_index, action_batch]
        q_next = self.network.forward(new_state_batch) #target network goes here
        q_next[terminal_batch] = 0.0

        q_target = reward_batch + self.gamma * torch.max(q_next, dim = 1)[0]

        loss = self.network.loss(q_target, q_eval).to(self.network.device)
        loss.backward()
        self.network.optimizer.step()

        self.epsilon = self.epsilon - self.eps_dec if self.epsilon > self.eps_end else self.eps_end





    #def updateActionSpace(player):
     #   pass
    #Only would need if we wanted to filter out used spaces before feeding into model
    #however then we'd never know about possible infiltrate moves

