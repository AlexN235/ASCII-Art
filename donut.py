#!/usr/bin/python
import numpy as np
import math
from shape import Shape

class Donut(Shape):
    """
    Class representing the Donut shape.
    """
    NUMBER_OF_POINTS_IN_A_CIRCLE = 12
    def __init__(self, radius):
        super().__init__()
        self.mesh_array_shape = None
        self.drawDonut(radius)
        self.shape = 'donut'
          
    def drawDonut(self, r):
        m = int(2*r*self.SHAPE_TO_GRID_MULTIPLIER)
        self.setGridSize(m, m, m)
        self.mesh_points = list(self._generateMesh(r))

    def generateShape(self):
        """
        Takes the corner coordinates of a square and draws the squares polygons for the cube.
        """
        c = np.array(self.getTransformedMesh()).reshape(self.getMeshArrayShape())
        polygons = []
        for i in range(self.NUMBER_OF_POINTS_IN_A_CIRCLE):
            next_i = self._getNextIndex(i, self.NUMBER_OF_POINTS_IN_A_CIRCLE)
            for j in range(self.NUMBER_OF_POINTS_IN_A_CIRCLE):
                next_j = self._getNextIndex(j, self.NUMBER_OF_POINTS_IN_A_CIRCLE)
                polygons.extend(self._squaresToPolygons(c[i][j],
                                                        c[next_i][j],
                                                        c[i][next_j],
                                                        c[next_i][next_j],
                                                        ))
        return polygons
        
    def getMeshArrayShape(self):
        return self.mesh_array_shape
    def setMeshArrayShape(self, shape):
        self.mesh_array_shape = shape
        
    def _getNextIndex(self, index, total):
        return 0 if index+1 == total else index+1
        
    def _generateMesh(self, radius):
        """
        Creates the mesh points of the donut by drawing an initial circle on the xy-plane,
        translating by the radius in the x direction and rotating around the y-axis.
        """
        # Draws initial circle
        circle_points = self.NUMBER_OF_POINTS_IN_A_CIRCLE
        n = circle_points-(circle_points%4)
        initial_circle = self._getAllCirclePoints(radius, n)
        
        # Translate by raidus
        translated_circle = self._translateCircle(initial_circle, radius)
        
        # Rotate by y axis and get next points for meshes
        res = []
        res.append(translated_circle)
        next_circle = translated_circle
        for i in range(n):
            next_circle = self._nextPointOnDonut(next_circle, n)
            res.append(next_circle)
            
        # Add meshes to list and track original shape.
        self.setMeshArrayShape(np.array(res).shape)
        m = self.getMeshArrayShape()
        return np.array(res).reshape(m[0]*m[1], m[2])
    
    def _getAllCirclePoints(self, r, total_points):
        """
        Get mesh points for a 2D circle given the north, south, west, east points of the circle.
        """
        res = []
        n = total_points-(total_points%4)
        circle = self._getCirclePoints(r)
        for point in circle:
            res.append(point)
            next_point = point
            for i in range(int(n/4)-1):
                next_point = self._nextPointOnCircle(next_point, n)
                res.append(next_point)
        return res
        
    def _getCirclePoints(self, r):
        """
        Returns the north, east, south, west points of a circle center around the origin.
        """
        r2 = r/2
        circle = [np.array([r2, 0 ,0 ,1]),
                np.array([0, r2 ,0 ,1]),
                np.array([-r2, 0 ,0 ,1]),
                np.array([0, -r2 ,0 ,1]),
                ]
        return circle
            
    def _nextPointOnCircle(self, points, number_of_rotations):
        """
        Get points for the circle that is placed on the xy-plane.
        """
        r = 2*math.pi/number_of_rotations
        rotation_array = np.array([[math.cos(r), math.sin(r), 0, 0],
                                   [-math.sin(r), math.cos(r), 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1],
                                   ])
        return list(np.dot(points, rotation_array)) 
        
    def _nextPointOnDonut(self, point, number_of_rotations):
        """
        Rotates along the y-axis to create the donut shape 
        """
        r = 2*math.pi/number_of_rotations
        rotation_array = np.array([[math.cos(r), 0, -math.sin(r), 0],
                                   [0, 1, 0, 0],
                                   [math.sin(r), 0, math.cos(r), 0],
                                   [0, 0, 0, 1],
                                   ])
        return list(np.dot(point, rotation_array)) 
        
    def _translateCircle(self, points, r):
        """
        Translates in the x direction by the radius.
        """
        translation_array = np.array([[1, 0, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 0, 1, 0],
                                      [r, 0, 0, 1],
                                      ])
        return list(np.dot(points, translation_array))
    