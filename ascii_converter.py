#!/usr/bin/python
import numpy as np
from PIL import Image

def main():
    s = ASCIIConverter('greygrid.png')
    s.convert()
    s.display()
    
    del s

class ASCIIConverter:
    """
    - Convert image to greyscale
    - Seperate image in blocks
    - Convert blocks into values related to the greyscale
    - recreate the image using ascii letters to represent each value in greyscale
    - display the ascii image
    """

    def __init__(self, img, box_size = 10):
        self.keys = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.")
        self.keys_len = len(self.keys)
        self.box_size = box_size
        self.picture = []
        
        if type(img) == str:
            self.img = Image.open(img)
            self._convert_to_greyscale()
        elif type(img) == list:
            self.img = img
        else:
            ## return error
            print("fail to grab image")

    def _convert_to_greyscale(self):
        self.img.convert('L')
        
    def _image_to_blocks(self):
        l, w = self.img.size
        self.img = np.asarray(self.img)
        
        for i in range(int(w/self.box_size)):
            temp = []
            for j in range(int(l/self.box_size)):
                x1 = i*self.box_size
                x2 = (i+1)*self.box_size
                y1 = j*self.box_size
                y2 = (j+1)*self.box_size
                temp.append(self._get_average(self.img[x1:x2, y1:y2]))
                
            self.picture.append(temp)
        self.picture = np.asarray(self.picture)
        
    def _get_average(self, boxImg):
        return np.sum(boxImg) / boxImg.size
        
    def _grey_to_ascii(self):
        res = []
        l, w = self.picture.shape
        for i in range(w):
            row_temp = []
            for j in range(l):
                b = int(self.picture[j][i]*(self.keys_len-1)/255)
                row_temp.append(self.keys[b])
            res.append(row_temp)
        self.picture = res
        
    def convert(self):
        self._image_to_blocks()
        self._grey_to_ascii()
    
    def get_ascii(self):
        return self.picture
        
if __name__ == "__main__":
    main()