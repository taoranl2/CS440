# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by James Gao (jamesjg2@illinois.edu) on 9/03/2021
# Inspired by work done by Jongdeog Lee (jlee700@illinois.edu)

"""
This file contains geometry functions necessary for solving problems in MP2
"""

import math
import numpy as np
from alien import Alien


def if_centroid_on_line(walli, pointi):
    #walli(startx, starty, endx, endy)
    #pointi(x,y)
    a = ((walli[2]-walli[0])**2+(walli[3]-walli[1])**2)**0.5
    b = ((walli[0]-pointi[0])**2+(walli[1]-pointi[1])**2)**0.5
    c = ((walli[2]-pointi[0])**2+(walli[3]-pointi[1])**2)**0.5
    cosb = a**2+c**2-b**2
    cosc = a**2+b**2-c**2
    if cosb < 0 or cosc < 0:
        return False
    else:
        return True

def point_line_dis(walli,pointi):
    a1 = walli[0]
    b1 = walli[1]
    a2 = walli[2]
    b2 = walli[3]
    x0 = pointi[0]
    y0 = pointi[1]
    if if_centroid_on_line(walli, pointi):
        if a2 == a1:
            dis = abs(x0 - a1)
        else:
            k = (b2 - b1) / (a2 - a1)
            m = (a2 * b1 - a1 * b2) / (a2 - a1)
            dis = abs(k * x0 - y0 + m) / ((k ** 2 + 1) ** 0.5)
    else:
        dis1 = ((a1 - x0) ** 2 + (b1 - y0) ** 2) ** 0.5
        dis2 = ((a2 - x0) ** 2 + (b2 - y0) ** 2) ** 0.5
        dis = min(dis1, dis2)
    return dis


def does_ball_touch_wall(alien, walls,granularity):
    center = alien.get_centroid()
    r = alien.get_width()
    dis_list = []
    for wall in walls:
        dis = point_line_dis(wall, center)
        dis_list.append(dis)
    for i in dis_list:
        if i-r < granularity/(2**0.5) or np.isclose(i-r, granularity/(2**0.5)):
            return True
    return False

#Determine whether two lines cross each other
def if_line_cross(lineA, lineB):
    a1 = (lineA[0], lineA[1])
    a2 = (lineA[2], lineA[3])
    b1 = (lineB[0], lineB[1])
    b2 = (lineB[2], lineB[3])

    if a1[0] == a2[0]:
        if (b1[0] - a1[0]) * (b2[0] - a2[0]) >= 0:
            return False
    else:
        k_a = (a1[1] - a2[1]) / (a1[0] - a2[0])
        bA = (a1[0] * a2[1] - a1[1] * a2[0]) / (a1[0] - a2[0])
        if (k_a * b1[0] - b1[1] + bA) * (k_a * b2[0] - b2[1] + bA) >= 0:
            return False

    if b1[0] == b2[0]:
        if (a1[0] - b1[0]) * (a2[0] - b2[0]) >= 0:
            return False
    else:
        k_b = (b1[1] - b2[1]) / (b1[0] - b2[0])
        b_b = (b1[0] * b2[1] - b1[1] * b2[0]) / (b1[0] - b2[0])
        if (k_b * a1[0] - a1[1] + b_b) * (k_b * a2[0] - a2[1] + b_b) >= 0:
            return False
    return True


def does_line_touch_wall(alien, walls,granularity):
    r = alien.get_width()
    alien_head = alien.get_head_and_tail()[0]
    alien_tail = alien.get_head_and_tail()[1]
    line_alien = (alien_head[0], alien_head[1], alien_tail[0], alien_tail[1])
    for wall in walls:
        if if_line_cross(line_alien, wall):
            return True
        else:
            dis1 = point_line_dis(wall, alien_head)
            dis2 = point_line_dis(wall, alien_tail)
            dis3 = point_line_dis(line_alien,(wall[0], wall[1]))
            dis4 = point_line_dis(line_alien,(wall[2], wall[3]))
            dis = min(dis1, dis2, dis3, dis4)
            if dis -r < granularity/(2**0.5) or np.isclose(dis-r, granularity/(2**0.5)):
                return True
    return False


