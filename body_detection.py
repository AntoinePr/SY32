#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 14:08:41 2017

@author: AntoineP
"""

import glob

#from shutil import copyfile
from skimage.io import imread, imshow
from skimage.util import img_as_float
from skimage.transform import rescale
from skimage.color import rgb2gray


#=================================
# Méthode de la fenêtre glissante
#=================================
apprFilesTest = glob.glob("projetpers/test/*")

def detection(apprFilesTest):
    for k in range(1,len(apprFilesTest)):
        image = rgb2gray(img_as_float(imread(apprFilesTest[1])))
        for s in range(2, 8):
            sizeX = image.shape[1]
            sizeY = image.shape[0]
            base = [64, 128]
            maxScaling = min(int(sizeX/base[0]), int(sizeY/base[1])) - 2
            maxScaling = max(maxScaling, 2)
            for posX in range(1, image.shape[1]-128, 20):
                for posY in range(1,image.shape[0]-128, 20):
                    print("X = " ,posX)
                    print("Y = " ,posY)
                    analyse(posX, posY, image, clf)
    
    
    
def analyse(posX, posY, image, clf):
    imageOK = image.reshape(image.shape[0], image.shape[1])
    pred = clf.predict(imageOK)
    if pred == 1:
        imageAff = image[posY:(posY+128), posX:(posX+64)]
        imshow(imageAff)