# maze.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Michael Abir (abir2@illinois.edu) and 
#            Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018
"""
This file contains the Maze class, which reads in a maze file and creates
a representation of the maze that is exposed through a simple interface.
"""

import copy
import numpy as np
from const import *
from util import *
from itertools import chain

class MazeError(Exception):
    pass

class NoStartError(Exception):
    pass

class NoObjectiveError(Exception):
    pass

class Maze:
    def __init__(self, input_map, alien, granularity=DEFAULT_GRANULARITY, offsets=[0, 0, 0], filepath=None):
        """Initialize the Maze class

        Args:
            input_map (array_like): input maze map of shape (num_cols, num_rows, num_levels)
            granularity (int): step size of the alien
            alien (Alien): the Alien instance
            offsets (list): list of offsets to make the maze start at (0,0,0) Ignore for this mp
            filepath (str): file path to the ASCII maze
        """        
        self.states_explored = 0
        if filepath:
            self.granularity = 0
            self.readFromFile(filepath)
            return

        self.__start = None
        self.__objective = []        
        self.__alien = alien
        self.offsets = offsets
        self.granularity = granularity
        self.alien = alien
        self.__dimensions = [len(input_map), len(input_map[0]),len(input_map[0][0])]      
        self.__map = input_map
        for x in range(self.__dimensions[X]):
            for y in range(self.__dimensions[Y]):
                for shape in range(self.__dimensions[SHAPE]):  
                    if self.__map[x][y][shape] == START_CHAR:
                        self.__start = idxToConfig((x, y,shape), self.offsets, granularity,self.__alien)
                    elif self.__map[x][y][shape] == OBJECTIVE_CHAR:
                        self.__objective.append(idxToConfig((x, y,shape), self.offsets, granularity,self.__alien))

        if not self.__start:
            # raise SystemExit
            raise NoStartError("Maze has no start")

        if not self.__objective:
            raise NoObjectiveError("Maze has no objectives")
    
    def __getitem__(self, index):
        """Access data at index via self[index] instead of using self.__map"""
        i, j, k = index
        if 0 <= i < self.__dimensions[X] and 0 <= j < self.__dimensions[Y] and 0 <= k < self.__dimensions[SHAPE]:
            return self.__map[i][j][k]
        else:
            raise IndexError('cell index ({0}, {1}, {2}) out of range'.format(i, j, k))
    
    def readFromFile(self, path):
        """Construct a maze from file for Part 1

        Args:
            path (string): file path
        """        
        levels = []
        with open(path) as file:
            lines = []
            for line in file.readlines():
                if line:
                    if line.strip() == '#':
                        levels.append(lines)
                        lines = []
                    else:
                        lines.append([c for c in line.strip()])
                    
        
        # Stores copy of ASCII maze in self.__map as well as dimensions
        h = len(levels) # number of levels
        n = len(levels[0]) # number of rows
        m = min(map(len, levels[0])) # number of columns
        
        if any(len(line) != m for line in levels[0]):
            raise MazeError('(maze \'{0}\'): all maze rows must be the same length (shortest row has length {1})'.format(path, m))
        
        
        self.__map = np.transpose(levels, (1, 2, 0)).tolist()
        self.__dimensions = [n, m, h]

        if any(self[x] != WALL_CHAR for x in chain(
            ((    0, j, k) for j in range(m) for k in range(h)), 
            ((n - 1, j, k) for j in range(m) for k in range(h)), 
            ((i,     0, k) for i in range(n) for k in range(h)), 
            ((i, m - 1, k) for i in range(n) for k in range(h)))):
            raise MazeError('(maze \'{0}\'): maze borders must only contain `wall` cells (\'{1}\')'.format(path, WALL_CHAR))
        if n < 3 or m < 3:
            raise MazeError('(maze \'{0}\'): maze dimensions ({1}, {2}) must be at least (3, 3)'.format(path, n, m))
        
        # Checks if only 1 start, if so, stores index in self.__start
        self.__start  = None 
        for x in ((i, j, k) 
            for i in range(n) 
            for j in range(m) 
            for k in range(h) if self[i, j, k] == START_CHAR):
            if self.__start is None:
                self.__start = x
            elif type(self.__start) is int:
                self.__start += 1 
            else: 
                self.__start  = 2
        if type(self.__start) is int or self.__start is None:
            raise MazeError('(maze \'{0}\'): maze must contain exactly one `start` cell (\'{1}\') (found {2})'.format(
                path, START_CHAR, 0 if self.__start is None else self.__start))
        
        # Stores waypoint indices in self.__objective
        self.__objective = tuple((i, j, k) 
            for i in range(n) 
            for j in range(m) 
            for k in range(h) if self[i, j, k] == OBJECTIVE_CHAR)

    def getChar(self, x, y, shape, part1=False):
        """Getting underlying character at the specified coordinate

        Args:
            x (int): x
            y (int): y
            shape (int): shape idx
            part1 (bool, optional): True if used for part 1. Defaults to False.

        Returns:
            str: ASCII character to return
        """        
        if part1:
            i, j, k = x, y, shape
            return self[i, j, k]
        oldx = x
        oldy = y
        oldshape = shape
        x, y,shape = configToIdx((x,y,shape), self.offsets, self.granularity,self.alien)
        print('getting char from {} {} {}, mapped to {} {} {} and is {}'.format(oldx,oldy,oldshape,x,y,shape,self.__map[x][y][shape]))
        return self.__map[x][y][shape]

    # Returns True if the given position is the location of a wall
    def isWall(self, x, y, shape, ispart1=False):
        return self.getChar(x, y, shape, ispart1) == WALL_CHAR

    # Rturns True if the given position is the location of an objective
    def isObjective(self, x, y, shape, ispart1=False):
        return self.getChar(x, y, shape, ispart1) == OBJECTIVE_CHAR

    # Returns the start position as a tuple of (row, col, level)
    def getStart(self):
        return self.__start

    def setStart(self, start):
        self.__start = start

    # Returns the dimensions of the maze as a (num_row, num_col, level) tuple
    def getDimensions(self):
        return self.__dimensions

    # Returns the list of objective positions of the maze
    def getObjectives(self):
        return copy.deepcopy(self.__objective)

    def setObjectives(self, objectives):
        self.__objective = objectives

    def isValidMove(self, x, y, shape, part1=False):
        """Check if the agent can move into a specific coordinate

        Args:
            x (int): x
            y (int): y
            shape (int): shape idx
            part1 (bool, optional): True if used for part 1. Defaults to False.

        Returns:
            bool: True if the move is valid, False otherwise
        """        
        if part1:
            i, j, k = x, y, shape
            return i >= 0 and i < self.getDimensions()[X] and \
               j >= 0 and j < self.getDimensions()[Y] and \
               0 <= k < self.getDimensions()[SHAPE] and not self.isWall(i, j, k, True)

        old_x,old_y,old_shape = x,y,shape
        x, y,shape = configToIdx((x,y,shape), self.offsets, self.granularity, self.alien)

        return x >= 0 and x < self.getDimensions()[X] and \
               y >= 0 and y < self.getDimensions()[Y] and \
               0 <= shape < self.getDimensions()[SHAPE] and not self.isWall(old_x,old_y,old_shape)
        
    def getNeighbors(self, x, y, shape, part1=False):
        """Returns list of neighboing squares that can be moved to from the given coordinate

        Args:
            x (int): x
            y (int): y
            shape (int): shape idx
            part1 (bool, optional): True if used for part 1. Defaults to False.

        Returns:
            list: list of possible neighbors 
        """        
        self.states_explored += 1
        if part1:
            i, j, k = x, y, shape
            return tuple(x for x in (
            (x + 1, y, k),
            (i - 1, j, k),
            (i, j + 1, k),
            (i, j - 1, k),
            (i, j, k - 1),
            (i, j, k + 1)) 
            if self.isValidMove( * x, True ))

        possibleNeighbors = [
            (x + self.granularity, y,shape),
            (x - self.granularity, y,shape),
            (x, y + self.granularity,shape),
            (x, y - self.granularity,shape),
            (x,y,self.alien.get_shapes().index(shape) -1),
            (x,y,self.alien.get_shapes().index(shape) +1)            
        ]
        neighbors = []
        for a, b,c in possibleNeighbors:
            if(type(c) == int):
                if(0<= c < len(self.alien.get_shapes())):
                    c = self.alien.get_shapes()[c]
                    if(self.isValidMove(a,b,c)):
                        neighbors.append((a,b,c))
                else:
                    continue
            elif self.isValidMove(a,b,c):
                neighbors.append((a,b,c))
        return neighbors

    def saveToFile(self, filename): 
        """Save the maze to file

        Args:
            filename (string): file name

        Returns:
            bool: True if successfully saved
        """               
        outputMap = ""
        for shape in range(self.__dimensions[2]):
            for y in range(self.__dimensions[1]):
                for x in range(self.__dimensions[0]):
                    outputMap += self.__map[x][y][shape]
                outputMap += "\n"
            outputMap += "#\n"

        with open(filename, 'w') as f:
            f.write(outputMap)

        return True
            

    def isValidPath(self, path):
        """Check if the path is valid

        Args:
            path (list): path of travelled cells

        Returns:
            string: detailed description on if the path is valid
        """        
        # First, check whether it moves single hop
        for i in range(1, len(path)):
            prev = path[i-1]
            cur = path[i]
            dist = abs(prev[0]-cur[0]) + abs(prev[1]-cur[1]) #+ abs(prev[2] - cur[2])
            if dist != self.granularity:
                return "Not single hop"
            if(abs(prev[2] - cur[2]) > 1):
                return "Illegal Shape Transformation"

        # Second, check whether it is valid move
        for pos in path:
            if not self.isValidMove(pos[0], pos[1],pos[2]):
                return "Not valid move"


        # Last, check whether it ends up at one of goals
        if not path[-1] in self.__objective:
            return "Last position is not a goal state"

        return "Valid"

    def get_map(self):
        return self.__map
