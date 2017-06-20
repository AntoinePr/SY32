#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 16:50:49 2017

@author: AntoineP
"""

"""
fonction pour diminuer la taille d'un image ?
"""

"""
Rapport pour dimanche 25/06
10 points rapports
5 points code
5 points résultats

Résultats peuvent être envoyés le dimanche 02/07
"""

import glob
import numpy as np

from skimage.io import imread, imshow
from skimage.util import img_as_float
from sklearn import svm
from sklearn.ensemble import AdaBoostClassifier

from learning import *
from neg_generation import generate_all_neg
from preformating import uniformize_label_sizes
from tool_func import *

apprFiles = glob.glob("projetpers/train/*")
apprFilesTest = glob.glob("projetpers/test/*")
label = np.loadtxt("projetpers/label.txt", dtype=np.int)
label = np.delete(label, 0, 1)

label = uniformize_label_sizes(label, apprFiles)

samp_matrix, samp_vector  = generate_all_neg(label, apprFiles)

"""
clf = svm.SVC(kernel='linear')
lst = [0.001, 0.01, 0.1, 1, 10]
r, C = optimisation_SVM(samp_matrix, samp_vector, 5, lst)
# r = 0.104; C = 0.01
lst = [0.001, 0.005, 0.01, 0.05, 0.1]
r, C = optimisation_SVM(samp_matrix, samp_vector, 5, lst)
# r = 0.104; C = 0.01
lst = [0.006, 0.008, 0.01, 0.02, 0.04]
r, C = optimisation_SVM(samp_matrix, samp_vector, 5, lst)
# r = 0.104; C = 0.01
"""

clf = svm.SVC(kernel='linear', C=0.01)
clf.fit(samp_matrix, samp_vector)
















