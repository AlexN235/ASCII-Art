#!/usr/bin/python
import numpy as np
import math

class Shape:
    NUMBER_OF_ROTATIONS = 32
    RADIANS = 2*math.pi/NUMBER_OF_ROTATIONS 
    SHAPE_TO_GRID_MULTIPLIER = 1.7
    
    def __init__(self):
        self.shape = []
        self.rotated_shape = []
        self.grid_size = []
        self.times_rotated = {
            'x': 0,
            'y': 0,
            'z': 0,
        }
        self._axis = {
            'x': 0,
            'y': 1,
            'z': 2,
        }
    
    def getGridSize(self):
        return self.grid_size
    def getTimesRotated(self, axis):
        return self.times_rotated[axis]
    def getAllTimesRotated(self):
        return self.times_rotated
    def getShape(self):
        return self.rotated_shape
        
    def setGridSize(self, x, y, z):
        grid_size = [x, y, z]
    def setTimesRotated(self, axis, val):
        self.times_rotated[axis] = val
        
    def rotate(self, rotation_axis):
        self.rotated_shape = self.shape
        m = self.SHAPE_TO_GRID_MULTIPLIER*2
        self._translation(-self.grid_size[0]/m, -self.grid_size[1]/m, -self.grid_size[2]/m)
        self._rotation(rotation_axis)
        self._translation(self.grid_size[0]/m, self.grid_size[1]/m, self.grid_size[2]/m)
        
    def _rotation(self, rotation_axis):
        if 'x' in rotation_axis:
            self._rotateXAxis()
        if 'y' in rotation_axis:
            self._rotateYAxis()
        if 'z' in rotation_axis:
            self._rotateZAxis()

    def _rotateXAxis(self):
        self.times_rotated['x'] = (self.times_rotated['x'] + 1) % self.NUMBER_OF_ROTATIONS
        r = self.RADIANS*self.times_rotated['x']
        rotation_array = np.array([[1, 0, 0, 0],
                                   [0, math.cos(r), math.sin(r), 0],
                                   [0, -math.sin(r), math.cos(r), 0],
                                   [0, 0, 0, 1],
                                   ])
        self.rotated_shape = list(np.dot(self.rotated_shape, rotation_array)) 

    def _rotateYAxis(self):
        self.times_rotated['y'] = (self.times_rotated['y'] + 1) % self.NUMBER_OF_ROTATIONS
        r = self.RADIANS*self.times_rotated['y']
        rotation_array = np.array([[math.cos(r), 0, -math.sin(r), 0],
                                   [0, 1, 0, 0],
                                   [math.sin(r), 0, math.cos(r), 0],
                                   [0, 0, 0, 1],
                                   ])
        self.rotated_shape = list(np.dot(self.rotated_shape, rotation_array)) 

    def _rotateZAxis(self):
        self.times_rotated['z'] = (self.times_rotated['z'] + 1) % self.NUMBER_OF_ROTATIONS
        r = self.RADIANS*self.times_rotated['z']
        rotation_array = np.array([[math.cos(r), math.sin(r), 0, 0],
                                   [-math.sin(r), math.cos(r), 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1],
                                   ])
        self.rotated_shape = list(np.dot(self.rotated_shape, rotation_array))         
        
    def _translation(self, x, y, z):
        translation_array = np.array([[1, 0, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 0, 1, 0],
                                      [x, y, z, 1],
                                      ])
        self.rotated_shape = list(np.dot(self.rotated_shape, translation_array))