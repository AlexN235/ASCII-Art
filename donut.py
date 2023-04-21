#!/usr/bin/python
import numpy as np
import math
from shape import Shape
from matplotlib import pyplot as plt


def main():
    radius = 20
    r2 = radius/2
    d = Donut(20)
    points = d.key_points
    print(points[0][0])


        
def plot3D(shape):
    ## Plots down a shape based on 3d matrix
    ## For testing only

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x, y, z ,a = np.array(shape).transpose()
    ax.scatter(x, y, z, c=z, alpha=1)
    fig.show()
    
    i = input("press enter")

    
def rotateTest(points):
        r = 2*math.pi/4
        rotation_array = np.array([[1, 0, 0, 0],
                                   [0, math.cos(r), math.sin(r), 0],
                                   [0, -math.sin(r), math.cos(r), 0],
                                   [0, 0, 0, 1],
                                   ])
        res = list(np.dot(points, rotation_array)) 
        return res

class Donut(Shape):
    """
    Class representing the Cube shape.
    """
    def __init__(self, radius):
        super().__init__()
        self.drawDonut(radius)
        self.shape = 'donut'
        
    def drawDonut(self, r):
        self.grid_size = [int(2*r*self.SHAPE_TO_GRID_MULTIPLIER),
                          int(2*r*self.SHAPE_TO_GRID_MULTIPLIER),
                          int(2*r*self.SHAPE_TO_GRID_MULTIPLIER)]
        self.key_points = self._generateMesh(r)
        self.transformed_points = self.key_points
        
    def generateShape(self):
        """
        Takes the corner coordinates of a square and draws the squares polygons for the cube.
        """
        return self.key_points
        
    def _generateMesh(self, radius):
        """
        Creates the mesh points of the donut by drawing an initial circle on the xy-plane,
        translating by the radius in the x direction and rotating around the y-axis.
        """
        points_used = 20
        n = points_used-(points_used%4)
        initial_circle = self._getAllCirclePoints(radius, n)
        # translate by raidus
        translated_circle = self._translatePoints(initial_circle, radius)
        # rotate by z axis and get next points for meshes
        res = []
        res.append(translated_circle)
        next_circle = translated_circle
        for i in range(n):
            next_circle = self._nextPointOnDonut(next_circle, n)
            res.append(next_circle)
        # add meshes to list and return
        return res
    
    def _getAllCirclePoints(self, r, total_points):
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
        res = list(np.dot(points, rotation_array)) 
        return res
        
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
        res = list(np.dot(point, rotation_array)) 
        return res
        
    def _translatePoints(self, points, r):
        """
        Translates in the x direction by the radius.
        """
        translation_array = np.array([[1, 0, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 0, 1, 0],
                                      [r, 0, 0, 1],
                                      ])
        return list(np.dot(points, translation_array))
    
if __name__ == "__main__":
    main()