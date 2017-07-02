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

from body_detection import *
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

clf = svm.SVC(kernel='linear', C=0.01, class_weight={0:0.1, 1:0.9})
clf.fit(samp_matrix, samp_vector)
err_rates = []
err_rates += validation_croisee(samp_matrix, samp_vector, 5, clf)

clf, errs = learn_false_pos(apprFiles, label, clf, samp_matrix, samp_vector)
err_rates  += errs
    

pos_rects, pos_vectors = detection(apprFilesTest, clf)

rects = pos_rects
rects[:, 0].astype('int')

fmt='%03d %d %d %d %d %f'
np.savetxt('result.txt', rects, fmt=fmt)




















