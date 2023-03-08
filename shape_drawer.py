#!/usr/bin/python
import numpy as np
from matplotlib import pyplot as plt

def main():
    shape = np.zeros((10, 10, 10))
    plot3D(shape)
    
def plot3D(shape):
    ## Plots down a shape based on 3d matrix
    ## For testing only

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    x, y, z = shape.nonzero()
    ax.scatter(x, y, z, c=z, alpha=1)
    fig.show()
    
    i = input("press enter")


class ShapeDrawer:
    """
    Draw different shapes: cube, sphere, cylinder etc.
    Rotate shapes
    """
    def __init__(self):
        self.shape = []
        
    def drawCube(self, l, w, h):
        self.shape = np.zeros((1.5*l, 1.5*h, 1.5*w))
        center = {
            x: int(1.5*l/2),
            y: int(1.5*h/2),
            z: int(1.5*w/2),
        }
        
        for idx in np.ndindex(np.shape(self.shape)):
            """ check all points to see fi it exist in the surface """
                    
                

if __name__ == "__main__":
    main()