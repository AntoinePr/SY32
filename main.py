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

clf = svm.SVC(kernel='linear', C=0.01)
clf.fit(samp_matrix, samp_vector)

validation_croisee(samp_matrix, samp_vector, 5, clf)

clf = learn_false_pos(apprFiles, label, clf, samp_matrix, samp_vector)

validation_croisee(samp_matrix, samp_vector, 5, clf)

tmpTest = apprFilesTest[0:10]
pos_rects, pos_vectors = detection(tmpTest, clf)

false_pos, z_false_pos = find_false_pos(label, pos_rects, pos_vectors)

show_inner_img(tmpTest[0], 0, 0, 2000, 2000)
show_inner_img(tmpTest[0], 440, 420, 64*2, 128*2)


























