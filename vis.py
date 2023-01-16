from p5 import *
import numpy as np
import mesa
from fish import  Fish, model
from model import model


width = 1000
height = 1000
model = model(width, height)
boid = Fish(1,model,(1,1),(1,1),25)
boid2= Fish(1,model,(2,2),(1,1),25)


def setup():
    size(width, height)

def draw():
    background(30,30,47)

    boid.show()
    boid2.show()
    boid.step()
    boid2.step()

if __name__ == '__main__':
    run()

