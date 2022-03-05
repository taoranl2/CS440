# mp2.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/04/2018

"""
This file contains the main application that is run for this MP.
"""

import pygame
import sys
import argparse
import configparser
import copy

from pygame.locals import *
from alien import Alien
from transform import transformToMaze
from search import search
from const import *
from util import *
from geometry import *
import time

class Application:

	def __init__(self, configfile, map_name, human=True, fps=DEFAULT_FPS):
		self.running = False
		self.displaySurface = None
		self.config = configparser.ConfigParser()
		self.config.read(configfile)
		self.fps = fps
		self.__human = human
		self.clock = pygame.time.Clock()   
		self.trajectory = []   
		lims = eval(self.config.get(map_name, 'Window'))
		# print(lims)
		self.alien_limits = [(0,int(lims[0])),(0,int(lims[1]))]
		# Parse config file
		self.windowTitle = "CS440 MP2 Shapeshifting Alien"
		self.window = eval(self.config.get(map_name, 'Window'))
		self.centroid = eval(self.config.get(map_name, 'StartPoint'))
		self.widths = eval(self.config.get(map_name, 'Widths'))
		self.alien_shape = 'Ball'
		self.lengths = eval(self.config.get(map_name, 'Lengths'))
		self.alien_shapes = ['Horizontal','Ball','Vertical']
		self.obstacles = eval(self.config.get(map_name, 'Obstacles'))
		boundary = [(0,0,0,lims[1]),(0,0,lims[0],0),(lims[0],0,lims[0],lims[1]),(0,lims[1],lims[0],lims[1])]
		self.obstacles.extend(boundary)
		self.goals = eval(self.config.get(map_name, 'Goals'))
		self.alien_color = BLACK
		self.alien = Alien(self.centroid,self.lengths,self.widths,self.alien_shapes,self.alien_shape,self.window)

	# Initializes the pygame context and certain properties of the maze
	def initialize(self):
		
		pygame.init()
		self.font = pygame.font.Font('freesansbold.ttf', 10)
		self.displaySurface = pygame.display.set_mode((self.window[0], self.window[1]), pygame.HWSURFACE)
		self.displaySurface.fill(WHITE)
		pygame.display.flip()
		pygame.display.set_caption(self.windowTitle)
		self.running = True

	def get_alien_color(self):
		if does_alien_touch_wall(self.alien, self.obstacles,self.granularity) or not is_alien_within_window(self.alien, self.window,self.granularity):
			self.alien_color = RED
		elif does_alien_touch_goal(self.alien,self.goals):
			self.alien_color = GREEN
		else: 
			self.alien_color = BLACK
	# Once the application is initiated, execute is in charge of drawing the game and dealing with the game loop
	def execute(self, searchMethod, granularity, trajectory, saveMaze):    
		self.granularity = granularity    
		self.initialize()
		if not self.running:
			print("Program init failed")
			raise SystemExit
		
		# currAngle = [0, 0, 0]
		# for i in range(len(self.arm.getArmAngle())):
		#     currAngle[i] = self.arm.getArmAngle()[i]
		self.gameLoop()        

		if not self.__human:
			print("Transforming a map configuration to a maze...")
			maze = transformToMaze(self.alien, self.goals, self.obstacles, self.window, granularity)
			print("Done!")
			print("Searching the path...")
			path = search(maze, searchMethod)
			if path is None:
				print("No path found!")
			else:
				self.trajectory = path
				self.gameLoop()
				print("Done!")
				if saveMaze and not self.__human:
					maze.saveToFile(saveMaze)
				self.drawTrajectory(final = True)

		while self.running:
			pygame.event.pump()            
			keys = pygame.key.get_pressed()
			
			if (keys[K_ESCAPE]):
				self.running = False                

			if self.__human:                
				# alpha, beta, gamma = currAngle     
				old_config = self.alien.get_centroid()
				x,y = self.alien.get_centroid()
				shape = self.alien_shapes.index(self.alien.get_shape())
				if (keys[K_a]):                    
					x -= granularity if isValueInBetween(self.alien_limits[X], x-granularity) else 0
				# move right
				elif (keys[K_d]):                    
					x += granularity if isValueInBetween(self.alien_limits[X], x+granularity) else 0
				#move down 
				elif (keys[K_s]):                    
					y += granularity if isValueInBetween(self.alien_limits[Y], y+granularity) else 0
				# move up
				elif (keys[K_w]):                    
					y -= granularity if isValueInBetween(self.alien_limits[Y], y-granularity) else 0
				# changes shape forward
				elif (keys[K_q]):                    
					shape = self.alien_shapes[shape+1] if isValueInBetween([0,len(self.alien_shapes)-1], shape+1) else self.alien_shapes[shape]
					self.alien.set_alien_shape(shape)
					#debounce
					time.sleep(0.1)
				# changes shape backward
				elif (keys[K_e]):                    
					shape = self.alien_shapes[shape-1] if isValueInBetween([0,len(self.alien_shapes)-1], shape-1) else self.alien_shapes[shape]
					self.alien.set_alien_shape(shape)
					#debounce
					time.sleep(0.1)

				self.alien.set_alien_pos([x,y])
				self.get_alien_color()


				# self.arm.setArmAngle(newAngle)
				self.gameLoop()
				# currAngle = copy.deepcopy(newAngle)

				# if doesArmTipTouchGoals(armEnd, self.goals):
				#     self.gameLoop()
				#     print("SUCCESS")
				#     raise SystemExit


		if saveMaze and not self.__human:
			maze.saveToFile(saveMaze)
			

	def gameLoop(self):


		self.clock.tick(self.fps)


		
		self.displaySurface.fill(WHITE)

		# create a text surface object,
		# on which text is drawn on it.
		text = self.font.render('({},{})'.format(*self.alien.get_centroid()), True, BLACK, WHITE)
		
		# create a rectangular object for the
		# text surface object
		textRect = text.get_rect()
		
		# set the center of the rectangular object.
		textRect.center = (self.window[0]-25,self.window[1]-10)

		self.displaySurface.blit(text, textRect)
		self.drawTrajectory()
		self.drawAlien()
		self.drawObstacles()
		self.drawGoal()
		pygame.display.flip()
	  

	def drawTrajectory(self,final = False):
		cnt = 1
		if final:
			while(True):
				for config in self.trajectory: 
					pygame.event.pump()            
					keys = pygame.key.get_pressed()
					if(keys[K_ESCAPE]):
						pygame.quit()
						sys.exit()
					self.alien.set_alien_config(config)
					self.get_alien_color()
					self.gameLoop()
					time.sleep(0.05)
				time.sleep(2)


	def drawAlien(self):
		self.alien_shape = self.alien.get_shape()
		shape_idx = self.alien_shapes.index(self.alien_shape)
		self.centroid = self.alien.get_centroid()
		if(self.alien_shape == 'Horizontal'):
			head = (self.centroid[0] + self.lengths[shape_idx]/2, self.centroid[1])
			tail = (self.centroid[0] - self.lengths[shape_idx]/2, self.centroid[1])
		elif(self.alien_shape == 'Vertical'):
			head = (self.centroid[0], self.centroid[1] + self.lengths[shape_idx]/2)
			tail = (self.centroid[0], self.centroid[1] - self.lengths[shape_idx]/2)
		elif(self.alien_shape == 'Ball'):
			head = (self.centroid[0],self.centroid[1])
			tail = (self.centroid[0],self.centroid[1])
		pygame.draw.line(self.displaySurface,self.alien_color,head,tail,self.widths[shape_idx])
		pygame.draw.circle(self.displaySurface,self.alien_color,head,self.widths[shape_idx]/2)
		pygame.draw.circle(self.displaySurface,self.alien_color,tail,self.widths[shape_idx]/2)

			



	def drawObstacles(self):
		for obstacle in self.obstacles:
			pygame.draw.line(self.displaySurface, BLACK, (obstacle[0], obstacle[1]), (obstacle[2],obstacle[3]))

	def drawGoal(self):
		for goal in self.goals:
			pygame.draw.circle(self.displaySurface, BLUE, (goal[0], goal[1]), goal[2])



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='CS440 MP2 Robotic Arm')
	
	parser.add_argument('--config', dest="configfile", type=str, default = "test_config.txt",
						help='configuration filename - default BasicMap')
	parser.add_argument('--map', dest="map_name", type=str, default = "BasicMap",
						help='configuration filename - default BasicMap')
	parser.add_argument('--method', dest="search", type=str, default = "bfs", 
						choices = ["bfs"],
						help='search method - default bfs')
	parser.add_argument('--human', default = False, action = "store_true",
						help='flag for human playable - default False')
	parser.add_argument('--fps', dest="fps", type=int, default = DEFAULT_FPS,
						help='fps for the display - default '+str(DEFAULT_FPS))
	parser.add_argument('--granularity', dest="granularity", type=int, default = DEFAULT_GRANULARITY,
						help='degree granularity - default '+str(DEFAULT_GRANULARITY))
	parser.add_argument('--trajectory', dest="trajectory", type=int, default = 0, 
						help='leave footprint of rotation trajectory in every x moves - default 0')
	parser.add_argument('--save-maze', dest="saveMaze", type=str, default = None, 
						help='save the contructed maze to maze file - default not saved')
	
	args = parser.parse_args()
	app = Application(args.configfile, args.map_name, args.human, args.fps)
	app.execute(args.search, args.granularity, args.trajectory, args.saveMaze)
