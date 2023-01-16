from mesa import Agent
from random import uniform
from math import pi
from math import sin
from math import cos

# Define an animal (only used in Fish!!)
class Animal(Agent):
    def __init__(self, id, model, pos, energy, move_cost, max_speed):
        super().__init__(id, model)

        self.pos = pos
        self.energy = energy
        self.move_cost = move_cost
        self.max_speed = max_speed
    
    # Move in a random direction at random speed
    def random_move(self):
        assert self in self.model.agents

        dist = uniform(0, self.max_speed)
        heading = uniform(0, 2 * pi)

        x_move = dist * cos(heading)
        y_move = dist * sin(heading)

        new_pos = (self.pos[0] + x_move, self.pos[1] + y_move)

        self.model.space.move_agent(self, new_pos)

        # Reduce energy based on distance moved
        self.energy = self.energy - self.move_cost * dist
    
    # Die if no energy left
    def maybe_die(self):
        assert self in self.model.agents

        if self.energy < 0:
            self.model.remove_agent(self)

# Define a fish
class Fish(Animal):
    def __init__(self, id, model, pos):
        super().__init__(id, model, pos, model.fish_initial_energy, model.fish_move_cost, model.shark_max_speed)
    
    def step(self):
        assert self in self.model.agents

        # If in sight, move away from closest shark
        neighbors = self.model.space.get_neighbors(self.pos, self.model.fish_vision, True)
        sharks = []
        for neighbor in neighbors:
            if type(neighbor) == Shark:
                sharks.append(neighbor)
        for shark in sharks:
            assert type(shark) == Shark
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
            if dist != 0:
                x_dir = (closest.pos[0] - self.pos[0]) * (self.max_speed / dist)
                y_dir = (closest.pos[1] - self.pos[1]) * (self.max_speed / dist)
            else:
                x_dir = self.max_speed
                y_dir = 0
            new_pos = (self.pos[0] - x_dir, self.pos[1] - y_dir)
            self.model.space.move_agent(self, new_pos)

        # Otherwise, move randomly
        else:
            self.random_move()

        # Maybe die
        self.maybe_die()

# Define a shark
class Shark(Agent):
    def __init__(self, id, model, pos):
        super().__init__(id, model)

        self.pos = pos
        self.energy = model.shark_initial_energy

    # Die if no energy left
    def maybe_die(self):
        assert self in self.model.agents

        if self.energy < 0:
            self.model.remove_agent(self)

    # Move in a random direction with random speed
    def random_move(self):
        assert self in self.model.agents

        dist = uniform(0, self.model.shark_max_speed)
        heading = uniform(0, 2 * pi)

        x_move = dist * cos(heading)
        y_move = dist * sin(heading)

        new_pos = (self.pos[0] + x_move, self.pos[1] + y_move)

        self.model.space.move_agent(self, new_pos)

        # Reduce energy based on distance moved
        self.energy = self.energy - self.model.shark_move_cost * dist
    
    # Find closest fish within vision
    def closest_fish(self, vision):
        assert self in self.model.agents

        # Get fish within vision
        neighbors = self.model.space.get_neighbors(self.pos, vision, True)
        fishes = []
        for neighbor in neighbors:
            if type(neighbor) == Fish:
                fishes.append(neighbor)
        for fish in fishes:
            assert type(fish) == Fish
        
        # If no fish in sight, return None
        if len(fishes) == 0:
            return None
        
        # Else, return closest fish
        else:
            min_dist = vision
            closest = None
            for fish in fishes:
                dist = self.model.space.get_distance(fish.pos, self.pos)
                if dist < min_dist:
                    min_dist = dist
                    closest = fish
            return closest

    # Move towards a point with bounded speed
    def move_towards(self, pos, max_speed):
        assert self in self.model.agents

        # Calculate direction
        x_dist = pos[0] - self.pos[0]
        y_dist = pos[1] - self.pos[1]
        dist = (x_dist ** 2 + y_dist ** 2) ** 0.5

        # Bound by max_speed
        if dist > max_speed and dist != 0:
            x_dist = x_dist * (max_speed / dist)
            y_dist = y_dist * (max_speed / dist)
        
        # Move
        new_pos = (self.pos[0] + x_dist, self.pos[1] + y_dist)
        self.model.space.move_agent(self, new_pos)

    # Eat fish within given radius
    def eat(self, radius):
        assert self in self.model.agents

        neighbors = self.model.space.get_neighbors(self.pos, radius, True)
        fishes = []
        for neighbor in neighbors:
            if type(neighbor) == Fish:
                fishes.append(neighbor)
        for fish in fishes:
            assert type(fish) == Fish
            self.model.remove_agent(fish)
            self.energy += self.model.shark_food_energy
    
    # Define shark behaviour
    def step(self):
        assert self in self.model.agents
        
        # If no fish in sight, move randomly
        food = self.closest_fish(self.model.shark_vision)
       
        if food == None:
            self.random_move()
        
        # Else, move towards closest fish
        else:
            self.move_towards(food.pos, self.model.shark_max_speed)
        
        # Eat all available fish
        self.eat(self.model.shark_eat_radius)

        # Maybe die
        self.maybe_die()