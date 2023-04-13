#!/usr/bin/python
import numpy as np
import math
from shape import Shape

class Cube(Shape):
    def __init__(self, l ,w, h):
        super().__init__()
        self.drawCube(l, w, h)
        
    def drawCube(self, l, w, h):
        self.grid_size = [int(l*self.SHAPE_TO_GRID_MULTIPLIER),
                          int(w*self.SHAPE_TO_GRID_MULTIPLIER),
                          int(h*self.SHAPE_TO_GRID_MULTIPLIER)]
        self.rotated_shape = []
        # One side of the cube
        self.shape.append(np.array((l, 0, h, 1)))    # A
        self.shape.append(np.array((l, w, h, 1)))    # B
        self.shape.append(np.array((l, 0, 0, 1)))    # C
        self.shape.append(np.array((l, w, 0, 1)))    # D
        # Other side of the cube
        self.shape.append(np.array((0, 0, h, 1)))    # E
        self.shape.append(np.array((0, w, h, 1)))    # F
        self.shape.append(np.array((0, 0, 0, 1)))    # G
        self.shape.append(np.array((0, w, 0, 1)))    # H
        self.shape = self.shape
        self.rotated_shape = self.shape