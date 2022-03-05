# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Kelvin Ma (kelvinm2@illinois.edu) on 01/24/2021

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)


# Feel free to use the code below as you wish
# Initialize it with a list/tuple of objectives
# Call compute_mst_weight to get the weight of the MST with those objectives
# TODO: hint, you probably want to cache the MST value for sets of objectives you've already computed...
class MST:
    def __init__(self, objectives):
        self.elements = {key: None for key in objectives}

        # TODO: implement some distance between two objectives 
        # ... either compute the shortest path between them, or just use the manhattan distance between the objectives
        self.distances   = {
                (i, j): abs(i[0]-j[0]) + abs(i[1]-j[1])
                for i, j in self.cross(objectives)
            }
        
    # Prim's algorithm adds edges to the MST in sorted order as long as they don't create a cycle
    def compute_mst_weight(self):
        weight      = 0
        for distance, i, j in sorted((self.distances[(i, j)], i, j) for (i, j) in self.distances):
            if self.unify(i, j):
                weight += distance
        return weight

    # helper checks the root of a node, in the process flatten the path to the root
    def resolve(self, key):
        path = []
        root = key 
        while self.elements[root] is not None:
            path.append(root)
            root = self.elements[root]
        for key in path:
            self.elements[key] = root
        return root
    
    # helper checks if the two elements have the same root they are part of the same tree
    # otherwise set the root of one to the other, connecting the trees
    def unify(self, a, b):
        ra = self.resolve(a) 
        rb = self.resolve(b)
        if ra == rb:
            return False 
        else:
            self.elements[rb] = ra
            return True

    # helper that gets all pairs i,j for a list of keys
    def cross(self, keys):
        return (x for y in (((i, j) for j in keys if i < j) for i in keys) for x in y)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    cur_pos = maze.start
    bfs_go = []
    bfs_gone = {cur_pos: (None, 0)}
    for i in maze.neighbors(cur_pos[0], cur_pos[1]):
        bfs_go.append((i, cur_pos, 1))
    go_pos = bfs_go.pop(0)
    cur_pos = go_pos[0]
    while cur_pos not in maze.waypoints:
        if cur_pos in bfs_gone.keys():
            if go_pos[2] >= bfs_gone[cur_pos][1]:
                go_pos = bfs_go.pop(0)
                cur_pos = go_pos[0]
        else:
            bfs_gone[cur_pos] = (go_pos[1], go_pos[2])
            neighbors = maze.neighbors(cur_pos[0], cur_pos[1])
            for i in neighbors:
                bfs_go.append((i, cur_pos, go_pos[2] + 1))
            go_pos = bfs_go.pop(0)
            cur_pos = go_pos[0]
    result = [cur_pos]
    cur_par = go_pos[1]
    while cur_par != maze.start:
        result.insert(0, cur_par)
        explored_tuple = bfs_gone[cur_par]
        cur_par = explored_tuple[0]
    result.insert(0, cur_par)
    return result

