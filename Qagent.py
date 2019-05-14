from ple import PLE
import frogger_new
import numpy as np
from pygame.constants import K_w,K_a,K_F15
import random
import pygame, sys
import qTableData

class NaiveAgent():
    def __init__(self, actions):
        self.actions = actions
        self.step = 0
        self.NOOP = K_F15
        self.firstTime = True
        self.sIndexOld = 0
        self.aIndexOld = 0
        self.stateArray = []
        self.qTable = []
        self.learningRate = 0.2
        self.discount = 0.9
        self.epsilon = 0.8
        self.deathCount = 0

    def buildTable(self):
        #only done on the first time through
        self.firstTime = False
        #enumerate states/ store in list
        count = 0
        stateArray = []
        #these will represent states
        # 0 = nothing is there
        # 1 = car is there
        # 2 = log/turtle is there
        # 3 = homeR is there
        for i in range (0,3):
            for j in range(0,4):
                for k in range (0,4):
                    for l in range(0,4):
                        for m in range (0,4):
                            for n in range(0,4):
                                for o in range (0,4):
                                    for p in range(0,4):
                                        for q in range(0,4):
                                        	state = [0]*9
                                        	state[0] = i
                                        	state[1] = j
                                        	state[2] = k
                                        	state[3] = l
                                        	state[4] = m
                                        	state[5] = n
                                        	state[6] = o
                                        	state[7] = p
                                        	state[8] = q
                                        	self.stateArray.append(state)
                                            #print (count)
                                            #print (self.stateArray[count])
                                            #count += 1

        #uncomment the following line to run pretrained frog
        self.qTable = qTableData.qTableData

       
        #uncomment following line to run unlearned frog
        '''
        for s in range(0,len(self.stateArray)+1):
            self.qTable.append([])
            for a in range(0,5):
                self.qTable[s].append(random.random())
        #print (self.qTable)
        '''
        return self.qTable

    def getFrogState(self, obs):

        #state array to return
        currState = [0]*9

        #rect zones in frog's local area
        #NW of frog
        nwZone = pygame.Rect(game.frog.get_pos()[0]-32, game.frog.get_pos()[1]-38, 32, 32)
        #N of frog
        nZone = pygame.Rect(game.frog.get_pos()[0], game.frog.get_pos()[1]-38, 32, 32)
        #NE of frog
        neZone = pygame.Rect(game.frog.get_pos()[0]+32, game.frog.get_pos()[1]-38, 32, 32)
        #E of frog
        eZone = pygame.Rect(game.frog.get_pos()[0]-40, game.frog.get_pos()[1], 40, 32)
        #W of frog
        wZone = pygame.Rect(game.frog.get_pos()[0]+40, game.frog.get_pos()[1], 40, 32)
        #SE fo frog
        seZone = pygame.Rect(game.frog.get_pos()[0]-32, game.frog.get_pos()[1]+38, 32, 32)
        #S of frog
        sZone = pygame.Rect(game.frog.get_pos()[0], game.frog.get_pos()[1]+38, 32, 32)
        #SW of frog
        swZone = pygame.Rect(game.frog.get_pos()[0]+32, game.frog.get_pos()[1]+38, 32, 32)

        #check to see if we are before, in, or after the middle
        if (game.frog.get_pos()[1] > 261):
            #not yet halfway
            currState[0] = 0
        if (game.frog.get_pos()[1] == 261):
            #froggy in the middle
            currState[0] = 1
        if (game.frog.get_pos()[1] < 261):
            #we are in the river
            currState[0] = 2

        #still in first half of game space... look for cars
        if currState[0] == 0:
            for i in range(0, len(obs['cars'])):
                if nwZone.colliderect(obs['cars'][i]):
                    currState[1] = 1
                if nZone.colliderect(obs['cars'][i]):
                    currState[2] = 1
                if neZone.colliderect(obs['cars'][i]):
                    currState[3] = 1
                if wZone.colliderect(obs['cars'][i]):
                    currState[4] = 1
                if eZone.colliderect(obs['cars'][i]):
                    currState[5] = 1
                if swZone.colliderect(obs['cars'][i]):
                    currState[6] = 1
                if sZone.colliderect(obs['cars'][i]):
                    currState[7] = 1
                if seZone.colliderect(obs['cars'][i]):
                    currState[8] = 1

        #we are in the middle... look for logs ahead, cars behind
        if currState[0] == 1:
            for i in range(0, len(obs['rivers'])):
                if nwZone.colliderect(obs['rivers'][i]):
                    currState[1] = 2
                if nZone.colliderect(obs['rivers'][i]):
                    currState[2] = 2
                if neZone.colliderect(obs['rivers'][i]):
                    currState[3] = 2
            for i in range(0, len(obs['cars'])):
                if swZone.colliderect(obs['cars'][i]):
                    currState[6] = 1
                if sZone.colliderect(obs['cars'][i]):
                    currState[7] = 1
                if seZone.colliderect(obs['cars'][i]):
                    currState[8] = 1

        #floating in the river... look for logs and homes
        if currState[0] == 2:
            for i in range(0, len(obs['rivers'])):
                if nwZone.colliderect(obs['rivers'][i]):
                    currState[1] = 2
                if nZone.colliderect(obs['rivers'][i]):
                    currState[2] = 2
                if neZone.colliderect(obs['rivers'][i]):
                    currState[3] = 2
                if wZone.colliderect(obs['rivers'][i]):
                    currState[4] = 2
                if eZone.colliderect(obs['rivers'][i]):
                    currState[5] = 2
                if swZone.colliderect(obs['rivers'][i]):
                    currState[6] = 2
                if sZone.colliderect(obs['rivers'][i]):
                    currState[7] = 2
                if seZone.colliderect(obs['rivers'][i]):
                    currState[8] = 2
            for i in range(0, len(obs['homeR'])):
                if nwZone.colliderect(obs['homeR'][i]):
                    currState[1] = 3
                if nZone.colliderect(obs['homeR'][i]):
                    currState[2] = 3
                if neZone.colliderect(obs['homeR'][i]):
                    currState[3] = 3

        #return state array
        return currState

    def pickAction(self, reward, obs):
        #if first time through, build 2d qTable
        if self.firstTime:
            self.qTable = self.buildTable()

        #get new state
        currState = self.getFrogState(obs)

        #get state index from stateArray given current state
        sIndex = self.stateArray.index(currState)

        #get qTable value of best action for this state based on history 
        optActionVal = max(self.qTable[sIndex])
        #get what that action was
        optActionIndex = self.qTable[sIndex].index(optActionVal)

        #update qTable from previous step
        self.qTable[self.sIndexOld][self.aIndexOld] = self.qTable[self.sIndexOld][self.aIndexOld] + self.learningRate * (reward + self.discount * optActionVal - self.qTable[self.sIndexOld][self.aIndexOld])

        self.aIndexOld = optActionIndex
        self.sIndexOld = sIndex

        #exploration function
        if random.random() > self.epsilon:
        	return self.actions[np.random.randint(0,len(self.actions))]

        #return action
        if optActionIndex == 0:
        	return self.actions[0]
        elif optActionIndex == 1:
        	return self.actions[1]
        elif optActionIndex == 2:
        	return self.actions[2]
        elif optActionIndex == 3:
        	return self.actions[3]
        else:
        	return self.NOOP

        #return self.NOOP
        #Uncomment the following line to get random actions
        #return self.actions[np.random.randint(0,len(self.actions))]

game = frogger_new.Frogger()
fps = 30
p = PLE(game, fps=fps,force_fps=False)
agent = NaiveAgent(p.getActionSet())
reward = 0.0

#p.init()

while True:
    if p.game_over():
    	agent.deathCount += 1
    	if agent.deathCount%250 == 0:
    		agent.epsilon = agent.epsilon + (agent.epsilon/100.00)
    		print (agent.qTable)
    		print ('{} deaths'.format(agent.deathCount))
    		agent.deathCount += 1
    	p.reset_game()
       
    obs = game.getGameState()
    #print (obs)
    action = agent.pickAction(reward, obs)
    reward = p.act(action)
    #print game.score