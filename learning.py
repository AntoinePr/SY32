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

import numpy as np

from sklearn import svm

from body_detection import detection
from tool_func import same_rect

#=================================
# Apprentissage 
#=================================

def validation_croisee(xa,ya, nvc, clf):
    r = np.zeros(nvc)
    for i in range(nvc):
        print("     Level {}".format(i+1))
        mask = np.zeros(xa.shape[0], dtype=bool)
        mask[np.arange(i, mask.size, nvc)] = True
        clf.fit(xa[~mask,:], ya[~mask])
        r[i] = np.mean(clf.predict(xa[mask]) != ya[mask])
    return np.mean(r)
    

def optimisation_SVM(xa, ya, nvc, lst):
    print("==================================================")
    print("Optimisation SVM")
    print("==================================================")
    r = np.zeros(len(lst))
    count = 0
    for i in range(len(lst)):
        print("C = {}".format(lst[i]))
        print("---------------------------------------")
        clf = svm.SVC(kernel='linear', C=lst[i])
        r[count] = validation_croisee(xa, ya, nvc, clf)
        count +=1
    return [r.min(), lst[np.argmin(r)]] 

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

# Compare the positive rectangles found with the true positives
# returns all false positives vectors
def find_false_pos(label, pos_rects, pos_vectors):
    print("==================================================")
    print("Finding false positive")
    print("==================================================")
    nb_pos = pos_rects.shape[0]
    false_pos = np.zeros((64*128,), dtype=np.int)
    for i in range(pos_rects.shape[0]):
        line = pos_rects[i,]
        valid_rect = label[int(line[0]),:]
        if not same_rect(valid_rect, line[1:5]):
            false_pos = np.vstack([false_pos, pos_vectors[i,]])
        
    false_pos = np.delete(false_pos, 0, 0)
    nb_false_pos = false_pos.shape[0]
    z_false_pos = np.array([[0]] * nb_false_pos)
    print("---------------------------------------")
    print("{} false positives detected".format(nb_false_pos))
    print("---------------------------------------")
    print("{} true positives detected".format(nb_pos-nb_false_pos))
    return false_pos, z_false_pos 

# Add some false pos to the learning data and relearn the classifier
def learn_false_pos(apprFiles, label, clf, samp_matrix, samp_vector):
    err_rates = []
    for phase in range(1):
        print("==================================================")
        print("LEARNING FALSE POSITIVE, PHASE {}".format(phase+1))
        print("==================================================")
        pos_rects, pos_vectors = detection(apprFiles, clf)
        false_pos, z_false_pos = find_false_pos(label, pos_rects, pos_vectors)
        samp_matrix = np.vstack([samp_matrix, false_pos])
        samp_vector = np.append(samp_vector, z_false_pos)
        err_rates.append(validation_croisee(samp_matrix, samp_vector, 5, clf))
        clf.fit(samp_matrix, samp_vector)
    return clf, err_rates
    
    











