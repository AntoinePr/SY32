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

# Returns true if two rectangles have an intersection
# bigger than 'ok_ratio'
def same_rect(rec1, rec2):
    # rec: posX, posY, width, hight
    ok_ratio = 0.5
    topLeftX = max(rec1[0], rec2[0])
    topLeftY = max(rec1[1], rec2[1])
    botRightX = min(rec1[0]+rec1[2], rec2[0]+rec2[2])
    botRightY = min(rec1[1]+rec1[3], rec2[1]+rec2[3])
    
    interWidth = max(botRightX-topLeftX, 0)
    interHight = max(botRightY-topLeftY, 0)
    interSize = interWidth*interHight
    
    if (interSize/(rec1[2]*rec1[3]) > ok_ratio
        or interSize/(rec2[2]*rec2[3]) > ok_ratio):
        return True
    
    return False