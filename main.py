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

from neg_generation import *
from preformating import *
from tool_func import *

apprFiles = glob.glob("projetpers/train/*")
label = np.loadtxt("projetpers/label.txt", dtype=np.int)



































