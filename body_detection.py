#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 14:08:41 2017

@author: AntoineP
"""

import glob
import numpy as np

#from shutil import copyfile
from skimage.io import imread, imshow
from skimage.util import img_as_float
from skimage.transform import rescale
from sklearn import svm
from skimage.color import rgb2gray


from neg_generation import *
from preformating import *
from tool_func import *

apprFiles = glob.glob("projetpers/train/*")
label = np.loadtxt("projetpers/label.txt", dtype=np.int)

#=================================
# Méthode de la fenêtre glissante
#=================================
apprFilesTest = glob.glob("projetpers/test/*")

   
for k in range(1,len(apprFilesTest)):
    image = rgb2gray(img_as_float(imread(apprFilesTest[1])))
    for s in range(2, 8):
        rescale(image, s*0.1)
        for posX in range(1, image.shape[1]-128, 20):
            for posY in range(1,image.shape[0]-128, 20):
                print("X = " ,posX)
                print("Y = " ,posY)
                #analyse(posX, posY, image, clf)
    
    
    
def analyse(posX, posY, image, clf):
    imageOK = image.reshape(image.shape[0], image.shape[1])
    pred = clf.predict(imageOK)
    if pred == 1:
        imageAff = image[posY:(posY+128), posX:(posX+64)]
        imshow(imageAff)