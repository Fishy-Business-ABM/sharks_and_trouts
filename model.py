from mesa import Model
from mesa.space import ContinuousSpace
from mesa import Agent
import numpy as np


class model(Model):
    '''Create a continuous space for the agents to move in'''

    def __init__(self, width, height):
        self.height = width
        self.width = height

        self.space = ContinuousSpace(self.width,self.height,True, 0,0)

        self.n_agents = 0
        self.agents = []



    def new_agent(self, agent_type,pos):
        '''This allows us to make agents of a given type'''

        self.n_agents += 1

        #Create a new agent of the given type
        new_agent = agent_type(self.n_agents, self, pos)

        #Place agent in the space 
        self.space.place_agent(new_agent, pos)

        #Keeping track of the added agents
        self.agents.append(new_agent)


    def remove_agent(self, agent):
        '''Allows for the removal of agents'''
        self.n_agents -= 1


        #Remove agent from space
        self.space.remove_agent(agent)
        self.agents.remove(agent)

    def step(self):
        '''The time step function'''
        for agent in list(self.agents):
            agent.step()


class TestAgent(Agent):
    def __init__(self, unique_id: int, model: Model, pos) -> None:
        super().__init__(unique_id, model)
        
        self.pos = pos

testmodel = model(10,10)

posistion = (5,5)
testmodel.new_agent(TestAgent,posistion)
testagent = testmodel.agents[0]







