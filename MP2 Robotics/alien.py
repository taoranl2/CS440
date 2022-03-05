# alien.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by James Gao (jamesjg2@illinois.edu) on 9/03/2021
import numpy as np
"""
This file contains code to represent the alien that we are using as our principal actor for MP2
"""

class Alien:
    """The Meaty Alien that will be navigating our map

        The alien has two forms that are represented with geometric shapes:

        Form 1 (Meatball):
            A circle with a fixed radius.

        Form 2 (Sausage):
            An oblong (sausage shape). This is represented as a line segment with a fixed length, and 
            The width of the alien's entire sausage body is the diameter of these circles.
    """

    def __init__(self, centroid, lengths,widths,shapes,init_shape,window):
        """Initializes the Alien instance

            Args:
                centroid: the (x, y) coordinate of the alien's center of mass
                lengths (list): lengths of the line segment in each shape (line length, 0, line length) for (Horizontal,Ball,Vertical)
                shapes (list): possible shapes that the alien can have, for this MP, it will always be ('Horizontal','Ball','Vertical')
                init_shape (str):  The initial shape of the alien (must exist in shapes)
                window (int, int): The (width, height) of the window that our alien will be running in
        """

        self.__centroid = centroid 
        self.__widths = widths 
        self.__lengths = lengths
        self.__shapes = shapes 
        self.__shape = init_shape
        self.__shapenum = self.__shapes.index(self.__shape)
        self.__limits = [[0,window[0]],[0,window[1]],[0,len(self.__shapes)]]

    # Returns a tuple with the (x,y) coordinates of the alien's head and tail ((x_head,y_head),(x_tail,y_tail))
    def get_head_and_tail(self):
        """Returns (head, tail). head and tail are (x,y) coordinates where the alien's head and tail are located.
        """
        if(self.__shape == 'Horizontal'):
            head = (self.__centroid[0] + self.__lengths[self.__shapenum]/2,self.__centroid[1])
            tail = (self.__centroid[0] - self.__lengths[self.__shapenum]/2,self.__centroid[1])
        elif(self.__shape == 'Vertical'):
            head = (self.__centroid[0],self.__centroid[1] - self.__lengths[self.__shapenum]/2 )
            tail = (self.__centroid[0],self.__centroid[1] + self.__lengths[self.__shapenum]/2 )
        elif(self.__shape == 'Ball'):
            head = (self.__centroid[0],self.__centroid[1])
            tail = head
        return (head,tail)

    def get_centroid(self):
        """Returns the centroid of the alien
        """
        return self.__centroid

    def get_length(self):
        """Returns length of the line segment in the current form of the alien
        """
        return self.__lengths[self.__shapenum]

    def get_width(self):
        """Returns the radius of the current shape
        """
        return self.__widths[self.__shapenum]/2

    def is_circle(self):
        """Returns whether the alien is in circle or oblong form. True is alien is in circle form, False if oblong form.
        """
        return self.__shape == 'Ball'

    def set_alien_pos(self, pos):
        """Sets the alien's centroid position to the specified pos argument. 
            Args:
                pos: The (x,y) coordinate position we want to place the alien's centroid 
        """
        self.__centroid = pos

    def set_alien_shape(self,shape):
        """Sets the alien's shape while maintaining the center of mass
            Args: 
                shape (str): The shape we are transforming the alien into. Must be one of 'Horizontal', 'Ball', Vertical
        """
        if((np.abs(self.__shapes.index(shape)-self.__shapenum) <= 1) and (shape in self.__shapes)):
            self.__shape = shape
            self.__shapenum = self.__shapes.index(self.__shape)
        else:
            # raise exception for illegal transformation?
            pass

    def set_alien_config(self,config):
        """Set the alien configuration
            Args:
                config: configuration of the alien in the format [x, y, shape]
        """
        self.__centroid = [config[0],config[1]]
        self.__shape = config[2]
        self.__shapenum = self.__shapes.index(self.__shape)
    
    def get_shape_idx(self):
        """Returns the shape index of our alien
        """
        return self.__shapenum

    def get_alien_limits(self):
        """Returns the limits of the 3D movement space for the alien
        """
        return self.__limits

    def get_config(self):
        """Returns the shape and position configuration of our alien in the form [x, y, shape]
        """
        return [self.__centroid[0],self.__centroid[1],self.__shape]

    def get_shapes(self):
        """Returns the possible shapes the alien can transform into
        """
        return self.__shapes
    
    def get_shape(self):
        """Returns the current shape of the alien
        """
        return self.__shape
