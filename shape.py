#!/usr/bin/python
import numpy as np
import math

class Shape:
    """
    Class representing the different shapes that will be drawn. The shape is represented
    by a smaller amount of points that draws a mesh of the shape. Transform the shapes
    through translations and rotations. All points are then generated during output in 
    the ShapeDrawer class.
    """
    NUMBER_OF_ROTATIONS = 32
    RADIANS = 2*math.pi/NUMBER_OF_ROTATIONS 
    SHAPE_TO_GRID_MULTIPLIER = 2
    
    def __init__(self):
        self.shape = ''
        self.mesh_points = []
        self.transformed_points = []
        self.grid_size = []
        self.times_rotated = {
            'x': 0,
            'y': 0,
            'z': 0,
        }
        
    # Getters
    def getShapeName(self):
        return self.shape
    def getGridSize(self):
        return self.grid_size
    def getTimesRotated(self, axis):
        return self.times_rotated[axis]
    def getAllTimesRotated(self):
        return self.times_rotated
    def getMesh(self):
        return self.mesh_points
    def getTransformedMesh(self):
        return self.transformed_points
    # Setters
    def setGridSize(self, x, y, z):
        self.grid_size = [x, y, z]
    def setTimesRotated(self, axis, val):
        self.times_rotated[axis] = val
        
    def translateToDisplay(self):
        """
        Translate the current shape to coordinates to be easily projected.
        """
        m = self.SHAPE_TO_GRID_MULTIPLIER
        size = self.getGridSize()
        self._translation(size[0]/m, size[1]/m, size[2]/m)

    def rotate(self, rotation_axis):
        """
        Rotates the shape around the center of the shape.
        """
        self.transformed_points = self.getMesh()
        self._rotation(rotation_axis)
     
    ### in class functions ###
    def _rotation(self, rotation_axis):
        """
        Input: a list containing either 'x', 'y', 'z' representing the x, y, z axis respectively.
        Rotates current key points representing the shape by the axis in the input.
        """
        if 'x' in rotation_axis:
            self._rotateXAxis()
        if 'y' in rotation_axis:
            self._rotateYAxis()
        if 'z' in rotation_axis:
            self._rotateZAxis()

    def _rotateXAxis(self):
        self.times_rotated['x'] = self.times_rotated['x'] + 1 % self.NUMBER_OF_ROTATIONS
        r = self.RADIANS*self.times_rotated['x']
        rotation_array = np.array([[1, 0, 0, 0],
                                   [0, math.cos(r), math.sin(r), 0],
                                   [0, -math.sin(r), math.cos(r), 0],
                                   [0, 0, 0, 1],
                                   ])
        self.transformed_points = list(np.dot(self.transformed_points, rotation_array)) 

    def _rotateYAxis(self):
        self.times_rotated['y'] = self.times_rotated['y'] + 1 % self.NUMBER_OF_ROTATIONS
        r = self.RADIANS*self.times_rotated['y']
        rotation_array = np.array([[math.cos(r), 0, -math.sin(r), 0],
                                   [0, 1, 0, 0],
                                   [math.sin(r), 0, math.cos(r), 0],
                                   [0, 0, 0, 1],
                                   ])
        self.transformed_points = list(np.dot(self.transformed_points, rotation_array)) 

    def _rotateZAxis(self):
        self.times_rotated['z'] = self.times_rotated['z'] + 1 % self.NUMBER_OF_ROTATIONS
        r = self.RADIANS*self.times_rotated['z']
        rotation_array = np.array([[math.cos(r), math.sin(r), 0, 0],
                                   [-math.sin(r), math.cos(r), 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1],
                                   ])
        self.transformed_points = list(np.dot(self.transformed_points, rotation_array))         
        
    def _translation(self, x, y, z):
        translation_array = np.array([[1, 0, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 0, 1, 0],
                                      [x, y, z, 1],
                                      ])
        self.transformed_points = list(np.dot(self.transformed_points, translation_array))
        
    def _squaresToPolygons(self, p1, p2, p3, p4):
        points = []
        points.append(np.array([p1, p2, p3]))
        points.append(np.array([p3, p4, p2]))
        return points