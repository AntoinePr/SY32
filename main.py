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
import random
import numpy as np

#from shutil import copyfile
from skimage.io import imread, imshow
from skimage.util import img_as_float

from neg_generation import *
from preformating import uniformize_label_sizes
from tool_func import *

apprFiles = glob.glob("projetpers/train/*")
label = np.loadtxt("projetpers/label.txt", dtype=np.int)
label = np.delete(label, 0, 1)

label = uniformize_label_sizes(label, apprFiles)

samp_matrix, samp_vector  = generate_all_neg(label, apprFiles)




























