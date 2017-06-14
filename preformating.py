#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 20:03:04 2017

@author: AntoineP
"""

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
        
    posX = max(posX, 0)
    posY = max(posY, 0)
        
    return posX, posY, width, hight
    
#show_inner_img(apprFiles[0], label[0,1], label[0,2], label[0,3], label[0,4])
#posX, posY, width, hight = reshape_rect(label[0,1], label[0,2], label[0,3], label[0,4])
#show_inner_img(apprFiles[0], posX, posY, width, hight)

def uniformize_label_sizes(label):
    for i in range(label.shape[0]):
        label[i,1:5] = reshape_rect(
                label[i,1], label[i,2], 
                label[i,3], label[i,4])
    return label