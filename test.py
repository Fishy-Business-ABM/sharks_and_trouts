import agent
import model
import random
import matplotlib.pyplot as plt
import numpy as np

tester = model.model()

shark_pos = (5,5)
tester.new_agent(agent.Shark, shark_pos)
shark = tester.agents[0]

for _ in range(10):
    pos = (random.uniform(0,10), random.uniform(0,10))
    tester.new_agent(agent.Fish, pos)

for _ in range(10):
    tester.step()

'''
for agent in tester.agents:
    print(type(agent))
    print(agent.pos)
    print(agent.energy)
'''