def does_alien_touch_wall(alien, walls, granularity):
    """Determine whether the alien touches a wall

        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            walls (list): List of endpoints of line segments that comprise the walls in the maze in the format [(startx, starty, endx, endx), ...]
            granularity (int): The granularity of the map

        Return:
            True if touched, False if not
    """
    if alien.get_shape() == "Ball":
        return does_ball_touch_wall(alien, walls,granularity)
    else:
        return does_line_touch_wall(alien, walls,granularity)

def does_ball_touch_goal(alien, goals):
    """Determine whether the ball alien touches a goal

          Args:
              alien (Alien): Instance of Alien class that will be navigating our map
              goals (list): x, y coordinate and radius of goals in the format [(x, y, r), ...]. There can be multiple goals

          Return:
              True if a goal is touched, False if not.
      """
    center = alien.get_centroid()
    r_a = alien.get_width()
    for goal in goals:
        dis = ((center[0]-goal[0])**2+(center[1]-goal[1])**2)**0.5
        if (dis < r_a + goal[2]) or np.isclose(dis, r_a + goal[2]):
            return True
    return False

def does_line_touch_goal(alien, goals):
    """Determine whether the horizontal or vertical alien touches a goal

        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            goals (list): x, y coordinate and radius of goals in the format [(x, y, r), ...]. There can be multiple goals

        Return:
            True if a goal is touched, False if not.
    """
    alien_head = alien.get_head_and_tail()[0]
    alien_tail = alien.get_head_and_tail()[1]
    line_alien = (alien_head[0], alien_head[1], alien_tail[0], alien_tail[1])
    r_a = alien.get_width()
    for goal in goals:
        x0 = goal[0]
        y0 = goal[1]
        dis = point_line_dis(line_alien, (x0,y0))
        if (dis < r_a + goal[2]) or np.isclose(dis, r_a + goal[2]):
            return True
    return False

def does_alien_touch_goal(alien, goals):
    """Determine whether the alien touches a goal
        
        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            goals (list): x, y coordinate and radius of goals in the format [(x, y, r), ...]. There can be multiple goals
        
        Return:
            True if a goal is touched, False if not.
    """
    if alien.get_shape() == "Ball":
        return does_ball_touch_goal(alien, goals)
    else:
        return does_line_touch_goal(alien, goals)

def is_alien_within_window(alien, window,granularity):
    """Determine whether the alien stays within the window
        
        Args:
            alien (Alien): Alien instance
            window (tuple): (width, height) of the window
            granularity (int): The granularity of the map
    """
    height = window[1]
    width = window[0]
    r_a = alien.get_width()
    for i in alien.get_head_and_tail():
        if i[0] + r_a >= width or i[0] - r_a <= 0 or i[1] + r_a >= height or i[1] - r_a <= 0:
            return False
    return True

