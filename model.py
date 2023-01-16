from mesa import Model
from mesa.space import ContinuousSpace
import numpy as np


initial_energy = 10


class model(Model):
    '''Create a continuous space for the agents to move in'''

    def __init__(self, width, height):
        self.height = width
        self.width = height
        self.shark_move_cost = 0.1
        self.fish_move_cost = 0.1
        self.shark_vision = 2
        self.fish_vision = 1
        self.shark_eat_radius = 0.5
        self.shark_food_energy = 0.1
        self.fish_initial_energy = 2
        self.shark_initial_energy = 10

        self.space = ContinuousSpace(self.width,self.height,True, 0,0)

        self.n_agents = 0
        self.agents = []



    def new_agent(self, agent_type, pos):
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