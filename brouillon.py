#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 17:51:26 2017

@author: AntoineP
"""

# Avg of outer rectangle and inner rectangle
def reshape_rect(posX, posY, width, hight):
    if(2*width == hight):
        # Rectangle has the right size
        return posX, posY, width, hight
    else:
        # Rectangle too large
        Rec1 = {}
        Rec1["width"] = int(hight/2)
        Rec1["hight"] = hight
        Rec1["posX"] = posX + (width-Rec1["width"])/2
        Rec1["posY"] = posY
        Rec2 = {}
        Rec2["width"] = width
        Rec2["hight"] = width*2
        Rec2["posX"] = posX
        Rec2["posY"] = posY + (hight-Rec2["hight"])/2
        
        posX = int((Rec1["posX"]+Rec2["posX"])/2)
        posY = int((Rec1["posY"]+Rec2["posY"])/2)
        width = int((Rec1["width"]+Rec2["width"])/2)
        hight = int((Rec1["hight"]+Rec2["hight"])/2)
        return posX, posY, width, hight