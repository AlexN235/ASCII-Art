#!/usr/bin/python
import numpy as np
import math
from shape import Shape

class Cube(Shape):
    """
    Class representing the Cube shape.
    """
    def __init__(self, l ,w, h):
        super().__init__()
        self.drawCube(l, w, h)
        self.shape = 'cube'
        
    def drawCube(self, l, w, h):
        self.grid_size = [int(l*self.SHAPE_TO_GRID_MULTIPLIER),
                          int(w*self.SHAPE_TO_GRID_MULTIPLIER),
                          int(h*self.SHAPE_TO_GRID_MULTIPLIER)]
        self.transformed_points = []
        # One side of the cube
        self.key_points.append(np.array((l/2, -w/2, h/2, 1)))   # A
        self.key_points.append(np.array((l/2, w/2, h/2, 1)))    # B
        self.key_points.append(np.array((l/2, -w/2, -h/2, 1)))  # C
        self.key_points.append(np.array((l/2, w/2, -h/2, 1)))   # D
        # Other side of the cube
        self.key_points.append(np.array((-l/2, -w/2, h/2, 1)))  # E
        self.key_points.append(np.array((-l/2, w/2, h/2, 1)))   # F
        self.key_points.append(np.array((-l/2, -w/2, -h/2, 1))) # G
        self.key_points.append(np.array((-l/2, w/2, -h/2, 1)))  # H
        self.transformed_points = self.key_points
        
    def generateShape(self):
        """
        Takes the corner coordinates of a square and draws the squares polygons for the cube.
        """
        c = self.getKeyPoints()
        polygon_points = []
        polygon_points.extend(self._squaresToPolygons(c[0], c[1], c[4], c[5]))
        polygon_points.extend(self._squaresToPolygons(c[0], c[1], c[2], c[3]))
        polygon_points.extend(self._squaresToPolygons(c[2], c[0], c[6], c[4]))
        polygon_points.extend(self._squaresToPolygons(c[6], c[7], c[4], c[5]))
        polygon_points.extend(self._squaresToPolygons(c[6], c[7], c[2], c[3]))
        polygon_points.extend(self._squaresToPolygons(c[7], c[5], c[3], c[1]))
        return polygon_points
        
    def _squaresToPolygons(self, p1, p2, p3, p4):
        points = []
        points.append(np.array([p1, p2, p3]))
        points.append(np.array([p3, p4, p2]))
        return points