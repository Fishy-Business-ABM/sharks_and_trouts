import mesa
from p5 import Vector, setup, draw, size, background, run, stroke, circle
import random
from copy import copy
import numpy as np
import math

class model(mesa.Model):
    '''Create a continuous space for the agents to move in'''

    def __init__(self, width=10, height=10):
        self.height = width
        self.width = height

        self.schedule_Fish = mesa.time.RandomActivation(self)

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



class Fish(mesa.Agent):
    def __init__(self, id, model, pos,vel,perception):
        super().__init__(id, model)
        x,y = pos
        v_x,v_y = vel
        self.perception = perception
        self.position = Vector(x,y)
        self.velocity = Vector(v_x,v_y) 
        self.acceleration = Vector(0,0)
        self.model = model
        self.max_speed = 5

    
    def align(self):
        steering = Vector(*np.zeros(2))
        fishes = self.model.space.get_neighbors((self.position.x,self.position.y),self.perception,False)

        for fish in fishes:
            d = Vector.distance(self.position,fish.position)
            if d < self.perception:
                steering += fish.velocity

        if len(fishes)>0:
            steering = steering * (1/len(fishes))
            steering = Vector(*steering)
            steering = Vector.normalize(steering) * self.max_speed 

        
        return steering

    def separation(self):
        steering = Vector(*np.zeros(2))
        fishes = self.model.space.get_neighbors((self.position.x,self.position.y),self.perception,False)

        for fish in fishes:
            d = Vector.distance(self.position, fish.position)
            if d < self.perception:
                sep = self.position - fish.position
                sep = sep * (1/d**2)
                steering += sep

        if len(fishes)>0:
            
            steering = steering* (1/len(fishes))
        
        return steering
    
    def cohesion(self):
        steering = Vector(*np.zeros(2))
        fishes = self.model.space.get_neighbors((self.position.x,self.position.y),self.perception,False)

        for fish in fishes:
            d = np.linalg.norm(self.position - fish.position)
            if d < self.perception:
                steering += fish.position

        if len(fishes)>0:
            steering = steering* (1/len(fishes))
        
        return steering

    def step(self):
        alignment = self.align()
        separation = self.separation()
        cohesion = self.cohesion()


        self.acceleration +=  alignment
        self.acceleration +=  separation
        self.acceleration +=  cohesion
        
        self.position += self.velocity
        self.velocity += self.acceleration
            
    def show(self):
        stroke(255)
        circle((self.position.x,self.position.y), 10)


