#!/usr/bin/python
import numpy as np
from matplotlib import pyplot as plt
import math

def main():
    sd = ShapeDrawer()
    sd.drawHalfSphere(10)
    
    plot3D(sd.shape)
    
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
        self.shape = np.zeros((int(1.5*l), int(1.5*h), int(1.5*w)))
        center = {
            'x': int(1.5*l/2),
            'y': int(1.5*h/2),
            'z': int(1.5*w/2),
        }
        for idx in np.ndindex(np.shape(self.shape)):
            """ check all points to see if it exist on the surface """
            x0 = center['x'] - l/2
            x1 = center['x'] + l/2
            y0 = center['y'] - h/2
            y1 = center['y'] + h/2
            z0 = center['z'] - w/2
            z1 = center['z'] + w/2
            x_condition = idx[0] >= x0 and idx[0] <= x1
            y_condition = idx[1] >= y0 and idx[1] <= y1
            z_condition = idx[2] >= z0 and idx[2] <= z1
            if idx[0] == x1 or idx[0] == x0:
                ## check if y, z are in range
                if y_condition and z_condition:
                    self.shape[idx[0]][idx[1]][idx[2]] = 1
            elif idx[1] == y1 or idx[1]  == y0:
                if x_condition and z_condition:
                ## check if x, z are in range
                    self.shape[idx[0]][idx[1]][idx[2]] = 1
            elif idx[2] == z1 or idx[2] == z0:
                ## check if x, y are in range
                if x_condition and y_condition:
                    self.shape[idx[0]][idx[1]][idx[2]] = 1
        
    def drawHalfSphere(self, r):
        grid_size = int(3*r)
        self.shape = np.zeros((grid_size, grid_size, grid_size))
        center = {
            'x': grid_size/2,
            'y': grid_size/2,
            'z': grid_size/2,
        }
        
        for idx in np.ndindex(np.shape(self.shape)):
            ## distance formula d=sqrt((x1-x0)^2 + (y1-y0)^2 + (z1-z0)^2)
            if idx[2] < center['y']:
               continue
            
            x2 = (idx[0]-center['x'])**2
            y2 = (idx[1]-center['y'])**2
            z2 = (idx[2]-center['z'])**2
            d = int(math.sqrt(x2 + y2 + z2))
            
            if d == r:
                self.shape[idx[0]][idx[1]][idx[2]] = 1

                    
    def __rotate(self, axis):
    """
    TO DO: 
        - rotate on a choosen axis rather than just z axis
        - make it less error prone
    """
        size = np.shape(self.shape)
        new_shape = np.zeros(size)
        center = {
            'x': size[0]/2,
            'y': size[1]/2,
            'z': size[2]/2,
        }
        for idx in np.ndindex(np.shape(self.shape)):
            x = idx[0] - center['x']
            y = idx[1] - center['y']
            new_x = x*math.cos(math.pi/4) - y*math.sin(math.pi/4) + center['x']
            new_y = x*math.sin(math.pi/4) + y*math.cos(math.pi/4) + center['y']
            new_shape[new_x][new_y][idx[2]] = self.shape[idx[0]][idx[1]][idx[2]]
        
        self.shape = new_shape
        
if __name__ == "__main__":
    main()