if __name__ == '__main__':
    #Walls, goals, and aliens taken from Test1 map
    walls =   [(0,100,100,100),  
                (0,140,100,140),
                (100,100,140,110),
                (100,140,140,130),
                (140,110,175,70),
                (140,130,200,130),
                (200,130,200,10),
                (200,10,140,10),
                (175,70,140,70),
                (140,70,130,55),
                (140,10,130,25),
                (130,55,90,55),
                (130,25,90,25),
                (90,55,90,25)]
    goals = [(110, 40, 10)]
    window = (220, 200)

    def test_helper(alien : Alien, position, truths):
        alien.set_alien_pos(position)
        config = alien.get_config()

        touch_wall_result = does_alien_touch_wall(alien, walls, 0) 
        touch_goal_result = does_alien_touch_goal(alien, goals)
        in_window_result = is_alien_within_window(alien, window, 0)

        assert touch_wall_result == truths[0], f'does_alien_touch_wall(alien, walls) with alien config {config} returns {touch_wall_result}, expected: {truths[0]}'
        assert touch_goal_result == truths[1], f'does_alien_touch_goal(alien, goals) with alien config {config} returns {touch_goal_result}, expected: {truths[1]}'
        assert in_window_result == truths[2], f'is_alien_within_window(alien, window) with alien config {config} returns {in_window_result}, expected: {truths[2]}'

    #Initialize Aliens and perform simple sanity check. 
    alien_ball = Alien((30,120), [40, 0, 40], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Ball', window)
    test_helper(alien_ball, alien_ball.get_centroid(), (False, False, True))

    alien_horz = Alien((30,120), [40, 0, 40], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Horizontal', window)	
    test_helper(alien_horz, alien_horz.get_centroid(), (False, False, True))

    alien_vert = Alien((30,120), [40, 0, 40], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Vertical', window)	
    test_helper(alien_vert, alien_vert.get_centroid(), (True, False, True))

    edge_horz_alien = Alien((50, 100), [100, 0, 100], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Horizontal', window)
    edge_vert_alien = Alien((200, 70), [120, 0, 120], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Vertical', window)

    alien_positions = [
                        #Sanity Check
                        (0, 100),

                        #Testing window boundary checks
                        (25.6, 25.6),
                        (25.5, 25.5),
                        (194.4, 174.4),
                        (194.5, 174.5),

                        #Testing wall collisions
                        (30, 112),
                        (30, 113),
                        (30, 105.5),
                        (30, 105.6), # Very close edge case
                        (30, 135),
                        (140, 120),
                        (187.5, 70), # Another very close corner case, right on corner
                        
                        #Testing goal collisions
                        (110, 40),
                        (145.5, 40), # Horizontal tangent to goal
                        (110, 62.5), # ball tangent to goal
                        
                        #Test parallel line oblong line segment and wall
                        (50, 100),
                        (200, 100),
                        (205.5, 100) #Out of bounds
                    ]

    #Truths are a list of tuples that we will compare to function calls in the form (does_alien_touch_wall, does_alien_touch_goal, is_alien_within_window)
    alien_ball_truths = [
                            (True, False, False),
                            (False, False, True),
                            (False, False, True),
                            (False, False, True),
                            (False, False, True),
                            (True, False, True),
                            (False, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (False, True, True),
                            (False, False, True),
                            (True, True, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True)
                        ]
    alien_horz_truths = [
                            (True, False, False),
                            (False, False, True),
                            (False, False, False),
                            (False, False, True),
                            (False, False, False),
                            (False, False, True),
                            (False, False, True),
                            (True, False, True),
                            (False, False, True),
                            (True, False, True),
                            (False, False, True),
                            (True, False, True),
                            (True, True, True),
                            (False, True, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, False),
                            (True, False, False)
                        ]
    alien_vert_truths = [
                            (True, False, False),
                            (False, False, True),
                            (False, False, False),
                            (False, False, True),
                            (False, False, False),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (False, False, True),
                            (True, True, True),
                            (False, False, True),
                            (True, True, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True)
                        ]

    for i in range(len(alien_positions)):
        test_helper(alien_ball, alien_positions[i], alien_ball_truths[i])
        test_helper(alien_horz, alien_positions[i], alien_horz_truths[i])
        test_helper(alien_vert, alien_positions[i], alien_vert_truths[i])

    #Edge case coincide line endpoints
    test_helper(edge_horz_alien, edge_horz_alien.get_centroid(), (True, False, False))
    test_helper(edge_horz_alien, (110,55), (True, True, True))
    test_helper(edge_vert_alien, edge_vert_alien.get_centroid(), (True, False, True))


    print("Geometry tests passed\n")