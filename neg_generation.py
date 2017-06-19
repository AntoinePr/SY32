#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 10:23:56 2017

@author: AntoineP
"""

import random
import numpy as np


# Returns true if two rectangles have an intersection
# bigger than 'ok_ratio'
def same_rect(rec1, rec2):
    # rec: posX, posY, width, hight
    ok_ratio = 0.7
    topLeftX = max(rec1[0], rec2[0])
    topLeftY = max(rec1[1], rec2[1])
    botRightX = min(rec1[0]+rec1[2], rec2[0]+rec2[2])
    botRightY = min(rec1[1]+rec1[3], rec2[1]+rec2[3])
    
    interWidth = max(botRightX-topLeftX, 0)
    interHight = max(botRightY-topLeftY, 0)
    interSize = interWidth*interHight
    
    if (interSize/(rec1[2]*rec1[3]) > ok_ratio
        or interSize/(rec2[2]*rec2[3]) > ok_ratio):
        return True
    
    return False
    
# Returns a random rectangle of the right format
# makes sure it fits into the photo
def random_rect(sizeX, sizeY):
    base = [64, 128]
    maxScaling = min(int(sizeX/base[0]), int(sizeY/base[1])) - 2
    scale = random.randint(2, maxScaling)
    
    rectSize = [x * scale for x in base]
    posX = random.randint(0, sizeX-rectSize[0])
    posY = random.randint(0, sizeY-rectSize[1])
    
    return [posX, posY, rectSize[0], rectSize[1]]
      
#image = imread(apprFiles[79])
#rect = random_rect(415, 751)
#show_inner_img(apprFiles[79], rect[0], rect[1], rect[2], rect[3])

# Return an array of different random rectangles for
# a given picture format
def pict_neg_samples_generation(sizeX, sizeY):
    init_nb_of_samples = 50
    neg_samples = np.zeros((init_nb_of_samples, 4), dtype=np.int)
    res_samples = np.zeros((init_nb_of_samples, 4), dtype=np.int)
    
    # Populate neg_samples with random rectangles
    for i in range(init_nb_of_samples):
        neg_samples[i,:] = random_rect(sizeX, sizeY)
    
    # Remove homogenious rectangles from 'neg_samples'
    ite = 0
    while len(neg_samples.shape)>1 and neg_samples.shape[0] > 0:
        sample = neg_samples[0,:]
        # Add the sample to the result
        res_samples[ite,:] = sample
        ite += 1
        # Remove all rectangles similar to the curent one from 'neg_samples'
        index = 0
        to_delete = []
        for line in neg_samples:
            if same_rect(sample, line):
                to_delete.append(index)
            index += 1
        neg_samples = np.delete(neg_samples, to_delete, axis=0)
    
    # Remove empty rows from 'res_samples'
    index = 0
    to_delete = []
    for line in res_samples:
        if np.array_equal(line, [0, 0, 0, 0]):
            to_delete.append(index)
        index += 1
    res_samples = np.delete(res_samples, to_delete, axis=0)
        
    return res_samples

#samp = pict_neg_samples_generation(415, 751)
#i += 1
#rect = samp[i,:]
#show_inner_img(apprFiles[79], rect[0], rect[1], rect[2], rect[3])