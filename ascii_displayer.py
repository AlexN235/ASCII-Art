#!/usr/bin/python
import numpy as np
import os
import time
import sys
from ascii_converter import ASCIIConverter
from shape_drawer import ShapeDrawer

def main(args):
    displayer = ASCIIDisplayer(*args[1:])
    displayer.displayGif()

class ASCIIDisplayer:
    ANIMATION_TIMER = 0.1
    def __init__(self, shape = 'cube'):
        if shape == 'cube':
            self.drawer = ShapeDrawer('cube')
        elif shape == 'donut':
            self.drawer = ShapeDrawer('donut')
        else:   # default to cube shape
            self.drawer = ShapeDrawer('cube')
         
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
            
    def displayGif(self, shape = 'cube'):
        """
        displays an animated gif of a rotating shape in ascii art.
        """
        end = True
        while(end):
            self.drawer.rotate(['x', 'y', 'z'])
            self.converter = ASCIIConverter(self.drawer.project(), 1)
            self.converter.convert()
            self.display()
            time.sleep(self.ANIMATION_TIMER)

if __name__ == "__main__":
    args = sys.argv
    main(args)