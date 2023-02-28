#!/usr/bin/python
import numpy as np
from PIL import Image

def main():
    s = ASCIIConverter('greygrid.png')
    s.convert_to_greyscale()
    s.image_to_blocks()
    print(len(s.asciiArt))
    
    
    del s

class ASCIIConverter:
    """
    - Convert image to greyscale
    - Seperate image in blocks
    - Convert blocks into values related to the greyscale
    - recreate the image using ascii letters to represent each value in greyscale
    - display the ascii image
    """

    def __init__(self, filename, boxSize = 10):
        self.img = Image.open(filename)
        self.keys = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
        self.keysLen = len(self.keys)
        self.boxSize = boxSize
        self.asciiArt = []
        
    def convert_to_greyscale(self):
        self.img.convert('L')
        
    def image_to_blocks(self):
        l, w = self.img.size
        self.img = np.asarray(self.img)
        
        for i in range(int(w/self.boxSize)):
            temp = []
            for j in range(int(l/self.boxSize)):
                x1 = i*self.boxSize
                x2 = (i+1)*self.boxSize
                y1 = j*self.boxSize
                y2 = (j+1)*self.boxSize
                temp.append(self._get_average(self.img[x1:x2, y1:y2]))
                
            self.asciiArt.append(temp)
        self.asciiArt = np.asarray(self.asciiArt)
        
    def _get_average(self, boxImg):
        return np.sum(boxImg) / boxImg.size
        
    #def grey_to_ascii(self):
        
    
if __name__ == "__main__":
    main()