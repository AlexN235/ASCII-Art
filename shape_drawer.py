#!/usr/bin/python
import numpy as np
from matplotlib import pyplot as plt
import math
import time

def main():
    st = time.time()
    sd = ShapeDrawer()
    sd.drawCube(50, 50, 50)
    for i in range(3):
        sd.rotate('x')
    et = time.time()
    sd._cornersToSquares()
    plot3D(np.array(sd.getShape()))
    for i in sd.project():
        print(i)


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
    DIMENSION_MULTIPLE_SIZE = 1.5
    NUMBER_OF_ROTATIONS = 16
    RADIANS = 2*math.pi/NUMBER_OF_ROTATIONS # rotates 16 times
    
    def __init__(self):
        self.shape = []
        self.rotated_shape = []
        self.times_rotated = 0
        self.grid_size = []
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
        self.grid_size = [int((l+1)*1.5), int((w+1)*1.5), int((h+1)*1.5)]
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
        
    def rotate(self, rotation_axis):
        self.rotated_shape = self.shape
        self._translation(-self.grid_size[0]/3, -self.grid_size[1]/3, -self.grid_size[2]/3)
        self._rotation(rotation_axis)
        self._translation(self.grid_size[0]/3, self.grid_size[1]/3, self.grid_size[2]/3)
        
    def _rotation(self, rotation_axis):
        self.times_rotated = (self.times_rotated + 1) % self.NUMBER_OF_ROTATIONS
        r = self.RADIANS*self.times_rotated
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
        
    def _cornersToSquares(self):
        c = self.rotated_shape
        self._squaresToPolygons(c[0], c[1], c[4], c[5])
        self._squaresToPolygons(c[0], c[1], c[2], c[3])
        self._squaresToPolygons(c[2], c[0], c[6], c[4])
        self._squaresToPolygons(c[6], c[7], c[4], c[5])
        self._squaresToPolygons(c[6], c[7], c[2], c[3])
        self._squaresToPolygons(c[7], c[5], c[3], c[1])
        
    def _squaresToPolygons(self, p1, p2, p3, p4):
        self._fillInPolygon(p1, p2, p3)
        self._fillInPolygon(p3, p4, p2)
   
    def _drawPoint(self, x, y, z, a):
        print('drawPoint incomplete')
    
    def _fillInPolygon(self, p1, p2, p3):
        """ input: p1 and p2 are one line and p3 p4 is a parallel line """ 
        l1 = np.unique(np.linspace(p1, p2, dtype=int), axis=0)

        full = np.unique(np.linspace(l1, p3, dtype=int), axis=0)
        full = full.reshape((full.shape[0]*full.shape[1],4))

        self.rotated_shape.extend(list(full))
        
    def drawHalfSphere(self, radius):
        grid_size = int(2*self.DIMENSION_MULTIPLE_SIZE*radius)
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
            if d == radius:
                self.shape[idx[0]][idx[1]][idx[2]] = 1
        self.rotated_shape = self.shape
         
    def getShape(self):
        """ 
        returns the represented shape on the 3D plane.
        """
        return self.rotated_shape
        
    def project(self):
        """
        project 3D model into 2D image by simply flatten on an plane.
        """
        self._cornersToSquares()
        self._translation(self.grid_size[0]/6, self.grid_size[1]/6, self.grid_size[2]/6)
        res = np.zeros(np.array(self.grid_size[0:2]))
        print(res.shape)
        for pixel in self.rotated_shape:
            grey_value = int(self._toHexScale((self.grid_size[2] - pixel[2])/self.grid_size[2]))
            if res[int(pixel[0])][int(pixel[1])] < grey_value:
                res[int(pixel[0])][int(pixel[1])] = grey_value
        return res
        
    def _toHexScale(self, value: int):
        if value > 1 or value < 0:
            return 0 # error
        return value*255
         
if __name__ == "__main__":
    main()