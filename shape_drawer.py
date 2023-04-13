#!/usr/bin/python
import numpy as np
from matplotlib import pyplot as plt
import math
import time
from cube import Cube

def main():
    sd = ShapeDrawer('cube')
    sd.rotate(['x'])
    print(sd.shape.getShape())

def plot3D(shape):
    ## Plots down a shape based on 3d matrix
    ## For testing only

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x, y, z ,a = shape.transpose()
    ax.scatter(x, y, z, c=z, alpha=1)
    fig.show()
    
    i = input("press enter")

class ShapeDrawer:
    """
    Draw different shapes: cube, sphere, cylinder etc. Represents these
    shapes in a 3D numpy matrix. Rotate shapes on different axis.
    """
    NUMBER_OF_ROTATIONS = 32
    RADIANS = 2*math.pi/NUMBER_OF_ROTATIONS 
    SHAPE_TO_GRID_MULTIPLIER = 1.7
    
    def __init__(self, shape):
        self.rotated_shape = []
        if shape == 'cube':
            self.shape = self.drawCube(20, 20, 20)
        else:   
            self.shape = self.drawCube(20, 20, 20) # default shape
           
    def drawCube(self, l, w, h):
        return Cube(l, w, h)
    
    def rotate(self, axis):
        self.rotated_shape = []
        self.shape.rotate(axis)
        
    def _cornersToSquares(self):
        c = self.shape.getShape()
        self._squaresToPolygons(c[0], c[1], c[4], c[5])
        self._squaresToPolygons(c[0], c[1], c[2], c[3])
        self._squaresToPolygons(c[2], c[0], c[6], c[4])
        self._squaresToPolygons(c[6], c[7], c[4], c[5])
        self._squaresToPolygons(c[6], c[7], c[2], c[3])
        self._squaresToPolygons(c[7], c[5], c[3], c[1])
        
    def _squaresToPolygons(self, p1, p2, p3, p4):
        self._fillInPolygon(p1, p2, p3)
        self._fillInPolygon(p3, p4, p2)
        
    def _fillInPolygon(self, p1, p2, p3):
        """ input: p1 and p2 are one line and p3 p4 is a parallel line """ 
        l1 = np.unique(np.linspace(p1, p2, dtype=int), axis=0)

        full = np.unique(np.linspace(l1, p3, dtype=int), axis=0)
        full = full.reshape((full.shape[0]*full.shape[1],4))

        self.rotated_shape.extend(list(full))
   
    def _drawPoint(self, x, y, z, a):
        print('drawPoint incomplete')
    
    def getShape(self):
        """ 
        returns the represented shape on the 3D plane.
        """
        return self.rotated_shape
        
    def project(self):
        """
        project 3D model into 2D image by simply flatten on an plane.
        """
        grid_size = self.shape.getGridSize()
        self._cornersToSquares()
        self._translation(grid_size[0]/6, grid_size[1]/6, grid_size[2]/6)
        res = np.zeros(np.array(grid_size[0:2]))
        for pixel in self.rotated_shape:
            grey_value = int(self._toHexScale((grid_size[2] - pixel[2])/grid_size[2]))
            if res[int(pixel[0])][int(pixel[1])] < grey_value:
                res[int(pixel[0])][int(pixel[1])] = grey_value
        return res
        
    def _translation(self, x, y, z):
        translation_array = np.array([[1, 0, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 0, 1, 0],
                                      [x, y, z, 1],
                                      ])
        self.rotated_shape = list(np.dot(self.rotated_shape, translation_array))
        
    def _toHexScale(self, value: int):
        if value > 1 or value < 0:
            return 0 # error
        return value*255
        
        
    def _findPlane(self, p1, p2, p3):
        v1 = p3-p1
        v2 = p2-p1
        
        cp = np.cross(v1, v2)
        
        d = np.dot(cp, p1)
        return cp, d #(cp = A, B, C)
        
    def _findPointInPlane(self, p1, p2, p3):
        in_plane = []
        cp, d = self._findPlane(p1, p2 ,p3)
        for point in self.shape:    
            if((point.dot(p3) + d) == 0):
                in_plane.append(point)
        return in_plane

         
if __name__ == "__main__":
    main()