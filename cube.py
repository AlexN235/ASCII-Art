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
        m = self.SHAPE_TO_GRID_MULTIPLIER
        self.getGridSize = [int(l*m), int(w*m), int(h*m)]
        # One side of the cube
        self.mesh_points.append(np.array((l/2, -w/2, h/2, 1)))   # A
        self.mesh_points.append(np.array((l/2, w/2, h/2, 1)))    # B
        self.mesh_points.append(np.array((l/2, -w/2, -h/2, 1)))  # C
        self.mesh_points.append(np.array((l/2, w/2, -h/2, 1)))   # D
        # Other side of the cube
        self.mesh_points.append(np.array((-l/2, -w/2, h/2, 1)))  # E
        self.mesh_points.append(np.array((-l/2, w/2, h/2, 1)))   # F
        self.mesh_points.append(np.array((-l/2, -w/2, -h/2, 1))) # G
        self.mesh_points.append(np.array((-l/2, w/2, -h/2, 1)))  # H
        
    def generateShape(self):
        """
        Takes the corner coordinates of a square and draws the squares polygons for the cube.
        """
        c = self.getTransformedMesh()
        
        polygon_points = []
        polygon_points.extend(self._squaresToPolygons(c[0], c[1], c[4], c[5]))
        polygon_points.extend(self._squaresToPolygons(c[0], c[1], c[2], c[3]))
        polygon_points.extend(self._squaresToPolygons(c[2], c[0], c[6], c[4]))
        polygon_points.extend(self._squaresToPolygons(c[6], c[7], c[4], c[5]))
        polygon_points.extend(self._squaresToPolygons(c[6], c[7], c[2], c[3]))
        polygon_points.extend(self._squaresToPolygons(c[7], c[5], c[3], c[1]))
        return polygon_points
