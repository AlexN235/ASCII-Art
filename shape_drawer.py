#!/usr/bin/python
import numpy as np
from matplotlib import pyplot as plt
import math
import time

def main():
    """ 
    st = time.time()
    sd = ShapeDrawer()
    sd.drawCube(50, 50, 50)
    et = time.time()
    #for i in range(20):
    #    sd.rotate('x')

    plot3D(sd.getShape())
    print(et-st)
    """
    sd = ShapeDrawer()
    sd.drawCubeByFunction(10, 10, 10)
    #for i in range(12):
    #    sd.rotatePoints('x')
    plot3D(sd.shape)
    
    a = np.array([0, 0, 0])
    b = np.array([0, 8, 0])
    c = np.array([0, 0, 8])
    d = np.array([0, 8, 8])
    
    ab = np.unique(np.linspace(a, b, dtype=int), axis=0)
    cd = np.unique(np.linspace(c, d, dtype=int), axis=0)
    
    full = np.unique(np.linspace(ab, cd, dtype=int), axis=0)
    plot3D(full)
    
def plot3D(shape):
    ## Plots down a shape based on 3d matrix
    ## For testing only

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    #x, y, z = shape.nonzero()  # old method
    x, y, z = shape.transpose() # new method
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
        
    def drawCubeByFunction(self, l, w, h):
        grid_size = [l*1.5, w*1.5, h*1.5]
        # One side of the cube
        self.shape.append((l, 0, h))    # A
        self.shape.append((l, w, h))    # B
        self.shape.append((l, 0, 0))    # C
        self.shape.append((l, w, 0))    # D
        # Other side of the cube
        self.shape.append((0, 0, h))    # E
        self.shape.append((0, w, h))    # F
        self.shape.append((0, 0, 0))    # G
        self.shape.append((0, w, 0))    # H
        self.shape = np.array(self.shape)
        
    def rotatePoints(self, rotation_axis):
        self.times_rotated = (self.times_rotated + 1) % self.NUMBER_OF_ROTATIONS
        r = self.RADIANS*self.times_rotated
        rotation_array = np.array([[math.cos(r), -math.sin(r), 0],
                                   [math.sin(r), math.cos(r), 0],
                                   [0, 0, 1],
                                   ])
        self.shape = np.dot(self.shape, rotation_array)
        
    def _findPlane(self, p1, p2, p3):
        v1 = p3-p1
        v2 = p2-p1
        
        cp = np.cross(v1, v2)
        
        d = np.dot(cp, p1)
        return cp, d #(cp = A, B, C)
        
    def _findPointInPlane(self, p1, p2, p3):
        in_plane = []
        cp, d = self._findPlane(p1, p2 ,p3)
        print(cp, d)
        for point in self.shape:    
            if((point.dot(p3) + d) == 0):
                print((point.dot(p3) + d),(point.dot(p3) + d) == 0)
                in_plane.append(point)
        return in_plane
        
    def _cornersToSquares(self):
        c = self.shape
        self._fillInPolygon(c[0], c[1], c[4], c[5])
        self._fillInPolygon(c[0], c[1], c[2], c[3])
        self._fillInPolygon(c[2], c[0], c[6], c[4])
        self._fillInPolygon(c[6], c[7], c[4], c[5])
        self._fillInPolygon(c[6], c[7], c[2], c[3])
        self._fillInPolygon(c[7], c[5], c[3], c[1])
   
    def _drawPoint(self, x, y, z, a):
        print('drawPoint incomplete')
    
    def _fillInPolygon(self, p1, p2, p3, p4):
        """ input: p1 and p2 are one line and p3 p4 is a parallel line """ 
        print("TO DO")
        
    def _findCubeNeighbours(self):
        """ Use at initialization, only works if corners are squared with the axis """
        # Find two opposing corners
        corners = self.shape
        c1 = np.array(corners[0])
        c2 = np.array([x for x in corners if (c1 != x).all()][0])
        # Find the three points that are neighbours for those opposing corner
        side1 = [x for x in corners if np.count_nonzero((c1 == x)) == len(c1)-1]
        side2 = [x for x in corners if np.count_nonzero((c2 == x)) == len(c2)-1]
        side1.insert(0, c1)
        side2.insert(0, c2)
        # return two list where the head of the list are the opposing corners.
        self._cornersToPlane(side1, side2)
        return side1, side2

    def drawCube(self, l, w, h):
        self.shape = np.zeros(( #change name so there no overlap
            int(self.DIMENSION_MULTIPLE_SIZE*l),
            int(self.DIMENSION_MULTIPLE_SIZE*h),
            int(self.DIMENSION_MULTIPLE_SIZE*w),
            ))
        grid_size = np.shape(self.shape)
        self.center = {
            'x': int(grid_size[0]/2),
            'y': int(grid_size[1]/2),
            'z': int(grid_size[2]/2),
        }
        x0 = self.center['x'] - l/2
        x1 = self.center['x'] + l/2
        y0 = self.center['y'] - h/2
        y1 = self.center['y'] + h/2
        z0 = self.center['z'] - w/2
        z1 = self.center['z'] + w/2
        for idx in np.ndindex(np.shape(self.shape)):
            """ check all points to see if it exist on the surface of the cube. """
            x_condition = idx[0] >= x0 and idx[0] <= x1
            y_condition = idx[1] >= y0 and idx[1] <= y1
            z_condition = idx[2] >= z0 and idx[2] <= z1
            if idx[0] == x1 or idx[0] == x0:
                ## check if y, z are in range
                if y_condition and z_condition:
                    self.shape[idx[0]][idx[1]][idx[2]] = 1
            elif idx[1] == y1 or idx[1]  == y0:
                if x_condition and z_condition:
                ## check if x, z are in range
                    self.shape[idx[0]][idx[1]][idx[2]] = 1
            elif idx[2] == z1 or idx[2] == z0:
                ## check if x, y are in range
                if x_condition and y_condition:
                    self.shape[idx[0]][idx[1]][idx[2]] = 1
        self.rotated_shape = self.shape
        
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

                     
    def rotate(self, rotation_axis):
        """
        Rotate the shape along an axis. Either 'x', 'y', or 'z'.
        """  
        self.times_rotated = (self.times_rotated + 1) % 16
        size = np.shape(self.rotated_shape)
        new_shape = np.zeros(size)
        
        other_axis = list(self._axis.keys())
        other_axis.remove(rotation_axis)
        t1, t2 = other_axis

        for idx in np.ndindex(size):
            if self.shape[idx[0]][idx[1]][idx[2]] == 0:
                continue
            x = idx[self._axis[t1]] - self.center[t1]
            y = idx[self._axis[t2]] - self.center[t2]
            radian = math.pi/8*self.times_rotated
            new_x = int(x*math.cos(RADIANS*self.times_rotated) - y*math.sin(RADIANS*self.times_rotated) + self.center[t1]) 
            new_y = int(x*math.sin(RADIANS*self.times_rotated) + y*math.cos(RADIANS*self.times_rotated) + self.center[t2])
            self._applyRotatedPoints(rotation_axis, idx, new_x, new_y, new_shape)
        
        self.rotated_shape = new_shape
        
    def _applyRotatedPoints(self, axis, idx, x, y, temp_model):
        """
        Helper function to have points rotate on desired axis.
        """
        if axis == 'x':
            temp_model[idx[0]][x][y] = self.shape[idx[0]][idx[1]][idx[2]]
        elif axis == 'y':
            temp_model[x][idx[1]][y] = self.shape[idx[0]][idx[1]][idx[2]]
        else: #axis == 'z'
            temp_model[x][y][idx[2]] = self.shape[idx[0]][idx[1]][idx[2]]
            
    def getShape(self):
        """ 
        returns the represented shape on the 3D plane.
        """
        return self.rotated_shape
        
    def project(self):
        """
        project 3D model into 2D image by simply flatten on an plane.
        """
        res = np.zeros(np.shape(self.rotated_shape[0]))
        for i, layer in enumerate(self.rotated_shape):
            depth = i / np.shape(self.shape)[0]
            for j, row in enumerate(layer):
                res[j] = list(map(lambda x, y: x if x > 0.05 else y*depth, res[j],row))
        return np.array(list(map(lambda x: 255*(1-x), res)))
        
    def _toHexScale(self, value: int):
        if value > 1 or value < 0:
            return 0 # error
        return value*255
         
if __name__ == "__main__":
    main()