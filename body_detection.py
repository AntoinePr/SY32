#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 14:08:41 2017

@author: AntoineP
"""
import numpy as np

from skimage.io import imread
from skimage.util import img_as_float
from skimage.transform import rescale
from skimage.color import rgb2gray


from tool_func import same_rect

MIN_SCORE  = 0.5 

# Analyse all pictures and returns a list
# of the coordinates of the detected bodies
def detection(apprFiles, clf):
    print("==================================================")
    print("Detection")
    print("==================================================")
    rects = np.zeros(6)
    vectors = np.zeros((64*128,), dtype=np.int)
    for k in range(0,len(apprFiles)):
        print("---------------------------------------")
        print("Image {}: {}".format(k, apprFiles[k]))
        pos_rects, pos_vectors = analyse_sub_pict(k, apprFiles[k], clf)
        if pos_rects is not None:
            rects = np.vstack([rects, pos_rects])
            vectors = np.vstack([vectors, pos_vectors])
    rects = np.delete(rects, 0, 0)
    vectors = np.delete(vectors, 0, 0)
    return rects, vectors

def analyse_sub_pict(pict_nb , pict_path, clf):
    # Reading of the image
    image = rgb2gray(img_as_float(imread(pict_path)))
    sizeX = image.shape[1]
    sizeY = image.shape[0]
    # Calculation of maxScaling
    maxScaling = min(int(sizeX/64), int(sizeY/128))
    maxScaling = max(maxScaling, 3)
    # Instanciation of arrays
    pos_rects = np.zeros(5)
    pos_vectors = np.zeros((64*128,), dtype=np.int)
    
    # Finding of positive rects per scale
    for scale in range(2, maxScaling):
        nb_pos = 0
        img = rescale(image, 1/scale, mode='reflect')
        stepX = 10
        stepY = 20
        # Translation over the X axis
        for posX in range(0, img.shape[1]-64, stepX):
            # Translation over the Y axis
            for posY in range(0,img.shape[0]-128, stepY):
                score, vector = is_a_body(posX, posY, img, clf)
                # Add of positive rectangle
                if score > MIN_SCORE:
                    nb_pos += 1
                    new_rect = np.array([ 
                            posX*scale,
                            posY*scale,
                            64*scale,
                            128*scale,
                            score])
                    pos_rects = np.vstack([pos_rects, new_rect])
                    pos_vectors = np.vstack([pos_vectors, vector])
        
        print("..................")
        print("Scale {}:  {} positive rects found".format(scale, nb_pos))

    # Remove of empty first row
    pos_rects = np.delete(pos_rects, 0, 0)
    pos_vectors = np.delete(pos_vectors, 0, 0)
    
    if len(pos_rects.shape) < 2:
        print("..................")
        print("No positive rectangles found")
        return None, None
              
    print("..................")
    print("{} rects before reducing number".format(pos_rects.shape[0]))
    
    pos_rects, pos_vectors = reduce_nb_rects(pos_rects, pos_vectors)
    print("..................")
    print("{} rects after".format(pos_rects.shape[0]))
    
    # Add of the picture number to the result
    pict_indice = np.array([[pict_nb]] * pos_rects.shape[0])
    pos_rects = np.append(pict_indice, pos_rects, axis=1)
                    
    return pos_rects, pos_vectors

# Analyse sub-picture and returns the score of the vector, and the vector
def is_a_body(posX, posY, image, clf):
    vector = image[posY:(posY+128), posX:(posX+64)]
    vector = vector.reshape(1, 64*128)
    score = clf.decision_function(vector)
    """
    if score > MIN_SCORE:
        print("    Score = {}  ;  PosX={}  ;  PosY={}".format(
                clf.decision_function(imageAff),
                posX, posY))
    """
    return score, vector

# Reduce the number of rectangles by only keeping those with the highest score
def reduce_nb_rects(pos_rects, pos_vectors):        
    res_rects = np.zeros(5)
    res_vectors = np.zeros((64*128,), dtype=np.int)
    
    while len(pos_rects.shape)>1 and pos_rects.shape[0] > 0:
        new_rect = pos_rects[0,:]
        new_vector = pos_vectors[0,:]
        index = 0
        to_delete = []
        for line in pos_rects:
            if same_rect(new_rect[0:4], line[0:4]):
                to_delete.append(index)
                # Keep the rectangle with the highest score
                if line[4] > new_rect[4]:
                    new_rect = line
                    new_vector = pos_vectors[index,:]
            index += 1
            
        #Add rect found to the result
        res_rects = np.vstack([res_rects, new_rect])
        res_vectors = np.vstack([res_vectors, new_vector])
        
        # Delete rectangles
        pos_rects = np.delete(pos_rects, to_delete, axis=0)
        pos_vectors = np.delete(pos_vectors, to_delete, axis=0)
    
    # Remove of empty first row
    res_rects = np.delete(res_rects, 0, axis=0)
    res_vectors = np.delete(res_vectors, 0, axis=0)
    
    return res_rects, res_vectors
        
        
        
        
    
    
    
    