import mesa
import numpy as np


initial_energy = 10


class model(mesa.Model):
    '''Create a continuous space for the agents to move in'''

    def __init__(self,
                 width=10, height=10,
                 shark_move_cost=2, fish_move_cost=0.2,
                 shark_vision=5, fish_vision=3,
                 shark_eat_radius=0.5,
                 shark_food_energy = 1,
                 shark_initial_energy=10, fish_initial_energy=2,
                 shark_max_speed=1, fish_max_speed=2):

        self.height = width
        self.width = height
        self.shark_move_cost = shark_move_cost
        self.fish_move_cost = fish_move_cost
        self.shark_vision = shark_vision
        self.fish_vision = fish_vision
        self.shark_eat_radius = shark_eat_radius
        self.shark_food_energy = shark_food_energy
        self.fish_initial_energy = fish_initial_energy
        self.shark_initial_energy = shark_initial_energy
        self.shark_max_speed = shark_max_speed
        self.fish_max_speed = fish_max_speed

        self.schedule_Fish = mesa.time.RandomActivation(self)
        self.schedule_Shark = mesa.time.RandomActivation(self)

        self.space = mesa.space.ContinuousSpace(self.width,self.height,True, 0,0)

        self.n_agents = 0
        self.agents = []



    def new_agent(self, agent_type, pos):
        '''This allows us to make agents of a given type'''

        self.n_agents += 1

        #Create a new agent of the given type
        new_agent = agent_type(self.n_agents, self, pos)

        #Place agent in the space 
        self.space.place_agent(new_agent, pos)

        #Add agent to correct scheduler
        getattr(self, f'schedule_{agent_type.__name__}').add(new_agent)

        #Keeping track of the added agents
        self.agents.append(new_agent)


    def remove_agent(self, agent):
        '''Allows for the removal of agents'''
        self.n_agents -= 1


        #Remove agent from space
        self.space.remove_agent(agent)
        self.agents.remove(agent)

        #Remove agent from scheduler
        getattr(self, f'schedule_{type(agent).__name__}').remove(agent)

    def step(self):
        '''The time step function'''

        self.schedule_Fish.step()
        self.schedule_Shark.step()