#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 14:08:41 2017

@author: AntoineP
"""
from skimage.io import imread, imshow
from skimage.util import img_as_float
from skimage.transform import rescale
from skimage.color import rgb2gray


#=================================
# Méthode de la fenêtre glissante
#=================================
def detection(apprFilesTest, clf):
    print("==================================================")
    print("Detection")
    print("==================================================")
    for k in range(0,len(apprFilesTest)):
        print("---------------------------------------")
        print("Image {}".format(k))
        image = rgb2gray(img_as_float(imread(apprFilesTest[k])))
        sizeX = image.shape[1]
        sizeY = image.shape[0]
        maxScaling = min(int(sizeX/64), int(sizeY/128)) - 1
        maxScaling = max(maxScaling, 3)
        for scale in range(2, maxScaling):
            print("  Scale {}".format(scale))
            img = image
            rescale(img, 1/scale, mode='reflect')
            stepX = 10
            stepY = 20
            for posX in range(0, img.shape[1]-64, stepX):
                for posY in range(0,img.shape[0]-128, stepY):
                    analyse(posX, posY, img, clf)
    
def analyse(posX, posY, image, clf):
    imageAff = image[posY:(posY+128), posX:(posX+64)]
    imageAff = imageAff.reshape(1, 64*128)
    score = clf.decision_function(imageAff)
    if score > 0.1:
        print("      PosX={}  ;  PosY={}".format(posX, posY))
        print("      Score = {}".format(clf.decision_function(imageAff)))