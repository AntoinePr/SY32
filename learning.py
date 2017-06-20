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


    
    