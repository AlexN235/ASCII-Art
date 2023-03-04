#!/usr/bin/python
import numpy as np
from ascii_converter import ASCIIConverter
import os

def main():
    a = ASCIIDisplayer('greygrid.png')
    a.display()
    
class ASCIIDisplayer:
    def __init__(self, img):
        self.converter = ASCIIConverter(img)
        self.converter.convert()
        
    def display(self):
        os.system('cls')
        ascii_img = np.array(self.converter.get_ascii())
        l, w = ascii_img.shape
        
        for row in ascii_img:
            for x in row:
                print(x+' ', sep='', end='', flush=True)
            print("")
    
if __name__ == "__main__":
    main()