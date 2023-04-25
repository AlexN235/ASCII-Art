#!/usr/bin/python
import numpy as np
from PIL import Image

class ASCIIConverter:
    """
    Takes an image or 2D array and converts it into an ascii image.
    """
    def __init__(self, img, box_size = 10):
        self.ascii_characters = list(" .,-~:;=!*#$@")
        self.character_len = len(self.ascii_characters)
        self.box_size = box_size
        self.picture = []   # ascii image
        
        # img is our original image or representation of an image.
        if type(img) == str:
            self.img = Image.open(img)
            self._convert_to_greyscale()
            self.shape = self.img.size
        elif type(img) == np.ndarray:
            self.img = img
            self.shape = self.img.shape
        else:
            ## return error
            print("fail to grab image")
            
    def convert(self):
        """ Converts the original image/2D array into an ascii image """
        self._image_to_blocks()
        self._grey_to_ascii()
    
    def get_ascii(self):
        """ returns the ascii representation of the image """
        return self.picture
        
    ### In class functions ###
    def _convert_to_greyscale(self):
        """ Convert image to greyscale """
        self.img.convert('L')
        
    def _image_to_blocks(self):
        """ Seperate image in blocks """
        l, w = self.shape
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
        """ 
        Convert blocks into values related to the greyscale and recreate 
        the image using ascii letters to represent each value in greyscale
        """
        res = []
        l, w = self.picture.shape
        for i in range(w):
            row_temp = []
            for j in range(l):
                b = int(self.picture[j][i]*(self.character_len-1)/255)
                row_temp.append(self.ascii_characters[b])
            res.append(row_temp)
        self.picture = res
       
        