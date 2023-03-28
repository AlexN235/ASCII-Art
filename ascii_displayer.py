#!/usr/bin/python
import numpy as np
import os
import time
from ascii_converter import ASCIIConverter
from shape_drawer import ShapeDrawer

def main():
    displayer = ASCIIDisplayer('cube')
    displayer.displayGif()

    """
    TO DO:
        - make displayGif function change the image change based on time.
        - rotated along multiple axis.
        - 
    """
class ASCIIDisplayer:
    ANIMATION_TIMER = 0.5
    def __init__(self, shape = 'halfsphere'):
        self.drawer = ShapeDrawer()
        if shape == 'halfsphere':
           self.drawer.drawHalfSphere(10)
        elif shape == 'cube':
            self.drawer.drawCube(10, 10, 10)
        self.converter = ASCIIConverter(self.drawer.project(), 1)
        self.converter.convert()
         
    def display(self):
        """
        prints the ascii art of the contained shape.
        """
        os.system('cls')
        ascii_img = np.array(self.converter.get_ascii())
        l, w = ascii_img.shape
        
        for row in ascii_img:
            for x in row:
                print(x+' ', sep='', end='', flush=True)
            print("")
            
    def displayGif(self, shape = 'halfsphere'):
        """
        displays an animated gif of a rotating shape in ascii art.
        """
        end = True
        while(end):
            self.display()
            self.drawer.rotate('x')
            self.converter = ASCIIConverter(self.drawer.project(), 1)
            self.converter.convert()
            time.sleep(self.ANIMATION_TIMER)

if __name__ == "__main__":
    main()