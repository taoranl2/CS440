
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
# from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *
import os
import math

def transformToMaze(alien, goals, walls, window,granularity):
    """This function transforms the given 2D map to the maze in MP1.

        Args:
            alien (Alien): alien instance
            goals (list): [(x, y, r)] of goals
            walls (list): [(startx, starty, endx, endy)] of walls
            window (tuple): (width, height) of the window

        Return:
            Maze: the maze instance generated based on input arguments.

    """

    numcol = int(window[0] / granularity) + 1
    numrow = int(window[1] / granularity) + 1
    map = np.full((numcol, numrow, 3), ' ')
    shapes = ['Horizontal', 'Ball', 'Vertical']

    config = alien.get_config()
    alien_id = configToIdx(config, [0, 0], granularity, alien)
    map[alien_id[0]][alien_id[1]][alien_id[2]] = 'P'

    for i in range(3):
        alien.set_alien_shape(shapes[i])
        for row in range(numrow):
            for col in range(numcol):
                configi = idxToConfig((col, row, i), [0, 0], granularity, alien)
                alien.set_alien_config(configi)
                if does_alien_touch_wall(alien, walls, granularity) and map[col][row][i] != 'P':
                    map[col][row][i] = '%'
                elif does_alien_touch_goal(alien, goals) and map[col][row][i] != 'P':
                    map[col][row][i] = '.'

    return Maze(map, alien, granularity)

if __name__ == '__main__':
    import configparser

    def generate_test_mazes(granularities,map_names):
        for granularity in granularities:
            for map_name in map_names:
                try:
                    print('converting map {} with granularity {}'.format(map_name,granularity))
                    configfile = './maps/test_config.txt'
                    config = configparser.ConfigParser()
                    config.read(configfile)
                    lims = eval(config.get(map_name, 'Window'))
                    # print(lis)
                    # Parse config file
                    window = eval(config.get(map_name, 'Window'))
                    centroid = eval(config.get(map_name, 'StartPoint'))
                    widths = eval(config.get(map_name, 'Widths'))
                    alien_shape = 'Ball'
                    lengths = eval(config.get(map_name, 'Lengths'))
                    alien_shapes = ['Horizontal','Ball','Vertical']
                    obstacles = eval(config.get(map_name, 'Obstacles'))
                    boundary = [(0,0,0,lims[1]),(0,0,lims[0],0),(lims[0],0,lims[0],lims[1]),(0,lims[1],lims[0],lims[1])]
                    obstacles.extend(boundary)
                    goals = eval(config.get(map_name, 'Goals'))
                    alien = Alien(centroid,lengths,widths,alien_shapes,alien_shape,window)
                    generated_maze = transformToMaze(alien,goals,obstacles,window,granularity)
                    generated_maze.saveToFile('./mazes/{}_granularity_{}.txt'.format(map_name,granularity))
                except Exception as e:
                    print('Exception at maze {} and granularity {}: {}'.format(map_name,granularity,e))
    def compare_test_mazes_with_gt(granularities,map_names):
        name_dict = {'%':'walls','.':'goals',' ':'free space','P':'start'}
        shape_dict = ['Horizontal','Ball','Vertical']
        for granularity in granularities:
            for map_name in map_names:
                this_maze_file = './mazes/{}_granularity_{}.txt'.format(map_name,granularity)
                gt_maze_file = './mazes/gt_{}_granularity_{}.txt'.format(map_name,granularity)
                if(not os.path.exists(gt_maze_file)):
                    print('no gt available for map {} at granularity {}'.format(map_name,granularity))
                    continue
                gt_maze = Maze([],[],[],filepath = gt_maze_file)
                this_maze = Maze([],[],[],filepath= this_maze_file)
                gt_map = np.array(gt_maze.get_map())
                this_map = np.array(this_maze.get_map())
                difx,dify,difz = np.where(gt_map != this_map)
                if(difx.size != 0):
                    diff_dict = {}
                    for i in ['%','.',' ','P']:
                        for j in ['%','.',' ','P']:
                            diff_dict[i + '_'+ j] = []
                    print('\n\nDifferences in {} at granularity {}:'.format(map_name,granularity))    
                    for i,j,k in zip(difx,dify,difz):
                        gt_token = gt_map[i][j][k] 
                        this_token = this_map[i][j][k]
                        diff_dict[gt_token + '_' + this_token].append(noAlienidxToConfig((j,i,k),granularity,shape_dict))
                    for key in diff_dict.keys():
                        this_list = diff_dict[key]
                        gt_token = key.split('_')[0]
                        your_token = key.split('_')[1]
                        if(len(this_list) != 0):
                            print('Ground Truth {} mistakenly identified as {}: {}'.format(name_dict[gt_token],name_dict[your_token],this_list))
                    print('\n\n')
                else:
                    print('no differences identified  in {} at granularity {}:'.format(map_name,granularity))
    ### change these to speed up your testing early on! 
    granularities = [2,5,8,10]
    map_names = ['Test1','Test2','Test3','Test4','NoSolutionMap']
    generate_test_mazes(granularities,map_names)
    compare_test_mazes_with_gt(granularities,map_names)
