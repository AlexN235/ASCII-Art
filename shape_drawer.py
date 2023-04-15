#!/usr/bin/python
import numpy as np
from matplotlib import pyplot as plt
import math
import time
from cube import Cube

def main():
    return

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
    def __init__(self, shape):
        self.pixels = []
        if shape == 'cube':
            self.shape = self._drawCube(20, 20, 20)
        else:   
            self.shape = self._drawCube(20, 20, 20) # default shape
           
    def _drawCube(self, l, w, h):
        return Cube(l, w, h)
    
    def rotate(self, axis):
        """
        rotates the shape.
        """
        self.pixels = []
        self.shape.rotate(axis)
        
    def getShape(self):
        """ 
        returns the represented shape on the 3D plane.
        """
        return self.pixels
        
    def project(self):
        """
        project 3D model into 2D image by simply flatten on an plane.
        """
        grid_size = self.shape.getGridSize()
        self.translateToDisplay()
        self._createShapePoints()
        res = np.zeros(np.array(grid_size[0:2]))
        for pixel in self.pixels:
            grey_value = int(self._toHexScale((grid_size[2] - pixel[2])/grid_size[2]))
            if res[int(pixel[0])][int(pixel[1])] < grey_value:
                res[int(pixel[0])][int(pixel[1])] = grey_value
        return res
        
    def translateToDisplay(self):
        self.shape.translateToDisplay()
        
    def _createShapePoints(self):
        """
        Generates all points from the key points of the shape.
        """
        if self.shape.getShapeName() == 'cube':
            self._cornersToSquares()
        
    def _toHexScale(self, value: int):
        if value > 1 or value < 0:
            return 0 # error
        return value*255
  
    def _cornersToSquares(self):
        """
        Takes the corner coordinates of a square and draws the squares polygons for the cube.
        """
        c = self.shape.getKeyPoints()
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
        """ input: p1 to p2 is a line parallel to the line p3 to p4. """ 
        l1 = np.unique(np.linspace(p1, p2, dtype=int), axis=0)

        full = np.unique(np.linspace(l1, p3, dtype=int), axis=0)
        full = full.reshape((full.shape[0]*full.shape[1],4))

        self.pixels.extend(list(full))
   
    def _drawPoint(self, x, y, z, a):
        print('drawPoint incomplete')
    
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