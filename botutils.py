import torch
from torch import nn
from torch import optim
from torch.nn import functional as F

import numpy as np

device = torch.accelerator.current_accelerator() if torch.accelerator.is_available() else "cpu"

class dnetwork(nn.Module):
    def __init__(self, input_dims, l1_dims, l2_dims, outpt_dims, learnrate):
        super().__init__()
        self.input_dims = input_dims
        self.l1_dims = l1_dims
        self.l2_dims = l2_dims
        self.outpt_dims = outpt_dims

        self.l1 = nn.Linear(*input_dims, l1_dims)
        self.l2 = nn.Linear(l1_dims, l2_dims)
        self.l3b = nn.Linear(l2_dims, outpt_dims) #for rollback just remove this and replace with l3 only
        self.l3c = nn.Linear(l2_dims, outpt_dims)
        self.l3d = nn.Linear(l2_dims, outpt_dims)

        self.optimizer = optim.Adam(self.parameters(), lr = learnrate)
        self.loss = nn.MSELoss()
        self.device = device
        self.to(device)

    def forward(self, state):
        x = F.relu(self.l1(state))
        x = F.relu(self.l2(x))
        #actions = self.l3(x)
        boardspace = self.l3b(x)
        card = self.l3c(x)
        numofguystodrop = self.l3d(x)
        #return as tuple below
        return boardspace, card, numofguystodrop
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

        self.action_space = [i for i in range(output_size)]

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
        if np.random.random() < self.epsilon: #should be >
            state = torch.tensor([observation]).to(self.network.device)
            actions = self.network.forward(state)
            action = torch.argmax(actions).item() #optimal
        else:
            action = np.random.choice(self.action_space)

        return action

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





        def updateActionSpace(player):
            pass


