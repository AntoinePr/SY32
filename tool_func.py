#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 19:58:11 2017

@author: AntoineP
"""
from skimage.io import imread, imshow

# Show a sub-part of an image
def show_inner_img(path, posX, posY, width, hight):
    image = imread(path)
    image = image[posY:(posY+hight), posX:(posX+width)]
    imshow(image)
    
# show_inner_img(apprFiles[188], 207, 5, 258, 378)