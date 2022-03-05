# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush

def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def bfs(maze, ispart1=False):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None.

    Args:
        maze: Maze instance from maze.py
        ispart1: pass this variable when you use functions such as getNeighbors and isObjective. DO NOT MODIFY THIS
    """
    queue = deque()
    path = deque()
    parent = {}
    gone = set()

    queue.append(maze.getStart())
    gone.add(maze.getStart())

    while len(queue) != 0:
        cur_pos = queue.popleft()
        if maze.isObjective(cur_pos[0],cur_pos[1],cur_pos[2],ispart1) == True:
            path.appendleft(cur_pos)
            while path[0] != maze.getStart():
                path.appendleft((parent[cur_pos]))
                cur_pos = parent[cur_pos]
            return path
        for i in maze.getNeighbors(cur_pos[0],cur_pos[1],cur_pos[2],ispart1):
            if i not in gone:
                parent[i] = cur_pos
                queue.append(i)
                gone.add(i)