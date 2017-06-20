#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 10:23:56 2017

@author: AntoineP
"""

import random
import numpy as np

from skimage import img_as_float
from skimage.color import rgb2gray
from skimage.io import imread
from skimage.transform import rescale


# Returns true if two rectangles have an intersection
# bigger than 'ok_ratio'
def same_rect(rec1, rec2):
    # rec: posX, posY, width, hight
    ok_ratio = 0.5
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
    # Makes sure maxScaling is big enough
    maxScaling = max(maxScaling, 2)
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
def generate_pict_neg(sizeX, sizeY, posRect):
    init_nb_of_samples = 50
    neg_samples = np.zeros((init_nb_of_samples, 4), dtype=np.int)
    res_samples = np.zeros((init_nb_of_samples, 4), dtype=np.int)
    
    # Populate neg_samples with random rectangles
    for i in range(init_nb_of_samples):
        neg_samples[i,:] = random_rect(sizeX, sizeY)
    
    # Remove rectangles similar to 'posRect'
    index = 0
    to_delete = []
    for line in neg_samples:
        if same_rect(posRect, line):
            to_delete.append(index)
        index += 1
    neg_samples = np.delete(neg_samples, to_delete, axis=0)
    
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

def rescale_rect(rect, scale):
    rect[0] = int(rect[0]*scale)
    rect[1] = int(rect[1]*scale)
    rect[2] = 64
    rect[3] = 128
    return rect
    

def from_rect_to_vector(image, rect):
    scale = 64/rect[2]
    image = rescale(image, scale, mode='reflect')
    rect = rescale_rect(rect, scale)
    vector = image[rect[1]:rect[1]+128, rect[0]:rect[0]+64]
    if vector.size != 8192:
        print("ERROR: vector has a wrong size to reshape")
        import pdb; pdb.set_trace()
    vector = vector.reshape(64*128)
    return vector

def generate_all_neg(label, apprFiles):
    print("==================================================")
    print("Generating all negative samples")
    print("==================================================")
    image = rgb2gray(imread(apprFiles[0]))
    image = img_as_float(image)
    
    # Instanciation of neg_matrix
    posRect = label[0]
    neg_samp = generate_pict_neg(image.shape[1], 
                                 image.shape[0], 
                                 posRect)
    # Add of first posRect
    samp_matrix = from_rect_to_vector(image, label[0,])
    samp_vector = [1]
    
    # Add of new lines to neg_matrix from first sample
    for i in range(neg_samp.shape[0]):
        new_row = from_rect_to_vector(image, neg_samp[i,])
        samp_matrix = np.vstack([samp_matrix, new_row])
        samp_vector.append(0)
    
    # Add of pos and neg vectors to the matrix
    # for all pictures
    for img_id in range(1, len(apprFiles)):
        if ((img_id) % 1) == 0:
            print("{} pictures treated".format(img_id))
            print("---------------------------------------")
        # Reading of the picture
        image = rgb2gray(imread(apprFiles[img_id]))
        image = img_as_float(image)
        posRect = label[img_id]
        
        # Add of pos vectors of the image
        new_row = from_rect_to_vector(image, posRect)
        samp_matrix = np.vstack([samp_matrix, new_row])
        samp_vector.append(1)
        
        #Add of neg vectors of the image
        neg_samp = generate_pict_neg(image.shape[1], 
                                     image.shape[0],
                                     posRect)
        for j in range(1, neg_samp.shape[0]):
            new_row = from_rect_to_vector(image, neg_samp[j,])
            samp_matrix = np.vstack([samp_matrix, new_row])
            samp_vector.append(0)
    
    samp_vector = np.array(samp_vector)

    return samp_matrix, samp_vector 








