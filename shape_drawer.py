#!/usr/bin/python
import numpy as np
from matplotlib import pyplot as plt
import math
import time
from cube import Cube
from donut import Donut

class ShapeDrawer:
    """
    Draw different shapes: cube, sphere, cylinder etc. Represents these
    shapes in a 3D numpy matrix. Rotate shapes on different axis.
    """
    def __init__(self, shape):
        self.pixels = []
        if shape == 'cube':
            self.shape = self._drawCube(20, 20, 20)
        elif shape == 'donut':
            self.shape = self._drawDonut(10)
        else:   
            self.shape = self._drawCube(20, 20, 20) # default shape
           
    def _drawCube(self, l, w, h):
        return Cube(l, w, h)
        
    def _drawDonut(self, r):
        return Donut(r)
    
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
        
        self._translateToDisplay()
        self._createShapePoints()
        image2D = np.zeros(np.array(grid_size[0:2]))
        for pixel in self.pixels:
            grey_value = int(self._toHexScale((grid_size[2] - pixel[2])/grid_size[2]))
            x, y = int(pixel[0]), int(pixel[1])
            if image2D[x][y] < grey_value:
                image2D[x][y] = grey_value
        return image2D

    ### In class functions ###
    def _translateToDisplay(self):
        self.shape.translateToDisplay()
        
    def _createShapePoints(self):
        """
        Generates all points from the key points of the shape.
        """
        self._cornersToSquares()
        
    def _toHexScale(self, value: int):
        if value > 1 or value < 0:
            return 0 # error
        return value*255
  
    def _cornersToSquares(self):
        points = self.shape.generateShape()   
        self._drawShape(points)
        
    def _drawShape(self, polygons):
        for point in polygons:
            a, b, c = point
            self._fillInPolygon(a, b, c)

    def _fillInPolygon(self, p1, p2, p3):
        """ input: p1 to p2 is a line parallel to the line p3 to p4. """ 
        l1 = np.unique(np.linspace(p1, p2, dtype=int), axis=0)
        full = np.unique(np.linspace(l1, p3, dtype=int), axis=0)
        full = full.reshape((full.shape[0]*full.shape[1],4))
        
        self.pixels.extend(list(full))
