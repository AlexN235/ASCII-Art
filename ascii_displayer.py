#!/usr/bin/python
import numpy as np
from ascii_converter import ASCIIConverter
from shape_drawer import ShapeDrawer
import os
import time

def main():
    displayer = ASCIIDisplayer()
    displayer.displayGif()
    
class ASCIIDisplayer:
    def __init__(self):
        self.drawer = ShapeDrawer()
        self.drawer.drawHalfSphere(10)
        self.converter = ASCIIConverter(self.drawer.project(), 1)
        self.converter.convert()
         
    def display(self):
        os.system('cls')
        ascii_img = np.array(self.converter.get_ascii())
        l, w = ascii_img.shape
        
        for row in ascii_img:
            for x in row:
                print(x+' ', sep='', end='', flush=True)
            print("")
            
    def displayGif(self):
        end = True
        while(end):
            self.display()
            self.drawer.rotate('x')
            self.converter = ASCIIConverter(self.drawer.project(), 1)
            self.converter.convert()
            end = input("")
            if end == " ":
                end = False

if __name__ == "__main__":
    main()