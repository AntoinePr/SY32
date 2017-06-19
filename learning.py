# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:17:37 2017

@author: Jean-Baptiste SIX
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 16:50:49 2017

@author: AntoineP
"""

"""
fonction pour diminuer la taille d'un image ?
"""

import glob
import random
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
# Apprentissage 
#=================================

def validation_croisee(xa,ya, nvc, clf):
    r = np.zeros(nvc)
    for i in range(nvc):
        mask = np.zeros(xa.shape[0], dtype=bool)
        mask[np.arange(i, mask.size, nvc)] = True
        clf.fit(xa[~mask,:], ya[~mask])
        r[i] = np.mean(clf.predict(xa[mask]) != ya[mask])
        print("DONE")
    return np.mean(r)
    

def optimisation_SVM(xa, ya, nvc, min, max, step):
    lst = np.arange(min, max, step)
    r = np.zeros(lst.size)
    count = 0
    for i in range(lst.size):
        clf = svm.SVC(kernel='linear', C=lst[i])
        clf.fit(xa, ya)
        r[count] = validation_croisee(xa, ya, nvc, clf)
        count +=1
    return [r.min(), lst[np.argmin(r)]] 





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
    
    