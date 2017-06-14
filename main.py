#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 16:50:49 2017

@author: AntoineP
"""

"""
fonction pour diminuer la taille d'un image ?
"""

import numpy as np
import glob

#from shutil import copyfile
from skimage.io import imread, imsave, imshow
from skimage.util import img_as_float

apprFiles = glob.glob("train/*")
#copyfile("label.txt", "temp.txt")
file = np.loadtxt("label.txt", dtype=np.int)

# Reshape the rectangle so that 2*width = hight
def reshape_rect(posX, posY, width, hight):
    if(2*width > hight):
        # Rectangle too large
        oldHight = hight
        hight = 2*width
        posY = posY + int((oldHight-hight)/2)
    elif(2*width < hight):
        # Rectangle too hight
        oldWidth = width
        width = int(hight/2)
        # Makes sure the hight is exactly twicce bigger
        hight = 2*width
        posX = posX + int((oldWidth-width)/2)
        
    return posX, posY, width, hight
        
        
def show_inner_img(path, posX, posY, width, hight):
    image = imread(path)
    image = image[posY:(posY+hight), posX:(posX+width)]
    imshow(image)
    
show_inner_img(apprFiles[0], file[0,1], file[0,2], file[0,3], file[0,4])
posX, posY, width, hight = reshape_rect(file[0,1], file[0,2], file[0,3], file[0,4])
show_inner_img(apprFiles[0], posX, posY, width, hight)
    
    
    
    
    
    
    
    
    
    
    
    