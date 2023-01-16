from mesa import Agent
import random
from copy import copy
import numpy as np
import math

max_move_dist = 1
#hallo

# Define an animal
class Animal(Agent):
    def __init__(self, id, model, pos, energy, move_cost):
        super().__init__(id, model)

        self.pos = pos
        self.energy = energy
        self.move_cost = move_cost
    
    # Move to a random spot within a radius 1 square
    def random_move(self):
        assert self != None

        dist = random.uniform(0,max_move_dist)
        heading = random.uniform(0, 2 * math.pi)

        x_move = dist * math.cos(heading)
        y_move = dist * math.sin(heading)

        new_pos = (self.pos[0] + x_move, self.pos[1] + y_move)

        self.model.space.move_agent(self, new_pos)

        # Reduce energy based on distance moved
        self.energy = self.energy - self.move_cost * dist
    
    # Die if no energy left
    def maybe_die(self):
        assert self != None

        if self.energy < 0:
            self.model.remove_agent(self)

# Define a shark
class Shark(Animal):
    def __init__(self, id, model, pos):
        super().__init__(id, model, pos, model.shark_initial_energy ,model.shark_move_cost)
    
    def step(self):
        assert self != None
        
        # If in sight, move towards closest fish
        fishes = self.model.space.get_neighbors(self.pos, self.model.shark_vision, False)
        for fish in fishes:
            if type(fish) != Fish:
                fishes.remove(fish)
        if len(fishes) > 0:

            # Find closest fish and its distance
            min_dist = self.model.shark_vision
            closest = None
            for fish in fishes:
                dist = self.model.space.get_distance(fish.pos, self.pos)
                if dist < min_dist:
                    min_dist = dist
                    closest = fish
            dist = min_dist

            # Move at most max_move_dist towards closest fish
            x_dist = closest.pos[0] - self.pos[0]
            y_dist = closest.pos[1] - self.pos[1]
            if dist > max_move_dist:
                x_dist = x_dist * (max_move_dist / dist)
                y_dist = y_dist * (max_move_dist / dist)
            new_pos = (self.pos[0] + x_dist, self.pos[1] + y_dist)
            self.model.space.move_agent(self, new_pos)

        # Otherwise, move randomly
        else:
            self.random_move()

        # Maybe die
        self.maybe_die()

        # Eat fish within defined radius
        fishes = self.model.space.get_neighbors(self.pos, self.model.shark_eat_radius, False)
        for fish in fishes:
            if type(fish) == Fish:
                self.model.remove_agent(fish)
                self.energy += self.model.shark_food_energy

# Define a fish
class Fish(Animal):
    def __init__(self, id, model, pos):
        super().__init__(id, model, pos, model.fish_initial_energy, model.fish_move_cost)
    
    def step(self):

        # If in sight, move away from closest shark
        sharks = self.model.space.get_neighbors(self.pos, self.model.fish_vision, False)
        for shark in sharks:
            if type(shark) != Shark:
                sharks.remove(shark)
        if len(sharks) > 0:

            # Find closest shark and its distance
            min_dist = self.model.fish_vision
            closest = None
            for shark in sharks:
                dist = self.model.space.get_distance(shark.pos, self.pos)
                if dist < min_dist:
                    min_dist = dist
                    closest = shark
            dist = min_dist

            # Move away from closest shark at max speed
            x_dir = (closest.pos[0] - self.pos[0]) * (max_move_dist / dist)
            y_dir = (closest.pos[1] - self.pos[1]) * (max_move_dist / dist)
            new_pos = (self.pos[0] - x_dir, self.pos[1] - y_dir)
            self.model.space.move_agent(self, new_pos)

        # Otherwise, move randomly
        else:
            self.random_move()

        # Maybe die
        self.maybe_die()