def manhattan(pos1,pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

import heapq

def astar_single(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """

    queue = []
    heapq.heapify(queue)
    dis = {}
    ast_gone = {}
    cur_pos = maze.start
    dis[maze.start] = (-1,-1)
    ast_gone[maze.start] = 1
    while cur_pos not in maze.waypoints:
        for i in maze.neighbors(cur_pos[0], cur_pos[1]):
            if i not in ast_gone:
                dis[i] = cur_pos
                distance = manhattan(i,maze.waypoints[0]) + ast_gone[cur_pos]
                heapq.heappush(queue, (distance, i))
                ast_gone[i] = 1 + ast_gone[cur_pos]
        cur_pos = heapq.heappop(queue)[1]
    result = []
    while(cur_pos != (-1,-1)):
        result.insert(0,cur_pos)
        cur_pos = dis[cur_pos]
    return result

def get_min(p,q):
    list1 = []
    if len(q) == 0:
        return 0
    for i in q:
        list1.append(manhattan(p,i))
    result = min(list1)
    return result

def mst_dis(t):
    mstt = MST(t)
    return mstt.compute_mst_weight()

def astar_multiple(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    ast_go = []
    ast_go.append((0, (maze.start,tuple(maze.waypoints))))
    ast_close = {(maze.start,tuple(maze.waypoints)):0}
    ast_g = {(maze.start, tuple(maze.waypoints)):0}
    ast_f = {(maze.start, tuple(maze.waypoints)):0}
    ast_gone = set()
    cur_pos = (maze.start, tuple(maze.waypoints))
    mst_value = mst_dis(tuple(maze.waypoints))
    dic_mst_value = {}
    dic_mst_value[tuple(maze.waypoints)] = mst_value
    while (len(ast_go) > 0):
        cur_pos = heapq.heappop(ast_go)[1]
        if len(cur_pos[1]) == 0:
            break
        ast_gone.add(cur_pos)
        for i in maze.neighbors(cur_pos[0][0], cur_pos[0][1]):
            tuple_nei = (i, tuple(set(cur_pos[1]) - {i}))
            if tuple_nei[1] not in dic_mst_value.keys():
                dic_mst_value[tuple_nei[1]] = MST(tuple_nei[1]).compute_mst_weight()
            if tuple_nei not in ast_gone:
                total_dis = get_min(i, tuple_nei[1]) + dic_mst_value[tuple_nei[1]] + ast_g[cur_pos] + 1
                if (tuple_nei in ast_f.keys()) and total_dis < ast_f.get(tuple_nei):
                    ast_go.remove((ast_f[tuple_nei], tuple_nei))
                    ast_f[tuple_nei] = total_dis
                    ast_g[tuple_nei] = ast_g[cur_pos] + 1
                    ast_close[tuple_nei] = cur_pos
                    ast_go.append((ast_f[tuple_nei], tuple_nei))
                    heapq.heapify(ast_go)
                if tuple_nei not in ast_f.keys():
                    ast_f[tuple_nei] = total_dis
                    ast_g[tuple_nei] = ast_g[cur_pos] + 1
                    ast_close[tuple_nei] = cur_pos
                    heapq.heappush(ast_go, (ast_f[tuple_nei], tuple_nei))
    result = []
    while (cur_pos != 0):
        result.insert(0,cur_pos[0])
        cur_pos = ast_close[cur_pos]
    return result


def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    w = 2.66
    ast_go = []
    ast_go.append((0, (maze.start, tuple(maze.waypoints))))
    ast_close = {(maze.start, tuple(maze.waypoints)): 0}
    ast_g = {(maze.start, tuple(maze.waypoints)): 0}
    ast_f = {(maze.start, tuple(maze.waypoints)): 0}
    ast_gone = set()
    cur_pos = (maze.start, tuple(maze.waypoints))
    mst_value = mst_dis(tuple(maze.waypoints))
    dic_mst_value = {}
    dic_mst_value[tuple(maze.waypoints)] = mst_value
    while (len(ast_go) > 0):
        cur_pos = heapq.heappop(ast_go)[1]
        if len(cur_pos[1]) == 0:
            break
        ast_gone.add(cur_pos)
        for i in maze.neighbors(cur_pos[0][0], cur_pos[0][1]):
            tuple_nei = (i, tuple(set(cur_pos[1]) - {i}))
            if tuple_nei[1] not in dic_mst_value.keys():
                dic_mst_value[tuple_nei[1]] = MST(tuple_nei[1]).compute_mst_weight()
            if tuple_nei not in ast_gone:
                total_dis = w*(get_min(i, tuple_nei[1]) + dic_mst_value[tuple_nei[1]]) + ast_g[cur_pos] + 1
                if (tuple_nei in ast_f.keys()) and total_dis < ast_f.get(tuple_nei):
                    ast_go.remove((ast_f[tuple_nei], tuple_nei))
                    ast_f[tuple_nei] = total_dis
                    ast_g[tuple_nei] = ast_g[cur_pos] + 1
                    ast_close[tuple_nei] = cur_pos
                    ast_go.append((ast_f[tuple_nei], tuple_nei))
                    heapq.heapify(ast_go)
                if tuple_nei not in ast_f.keys():
                    ast_f[tuple_nei] = total_dis
                    ast_g[tuple_nei] = ast_g[cur_pos] + 1
                    ast_close[tuple_nei] = cur_pos
                    heapq.heappush(ast_go, (ast_f[tuple_nei], tuple_nei))
    result = []
    while (cur_pos != 0):
        result.insert(0, cur_pos[0])
        cur_pos = ast_close[cur_pos]
    return result

            
