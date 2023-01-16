import agent
import model
from random import uniform
import matplotlib.pyplot as plt

dimension = 20

tester = model.model(dimension, dimension)
tester.fish_move_cost = 0

for _ in range(3):
    pos = (uniform(0, dimension), uniform(0, dimension))
    tester.new_agent(agent.Shark, pos)
sharks = tester.agents

for _ in range(20):
    pos = (uniform(0, dimension), uniform(0, dimension))
    tester.new_agent(agent.Fish, pos)

paths_x = []
paths_y = []
indices = []
index = 0
for shark in sharks:
    shark.index = index
    index += 1
    paths_x.append([])
    paths_y.append([])

for _ in range(50):
    tester.step()

    for a in tester.agents:
        x = a.pos[0]
        y = a.pos[1]
        if type(a) == agent.Fish:
            plt.plot([x], [y], 'bo', ms=a.energy)
        else:
            paths_x[a.index].append(x)
            paths_y[a.index].append(y)
            plt.plot([x],[y],'ro', ms=a.energy)

        for shark in sharks:
            plt.plot(paths_x[shark.index], paths_y[shark.index],'r-')

    plt.xlim(0, tester.height)
    plt.ylim(0, tester.width)
    plt.draw()
    plt.pause(0.1)
    plt.close()