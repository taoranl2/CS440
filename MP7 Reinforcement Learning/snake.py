import random
import pygame
import utils

class SnakeEnv:
    def __init__(self, snake_head_x, snake_head_y, food_x, food_y):
        self.game = Snake(snake_head_x, snake_head_y, food_x, food_y)
        self.render = False

    def get_actions(self):
        return self.game.get_actions()

    def reset(self):
        return self.game.reset()
    
    def get_points(self):
        return self.game.get_points()

    def get_environment(self):
        return self.game.get_environment()

    def step(self, action):
        environment, points, dead = self.game.step(action)
        if self.render:
            self.draw(environment, points, dead)
        return environment, points, dead

    def draw(self, environment, points, dead):
        snake_head_x, snake_head_y, snake_body, food_x, food_y = environment
        self.display.fill(utils.BLUE)    
        pygame.draw.rect( self.display, utils.BLACK,
                [
                    utils.GRID_SIZE,
                    utils.GRID_SIZE,
                    utils.DISPLAY_SIZE - utils.GRID_SIZE * 2,
                    utils.DISPLAY_SIZE - utils.GRID_SIZE * 2
                ])

        # Draw snake head
        pygame.draw.rect(
                    self.display, 
                    utils.GREEN,
                    [
                        snake_head_x,
                        snake_head_y,
                        utils.GRID_SIZE,
                        utils.GRID_SIZE
                    ],
                    3
                )

        # Draw snake body
        for seg in snake_body:
            pygame.draw.rect(
                self.display, 
                utils.GREEN,
                [
                    seg[0],
                    seg[1],
                    utils.GRID_SIZE,
                    utils.GRID_SIZE,
                ],
                1
            )

        # Draw food
        pygame.draw.rect(
                    self.display, 
                    utils.RED,
                    [
                        food_x,
                        food_y,
                        utils.GRID_SIZE,
                        utils.GRID_SIZE
                    ]
                )

        text_surface = self.font.render("Points: " + str(points), True, utils.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = ((280),(25))
        self.display.blit(text_surface, text_rect)
        pygame.display.flip()
        if dead:
            # slow clock if dead
            self.clock.tick(1)
        else:
            self.clock.tick(5)

        return 

    def display(self):
        pygame.init()
        pygame.display.set_caption('MP4: Snake')
        self.clock = pygame.time.Clock()
        pygame.font.init()

        self.font = pygame.font.Font(pygame.font.get_default_font(), 15)
        self.display = pygame.display.set_mode((utils.DISPLAY_SIZE, utils.DISPLAY_SIZE), pygame.HWSURFACE)
        self.draw(self.game.get_environment(), self.game.get_points(), False)
        self.render = True
            
class Snake:
    def __init__(self, snake_head_x, snake_head_y, food_x, food_y):
        self.init_snake_head_x = snake_head_x
        self.init_snake_head_y = snake_head_y
        self.init_food_x = food_x
        self.init_food_y = food_y
        # This quantity mentioned in the spec, 8*12*12
        self.starve_steps = 8*(utils.DISPLAY_SIZE//utils.GRID_SIZE)**2
        self.reset()

    def reset(self):
        self.points = 0
        self.steps = 0
        self.snake_head_x = self.init_snake_head_x
        self.snake_head_y = self.init_snake_head_y
        self.snake_body = []
        self.food_x = self.init_food_x
        self.food_y = self.init_food_y

    def get_points(self):
        # These points only updated when food eaten
        return self.points

    def get_actions(self):
        # Corresponds to up, down, left, right
        # return [0, 1, 2, 3]
        return utils.UP, utils.DOWN, utils.LEFT, utils.RIGHT

    def get_environment(self):
        return [
            self.snake_head_x,
            self.snake_head_y,
            self.snake_body,
            self.food_x,
            self.food_y
        ]

    def step(self, action):
        is_dead = self.move(action)
        return self.get_environment(), self.get_points(), is_dead

    def move(self, action):
        self.steps += 1

        delta_x = delta_y = 0

        # Up
        if action == utils.UP:
            delta_y = -1 * utils.GRID_SIZE
        # Down
        elif action == utils.DOWN:
            delta_y = utils.GRID_SIZE
        # Left
        elif action == utils.LEFT:
            delta_x = -1 * utils.GRID_SIZE
        # Right
        elif action == utils.RIGHT:
            delta_x = utils.GRID_SIZE

        old_body_head = None
        if len(self.snake_body) == 1:
            old_body_head = self.snake_body[0]

        # Snake "moves" by 1. adding previous head location to body, 
        self.snake_body.append((self.snake_head_x, self.snake_head_y))
        # 2. updating new head location via delta_x/y
        self.snake_head_x += delta_x
        self.snake_head_y += delta_y

        # 3. removing tail if body size greater than food eaten (points)
        if len(self.snake_body) > self.points:
            del(self.snake_body[0])

        # Eats food, updates points, and randomly generates new food, if appropriate
        self.handle_eatfood()

        # Colliding with the snake body or going backwards while its body length
        # greater than 1
        if len(self.snake_body) >= 1:
            for seg in self.snake_body:
                if self.snake_head_x == seg[0] and self.snake_head_y == seg[1]:
                    return True

        # Moving towards body direction, not allowing snake to go backwards while 
        # its body length is 1
        if len(self.snake_body) == 1:
            if old_body_head == (self.snake_head_x, self.snake_head_y):
                return True

        # Check if collide with the wall (left, top, right, bottom)
        # Again, views grid position wrt top left corner of square
        if (self.snake_head_x < utils.GRID_SIZE or self.snake_head_y < utils.GRID_SIZE or
            self.snake_head_x + utils.GRID_SIZE > utils.DISPLAY_SIZE-utils.GRID_SIZE or self.snake_head_y + utils.GRID_SIZE > utils.DISPLAY_SIZE-utils.GRID_SIZE):
            return True

        # looping for too long and starved
        if self.steps > self.starve_steps:
            return True

        return False

    def handle_eatfood(self):
        if (self.snake_head_x == self.food_x) and (self.snake_head_y == self.food_y):
            self.random_food()
            self.points += 1
            self.steps = 0

    def random_food(self):

        # Math looks at upper left corner wrt DISPLAY_SIZE for grid coordinates

        max_x = utils.DISPLAY_SIZE - utils.WALL_SIZE - utils.GRID_SIZE
        max_y = utils.DISPLAY_SIZE - utils.WALL_SIZE - utils.GRID_SIZE
        
        self.food_x = random.randint(utils.WALL_SIZE, max_x) // utils.GRID_SIZE * utils.GRID_SIZE
        self.food_y = random.randint(utils.WALL_SIZE, max_y) // utils.GRID_SIZE * utils.GRID_SIZE

        # Keeps generating new food locations if it lands on the snake
        while self.check_food_on_snake():
            self.food_x = random.randint(utils.WALL_SIZE, max_x) // utils.GRID_SIZE * utils.GRID_SIZE
            self.food_y = random.randint(utils.WALL_SIZE, max_y) // utils.GRID_SIZE * utils.GRID_SIZE

    def check_food_on_snake(self):
        if self.food_x == self.snake_head_x and self.food_y == self.snake_head_y:
            return True 
        for seg in self.snake_body:
            if self.food_x == seg[0] and self.food_y == seg[1]:
                return True
        return False
        
    
