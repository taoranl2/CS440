# util.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) 
#            Krishna Harsha (kk20@illinois.edu) on 09/12/2018

"""
This file contains helper functions that helps other modules, 
"""

# Transform between alien configs and an array index
def configToIdx(config, offsets, granularity,alien):
    result = []
    for i in range(len(config[:2])):
        result.append(int((config[i]-offsets[i]) / granularity))
    result.append(alien.get_shapes().index(config[-1]))
    return tuple(result)

def idxToConfig(index, offsets, granularity,alien):
    result = []
    for i in range(len(index[:2])):
        result.append(int((index[i]*granularity)+offsets[i]))
    result.append(alien.get_shapes()[index[-1]])
    return tuple(result)

def noAlienidxToConfig(index,granularity,shape_dict):
    result = []
    for i in range(len(index[:2])):
        result.append(int((index[i]*granularity)))
    result.append(shape_dict[index[-1]])
    return tuple(result)

def isValueInBetween(valueRange, target):
    if target < min(valueRange) or target > max(valueRange):
        return False
    else:
        return True

