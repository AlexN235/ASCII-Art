#!/usr/bin/python
import numpy as np
from matplotlib import pyplot as plt
import math

def main():
    sd = ShapeDrawer()
    sd.drawHalfSphere(10)
    for i in range(18):
        sd.rotate('x')

    plot3D(sd.getShape())
    print(sd.project())
    
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
        self.rotated_shape = []
        self.times_rotated = 0
        self.center = {
            'x': 0,
            'y': 0,
            'z': 0,
        }
        self._axis = {
            'x': 0,
            'y': 1,
            'z': 2,
        }
        
    def drawCube(self, l, w, h):
        self.shape = np.zeros((int(1.5*l), int(1.5*h), int(1.5*w)))
        self.center = {
            'x': int(1.5*l/2),
            'y': int(1.5*h/2),
            'z': int(1.5*w/2),
        }
        x0 = self.center['x'] - l/2
        x1 = self.center['x'] + l/2
        y0 = self.center['y'] - h/2
        y1 = self.center['y'] + h/2
        z0 = self.center['z'] - w/2
        z1 = self.center['z'] + w/2
        for idx in np.ndindex(np.shape(self.shape)):
            """ check all points to see if it exist on the surface of the cube. """
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
        self.rotated_shape = self.shape
        
    def drawHalfSphere(self, radius):
        grid_size = int(3*radius)
        self.shape = np.zeros((grid_size, grid_size, grid_size))
        self.center = {
            'x': grid_size/2,
            'y': grid_size/2,
            'z': grid_size/2,
        }
        
        for idx in np.ndindex(np.shape(self.shape)):
            ## distance formula d=sqrt((x1-x0)^2 + (y1-y0)^2 + (z1-z0)^2)
            if idx[1] < self.center['z']:
               continue
            
            x2 = (idx[0]-self.center['x'])**2
            y2 = (idx[1]-self.center['y'])**2
            z2 = (idx[2]-self.center['z'])**2
            d = int(math.sqrt(x2 + y2 + z2))
            
            if d == r:
                self.shape[idx[0]][idx[1]][idx[2]] = 1
        self.rotated_shape = self.shape

                     
    def rotate(self, rotation_axis):
        """
        Rotate the shape along an axis. Either 'x', 'y', or 'z'.
        """  
        self.times_rotated = (self.times_rotated + 1) % 8
        size = np.shape(self.rotated_shape)
        new_shape = np.zeros(size)
        
        other_axis = list(self._axis.keys())
        other_axis.remove(rotation_axis)
        t1, t2 = other_axis

        for idx in np.ndindex(size):
            if self.shape[idx[0]][idx[1]][idx[2]] == 0:
                continue
            x = idx[self._axis[t1]] - self.center[t1]
            y = idx[self._axis[t2]] - self.center[t2]
            radian = math.pi/8*self.times_rotated
            new_x = int(x*math.cos(radian) - y*math.sin(radian) + self.center[t1]) 
            new_y = int(x*math.sin(radian) + y*math.cos(radian) + self.center[t2])
            self._applyRotatedPoints(rotation_axis, idx, new_x, new_y, new_shape)
        
        self.rotated_shape = new_shape
        
    def _applyRotatedPoints(self, axis, idx, x, y, temp_model):
        """
        Helper function to have points rotate on desired axis.
        """
        if axis == 'x':
            temp_model[idx[0]][x][y] = self.shape[idx[0]][idx[1]][idx[2]]
        elif axis == 'y':
            temp_model[x][idx[1]][y] = self.shape[idx[0]][idx[1]][idx[2]]
        else: #axis == 'z'
            temp_model[x][y][idx[2]] = self.shape[idx[0]][idx[1]][idx[2]]
            
    def getShape(self):
        return self.rotated_shape
        
    def project(self):
        """
        project 3D model into 2D image Simply flatten on an axis.
        """
        res = np.zeros(np.shape(self.rotated_shape[0]))
        for i, layer in enumerate(self.rotated_shape):
            depth = i / np.shape(self.shape)[0]
            for j, row in enumerate(layer):
                res[j] = list(map(lambda x, y: x if x*depth > 0.05 else y*depth, res[j],row))
        return res
         
if __name__ == "__main__":
    main()