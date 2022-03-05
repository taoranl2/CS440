import numpy as np
import utils

class Agent:    
    def __init__(self, actions, Ne=40, C=40, gamma=0.7):
        # HINT: You should be utilizing all of these
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma
        self.reset()
        # Create the Q Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()
        
    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path,self.Q)
        utils.save(model_path.replace('.npy', '_N.npy'), self.N)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        # HINT: These variables should be used for bookkeeping to store information across time-steps
        # For example, how do we know when a food pellet has been eaten if all we get from the environment
        # is the current number of points? In addition, Q-updates requires knowledge of the previously taken
        # state and action, in addition to the current state from the environment. Use these variables
        # to store this kind of information.
        self.points = 0
        self.s = None
        self.a = None
    
    def act(self, environment, points, dead):
        '''
        :param environment: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] to be converted to a state.
        All of these are just numbers, except for snake_body, which is a list of (x,y) positions 
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: chosen action between utils.UP, utils.DOWN, utils.LEFT, utils.RIGHT

        Tip: you need to discretize the environment to the state space defined on the webpage first
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the playable board)
        '''
        s_prime = self.generate_state(environment)

        # TODO: write your function here

        if not self._train:
            temp = self.Q[s_prime][3] - 1
            for i in range(3, -1, -1):
                q = self.Q[s_prime][i]
                if q > temp:
                    temp = q
                    self.a = i
        else:
            if self.a != None:
                if self.s != None:
                    if dead:
                        r = -1
                    elif points == self.points + 1:
                        r = 1
                    else:
                        r = -0.1
                    temp = self.Q[s_prime][3] - 1
                    for i in range(3, -1, -1):
                        q = self.Q[s_prime][i]
                        if q > temp:
                            temp = q
                    self.N[self.s][self.a] += 1
                    self.Q[self.s][self.a] += (self.C / (self.N[self.s][self.a] + self.C)) * (self.gamma * temp + r - self.Q[self.s][self.a])
            if dead:
                self.reset()
                return 1
            self.s = s_prime
            self.points = points
            temp = self.Q[s_prime][3] - 1
            for i in range(3, -1, -1):
                if self.N[s_prime][i] < self.Ne:
                    p = 1
                else:
                    p = self.Q[s_prime][i]
                if p > temp:
                    temp = p
                    self.a = i

        return self.a


    def generate_state(self, environment):
        # TODO: Implement this helper function that generates a state given an environment 
        cur_state = [0, 0, 0, 0, 0, 0, 0, 0]
        if environment[0] < environment[3]:
            cur_state[0] = 2
        if environment[0] > environment[3]:
            cur_state[0] = 1
        if environment[0] == utils.GRID_SIZE:
            cur_state[2] = 1
        if environment[0] == (utils.DISPLAY_SIZE - 2 * utils.GRID_SIZE):
            cur_state[2] = 2
        if environment[0] < utils.GRID_SIZE:
            cur_state[2] = 0
            cur_state[3] = 0
        if environment[0] > (utils.DISPLAY_SIZE - 2 * utils.GRID_SIZE):
            cur_state[2] = 0
            cur_state[3] = 0
        if environment[1] < utils.GRID_SIZE:
            cur_state[2] = 0
            cur_state[3] = 0
        if environment[1] > (utils.DISPLAY_SIZE - 2 * utils.GRID_SIZE):
            cur_state[2] = 0
            cur_state[3] = 0
        if environment[1] > environment[4]:
            cur_state[1] = 1
        if environment[1] < environment[4]:
            cur_state[1] = 2
        if environment[1] == utils.GRID_SIZE:
            cur_state[3] = 1
        if (environment[0] + utils.GRID_SIZE, environment[1]) in environment[2]:
            cur_state[7] = 1
        if (environment[0] - utils.GRID_SIZE, environment[1]) in environment[2]:
            cur_state[6] = 1
        if environment[1] == (utils.DISPLAY_SIZE - 2 * utils.GRID_SIZE):
            cur_state[3] = 2
        if (environment[0], environment[1] + utils.GRID_SIZE) in environment[2]:
            cur_state[5] = 1
        if (environment[0], environment[1] - utils.GRID_SIZE) in environment[2]:
            cur_state[4] = 1
        return tuple(cur_state)