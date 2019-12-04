'''
Tetris Battle

originally Ccreated by Yuwei Xu, Eman Igbokwe

modified by Yi-Lin Sung

this is a similar version to the ever popular tetris battle
game with not many changes"
'''

#basic modules needed for game to run
import os
import pygame
import random

import numpy as np

from .settings import *

from copy import deepcopy

import time as t
from collections import Counter

def put_block_in_grid(grid, block, px, py):
    feasibles = block.return_pos_color(px, py)

    for x, y, c in feasibles:
        '''
        TODO: y boundary
        '''
        if -1 < x < GRID_WIDTH and -1 < y < len(grid[0]):
            grid[x][y] = c

def collide(grid, block, px, py):
    feasibles = block.get_feasible()

    # print(px)
    # print(block)
    # excess = len(grid[0]) - GRID_DEPTH
    for pos in feasibles:
        # print(px + pos[0], py + pos[1])
        if px + pos[0] > GRID_WIDTH - 1:   # right
            return True

        if px + pos[0] < 0:   # left
            return True

        if py + pos[1] > len(grid[0]) - 1:  # down
            return True

        if py + pos[1] < 0:   # up
            continue
        
        if grid[px + pos[0]][py + pos[1]] > 0:
            # print(px, py)
            # print(px + pos[0], py + pos[1])
            # print("Touch")
            return True

    return False

# collidedown function
# for i in range 4(y position)
# if px+y=20 then collidedown =true
# used for move down and rotation collisions
def collideDown(grid, block, px, py):
    return collide(grid, block, px, py + 1)

# collideleft function
# for i in range 4(x positions)
# if blockx +x =0 then collide left = True
# used for moving block and rotation collision
def collideLeft(grid, block, px, py):
    return collide(grid, block, px - 1, py)

# collideright function
# for i in range 4(x positions)
# if blockx +x +1>9 then collide left = True
# plus 1 is there cuz pxis on left of the piece
# used for moving block and rotation collision
def collideRight(grid, block, px, py):
    return collide(grid, block, px + 1, py)

# rotatecollision function
# when respective rotate buttons are pressed
# this function checks if collide(left right or down has occured)
# if it hasnt then rotation occurs
def rotateCollide(grid, block, px, py):
    feasibles = block.get_feasible()

    left_most = 100
    right_most = 0
    up_most = 100
    down_most = 0

    for pos in feasibles:
        right_most = max(right_most, pos[0])
        left_most = min(left_most, pos[0])

        down_most = max(down_most, pos[1])
        up_most = min(up_most, pos[1])

    c = Counter()
    # print(px)
    # print(block)
    excess = len(grid[0]) - GRID_DEPTH
    for pos in feasibles:
        # print(px + pos[0], py + pos[1])
        if px + pos[0] > 9:   # right
            c.update({"right": 1})

        if px + pos[0] < 0:   # left
            c.update({"left": 1})

        if py + pos[1] > len(grid[0]) - 1:  # down
            c.update({"down": 1})

        # if py + pos[1] < excess:   # up
        #     c.update({"up": 1})

        if 0 <= px + pos[0] <= 9 and excess <= py + pos[1] <= len(grid[0]) - 1:
        
            if grid[px + pos[0]][py + pos[1]] > 0:
                if pos[0] == left_most:
                    c.update({"left": 1})
                elif pos[0] == right_most:
                    c.update({"right": 1})
                elif pos[1] == down_most:
                    c.update({"down": 1})
                # elif pos[1] == up_most:
                #     c.update({"up": 1})

    # print(c)
    if len(c) == 0:
        return False
    else:
        return c.most_common()[0][0]


#this function checks if a tspin has occured
#checks all possible tspin positions
#then spins the t piece into the spot
def tspinCheck(grid, block, px, py):

    if collideDown(grid, block, px, py) == True:
        if block.block_type() == 'T':
            if px + 2 < GRID_WIDTH and py + 3 < len(grid[0]):
                if grid[px][py + 1] > 0 and grid[px][py + 3] > 0 and grid[px + 2][py + 3] > 0:

                    return True
                elif grid[px][py + 3] > 0 and grid[px + 2][py + 3] > 0 and grid[px + 2][py + 1] > 0:

                    return True
    return False

# this function rotates the piece
# when rotation button is hit the next grid in the piece list becomes the piece
def rotate(grid, block, px, py, _dir=1):
    # print(grid)

    block.rotate(_dir)

    # b = block.now_block()

    collision = rotateCollide(grid, block, px, py) # checks for collisions
    # print(collision)
    find = 0

    if collision == "left":
        y_list = [0, 1, -1]
        for s_x in range(0, 3):
            for s_y in y_list:
                if not find and not collide(grid, block, px + s_x, py + s_y):
                    px += s_x
                    py += s_y
                    find = 1
    elif collision == "right":
        y_list = [0, 1, -1]
        for s_x in reversed(range(-2, 0)):
            for s_y in y_list:
                if not find and not collide(grid, block, px + s_x, py + s_y):
                    px += s_x
                    py += s_y
                    find = 1
    elif collision == "down":
        # y_list = [-1, -2]
        x_list = [0, -1, 1, -2, 2]
        for s_y in reversed(range(-1, 0)):
            for s_x in x_list:
                if not find and not collide(grid, block, px + s_x, py + s_y):
                    px += s_x
                    py += s_y
                    find = 1

    elif collision == "up":
        x_list = [0, -1, 1, -2, 2]
        for s_y in range(1, 2):
            for s_x in x_list:
                if not find and not collide(grid, block, px + s_x, py + s_y):
                    px += s_x
                    py += s_y
                    find = 1

    if collision != False and not find:
        block.rotate(- _dir) 

    # print(collision)

    tspin = 0
    if tspinCheck(grid, block, px, py) == True:
        tspin = 1
        print("Tspin rotate")

    # return [block, px, py, tspin]

    return block, px, py, tspin


# this function drops the piece as far as it can go until
# it collides with a piece below it
def hardDrop(grid, block, px, py):
    y = 0
    x = 0
    if collideDown(grid, block, px, py) == False:
        x = 1
    if x == 1:
        while True:
            py += 1
            y += 1
            if collideDown(grid, block, px, py) == True:
                break
        
    return y

# this function enables you to hold a piece
def hold(block, held, _buffer):
    # when piece is held the block at pos[0]
    # in the nextlist becomes the newpiece
    if held == None:
        held = block
        block = _buffer.new_block()

    # the piece switches with the held piece     
    else:
        block, held = held, block
        
    return [block, held]

def freeze(last_time):
    start = t.time()
    while t.time() - start < last_time:
        pass

def get_infos(board):
    # board is equal to grid

    # borrow from https://github.com/scuriosity/machine-learning-tetris/blob/master/tetris.py
    # This function will calculate different parameters of the current board

    # Initialize some stuff
    heights = [0] * len(board)
    diffs = [0] * (len(board) - 1)
    holes = 0
    diff_sum = 0

    # Calculate the maximum height of each column
    for i in range(0, len(board)):  # Select a column
        for j in range(0, len(board[0])):  # Search down starting from the top of the board
            if int(board[i][j]) > 0:  # Is the cell occupied?
                heights[i] = len(board[0]) - j  # Store the height value
                break

    # Calculate the difference in heights
    for i in range(0, len(diffs)):
        diffs[i] = heights[i + 1] - heights[i]

    # Calculate the maximum height
    max_height = max(heights)

    # Count the number of holes
    for i in range(0, len(board)):
        occupied = 0  # Set the 'Occupied' flag to 0 for each new column
        for j in range(0, len(board[0])):  # Scan from top to bottom
            if int(board[i][j]) > 0:
                occupied = 1  # If a block is found, set the 'Occupied' flag to 1
            if int(board[i][j]) == 0 and occupied == 1:
                holes += 1  # If a hole is found, add one to the count

    height_sum = sum(heights)

    for i in diffs:
        diff_sum += abs(i)

    return height_sum, diff_sum, max_height, holes

class Piece(object):
    def __init__(self, _type, possible_shapes):

        self._type = _type
        self.possible_shapes = possible_shapes

        self.current_shape_id = 0 

    def block_type(self):
        return self._type

    def reset(self):
        self.current_shape_id = 0

    def return_pos_color(self, px, py):
        feasibles = []

        block = self.now_block()

        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if block[x][y] > 0:
                    feasibles.append([px + x, py + y, block[x][y]])
        return feasibles

    def return_pos(self, px, py):
        feasibles = []

        block = self.now_block()

        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if block[x][y] > 0:
                    feasibles.append([px + x, py + y])
        return feasibles

    def get_feasible(self):
        feasibles = []

        b = self.now_block()

        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if b[x][y] > 0:
                    feasibles.append([x, y])

        return feasibles

    def now_block(self):
        return self.possible_shapes[self.current_shape_id]

    # def move_right(self, unit=1):
    #     self.px += unit

    # def move_left(self, unit=1):
    #     self.px -= unit

    # def move_up(self, unit=1):
    #     self.py -= unit

    # def move_down(self, unit=1):
    #     self.py += unit

    def rotate(self, _dir=1):
        self.current_shape_id += _dir
        self.current_shape_id %= len(self.possible_shapes)

class Buffer(object):
    '''
    Stores the coming pieces, every 7 pieces in a group.
    '''
    def __init__(self):
        self.now_list = []
        self.next_list = []

        self.fill(self.now_list)
        self.fill(self.next_list)

    '''
    make sure "now list" are filled

                     now list           next list
    next piece <- [           ]   <-  [            ]
 
    '''
    def new_block(self):
        out = self.now_list.pop(0)
        self.now_list.append(self.next_list.pop(0))

        if len(self.next_list) == 0:
            self.fill(self.next_list)

        return out

    def fill(self, _list):
        pieces_keys = deepcopy(POSSIBLE_KEYS)
        random.shuffle(pieces_keys)

        for key in pieces_keys:
            _list.append(Piece(key, PIECES_DICT[key]))


'''

class for player

'''

class Player(object):
    def __init__(self, info_dict):

        self._id = info_dict.get("id")

        self._drop = info_dict.get("drop")
        self._hold = info_dict.get("hold")
        self._rotate_right = info_dict.get("rotate_right")
        self._rotate_left = info_dict.get("rotate_left")
        self._down = info_dict.get("down")
        self._left = info_dict.get("left")
        self._right = info_dict.get("right")

    @property
    def id(self):
        return self._id

    @property
    def drop(self):
        return self._drop

    @property
    def hold(self):
        return self._hold

    @property
    def rotate_right(self):
        return self._rotate_right

    @property
    def rotate_left(self):
        return self._rotate_left

    @property
    def down(self):
        return self._down

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

'''

class Judge

'''

class Judge(object):

    @staticmethod
    def check_ko_win(tetris, max_ko):
        if tetris.KO >= max_ko:
            return 1

        return 0

    @staticmethod
    def who_win(tetris_1, tetris_2):
        if tetris_2.KO > tetris_1.KO: # Checks who is the winner of the game
            return tetris_2.get_id() # a is screebn.copy,endgame ends the game,2 is player 2 wins
        if tetris_1.KO > tetris_2.KO:
            return tetris_1.get_id() # a is screebn.copy,endgame ends the game,1 is player 1 wins
        if tetris_1.KO == tetris_2.KO:
            if tetris_2.sent > tetris_1.sent:
                return tetris_2.get_id() # a is screebn.copy,endgame ends the game,2 is player 2 wins
            elif tetris_1.sent > tetris_2.sent:
                return tetris_1.get_id() # a is screebn.copy,endgame ends the game,1 is player 1 wins
            elif tetris_1.get_maximum_height() > tetris_2.get_maximum_height():
                return tetris_2.get_id()
            elif tetris_2.get_maximum_height() > tetris_1.get_maximum_height():
                return tetris_1.get_id()
            else:
                return tetris_1.get_id() # no UI of draw

class Tetris(object):
    def __init__(self, player, gridchoice):

        if gridchoice == "none":
            self.o_grid = [[0] * GRID_DEPTH for i in range(GRID_WIDTH)]

        if gridchoice == "classic":
            self.o_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 3], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        if gridchoice == "comboking":
            self.o_grid = [[0, 0, 0, 0, 0, 5, 5, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], 
                          [0, 0, 0, 0, 0, 6, 6, 6, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 4, 5], 
                          [0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], 
                          [0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5], 
                          [0, 0, 0, 0, 0, 6, 6, 6, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 4, 5], 
                          [0, 0, 0, 0, 0, 5, 5, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]

        if gridchoice == "lunchbox":
            self.o_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 5, 5, 5, 5, 5, 5, 5, 1], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 2, 2, 2, 2, 2, 2, 5, 1], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 2, 4, 4, 4, 4, 2, 5, 1], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 5, 2, 4, 4, 4, 4, 2, 5, 6], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 5, 2, 2, 2, 2, 2, 2, 5, 6], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 5, 5, 5, 5, 5, 5, 5, 5, 6], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]]


        self.player = player

        self.reset()

    def reset(self):
        self.grid = deepcopy(self.o_grid)

        self.oldko = 0 # these two used to keep track of ko's

        self._n_used_block = 1

        self.buffer = Buffer()
        # list of the held piece
        self.held = None
        self.block = self.buffer.new_block()

        # amount of lines sent for p1 and p2
        self.sent = 0
        self.tempsend = 0 # tempsending for p1 and p2
        self.oldcombo = self.combo = -1 # used for checking comboas
        self.tspin = 0 # for t spin
        self.now_back2back = 0
        self.pre_back2back = 0
        self.tetris = 0

        #for "KO"
        self._KO = 0 

        self._attacked = 0
        self._is_fallen = 0

        self.px = 4
        self.py = -2

        # DEFINING VARIABLES
        self.cleared = 0
        self.kocounter = 0
        self.stopcounter = 0

        self.isholded = 0

        self.pressedRight = False
        self.pressedLeft = False
        self.pressedDown = False


        self.LAST_ROTATE_TIME = 0
        self.LAST_MOVE_SHIFT_TIME = 0
        self.LAST_MOVE_DOWN_TIME = 0
        self.LAST_COMBO_DRAW_TIME = 0
        self.LAST_TETRIS_DRAW_TIME = 0
        self.LAST_TSPIN_DRAW_TIME = 0
        self.LAST_BACK2BACK_DRAW_TIME = 0
        self.LAST_NATRUAL_FALL_TIME = 0
        self.LAST_FALL_DOWN_TIME = 0


        self.tetris_drawing = 0
        self.tspin_drawing = 0
        self.back2back_drawing = 0

        self.combo_counter = 0

        self.natural_down_counter = 0

    def increment_timer(self):
        self.LAST_ROTATE_TIME += 1
        self.LAST_MOVE_SHIFT_TIME += 1
        self.LAST_MOVE_DOWN_TIME += 1
        self.LAST_COMBO_DRAW_TIME += 1
        self.LAST_TETRIS_DRAW_TIME += 1
        self.LAST_TSPIN_DRAW_TIME += 1
        self.LAST_BACK2BACK_DRAW_TIME += 1
        self.LAST_NATRUAL_FALL_TIME += 1
        self.LAST_FALL_DOWN_TIME += 1

    @property
    def is_fallen(self):
        return self._is_fallen

    @property
    def n_used_block(self):
        return self._n_used_block

    @property
    def KO(self):
        return self._KO

    @property
    def attacked(self):
        return self._attacked
    
    def get_grid(self):
        excess = len(self.grid[0]) - GRID_DEPTH
        return_grids = np.zeros(shape=(GRID_WIDTH, GRID_DEPTH), dtype=np.float32)
        
        block, px, py = self.block, self.px, self.py
        excess = len(self.grid[0]) - GRID_DEPTH
        b = block.now_block()

        for i in range(len(self.grid)):
            return_grids[i] = np.array(self.grid[i][excess:GRID_DEPTH], dtype=np.float32)
        return_grids[return_grids > 0] = 1

        add_y = hardDrop(self.grid, self.block, self.px, self.py)

        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if b[x][y] > 0:
                    # draw ghost grid
                    if -1 < px + x < 10 and -1 < py + y + add_y - excess < 20:
                        return_grids[px + x][py + y + add_y - excess] = 0.3
                        
                    if -1 < px + x < 10 and -1 < py + y - excess < 20:
                        return_grids[px + x][py + y - excess] = 0.7

        informations = np.zeros(shape=(len(PIECE_NUM2TYPE) - 1, GRID_DEPTH), dtype=np.float32)
        if self.held != None:
            informations[PIECE_TYPE2NUM[self.held.block_type()] - 1][0] = 1

        nextpieces = self.buffer.now_list
        for i in range(5): # 5 different pieces 
            _type = nextpieces[i].block_type()
            informations[PIECE_TYPE2NUM[_type] - 1][i + 1] = 1
        # index start from 6

        informations[0][6] = self.sent / 100
        informations[1][6] = self.combo / 10
        informations[2][6] = self.pre_back2back
        informations[3][6] = self._attacked / GRID_DEPTH
        # informations[3][7] = self.time / MAX_TIME

        return_grids = np.concatenate((return_grids, informations), axis=0)

        return np.transpose(return_grids, (1, 0))

    def get_board(self):
        excess = len(self.grid[0]) - GRID_DEPTH
        return_grids = np.zeros(shape=(GRID_WIDTH, GRID_DEPTH), dtype=np.float32)
        
        block, px, py = self.block, self.px, self.py
        excess = len(self.grid[0]) - GRID_DEPTH
        # b = block.now_block()

        for i in range(len(self.grid)):
            return_grids[i] = np.array(self.grid[i][excess:GRID_DEPTH], dtype=np.float32)
        return_grids[return_grids > 0] = 1
        # for x in range(BLOCK_WIDTH):
        #     for y in range(BLOCK_LENGTH):
        #         if b[x][y] > 0:
        #             if -1 < px + x < 10 and -1 < py + y - excess < 20:
        #                 return_grids[px + x][py + y - excess] = 0.5


        return return_grids

    def get_maximum_height(self):
        max_height = 0
        for i in range(0, len(self.grid)):  # Select a column
            for j in range(0, len(self.grid[0])):  # Search down starting from the top of the board
                if int(self.grid[i][j]) > 0:  # Is the cell occupied?
                    max_height = max(max_height, len(self.grid[0]) - j) 
                    break
        return max_height

    def reset_pos(self):
        self.px = 4
        self.py = -2 + len(self.grid[0]) - GRID_DEPTH

    def get_id(self):
        return self.player.id

    def add_attacked(self, attacked):
        self._attacked += attacked
        self._attacked = min(self._attacked, GRID_DEPTH)

    def natural_down(self):
        if self.LAST_NATRUAL_FALL_TIME >= NATRUAL_FALL_FREQ:
            if collideDown(self.grid, self.block, self.px, self.py) == False:
                self.stopcounter = 0
                # self.block.move_down()
                self.py += 1
                # pass

            self.LAST_NATRUAL_FALL_TIME = 0
        # else:
        #     self.natural_down_counter += 1

    def trigger(self, evt):
        # if (hasattr(evt, "key")):
        #     print(evt.key)
        if evt.type == pygame.KEYDOWN:
            if evt.key == self.player.rotate_right and self.LAST_ROTATE_TIME >= ROTATE_FREQ: # rotating
                self.block, self.px, self.py, self.tspin = rotate(self.grid, self.block, self.px, self.py, _dir=1)
                self.LAST_ROTATE_TIME = 0

            if evt.key == self.player.rotate_left and self.LAST_ROTATE_TIME >= ROTATE_FREQ: # rotating
                self.block, self.px, self.py, self.tspin = rotate(self.grid, self.block, self.px, self.py, _dir=-1)
                self.LAST_ROTATE_TIME = 0

            if evt.key == self.player.drop: # harddrop
                y = hardDrop(self.grid, self.block, self.px, self.py) # parameters
                # self.block.move_down(y)
                self.py += y
                # self.stopcounter = COLLIDE_DOWN_COUNT
                # self.LAST_FALL_DOWN_TIME = -FALL_DOWN_FREQ
                self.LAST_FALL_DOWN_TIME = FALL_DOWN_FREQ

            if evt.key == self.player.hold: #holding 

                if not self.isholded:

                    self.block, self.held = hold(self.block, self.held, self.buffer) # parameters
                    self.held.reset()
                    self.reset_pos()
                    self.isholded = 1

            if evt.key == self.player.right:
                self.pressedRight = True

            if evt.key == self.player.left:
                self.pressedLeft = True

            if evt.key == self.player.down:
                self.pressedDown = True

        if evt.type == pygame.KEYUP:

            if evt.key == self.player.right:
                self.pressedRight = False

            if evt.key == self.player.left:
                self.pressedLeft = False

            if evt.key == self.player.down:
                self.pressedDown = False

    # move function
    # when respective buttons are pressed
    def move(self):
        # if keys[self.right]:
        if self.pressedRight and self.LAST_MOVE_SHIFT_TIME > MOVE_SHIFT_FREQ:
            if collideRight(self.grid, self.block, self.px, self.py) == False:    
                self.LAST_MOVE_SHIFT_TIME = 0

                # self.block.move_right()
                self.px += 1

        if self.pressedLeft and self.LAST_MOVE_SHIFT_TIME > MOVE_SHIFT_FREQ:
            if collideLeft(self.grid, self.block, self.px, self.py) == False:
                self.LAST_MOVE_SHIFT_TIME = 0

                # self.block.move_left()
                self.px -= 1

        if self.pressedDown and self.LAST_MOVE_DOWN_TIME > MOVE_DOWN_FREQ:
            if collideDown(self.grid, self.block, self.px, self.py) == False:
                self.LAST_MOVE_DOWN_TIME = 0
                # self.stopcounter = 0

                # self.block.move_down()
                self.py += 1

    def check_fallen(self):
        if collideDown(self.grid, self.block, self.px, self.py) == True:
            # self.stopcounter += 1
            if self.LAST_FALL_DOWN_TIME >= FALL_DOWN_FREQ:
                self._is_fallen = 1
                put_block_in_grid(self.grid, self.block, self.px, self.py)
                # print("fallen")

                return True

        else:
            self._is_fallen = 0
            # self.stopcounter = 0
            self.LAST_FALL_DOWN_TIME = 0

        return False

        # if self.stopcounter >= COLLIDE_DOWN_COUNT: # adds adequate delay  
        #     if block_in_grid(self.grid, self.block):
        #         self.is_fallen = 1
        #         return True

        # return False

    # compute the scores when the block is fallen down.
    # return True if the computation is done.

    def compute_scores(self, cleared, combo, tspin, tetris, pre_back2back):

        if cleared == 0:
            scores = 0
        else:
            scores = cleared if cleared == 4 else cleared - 1

            # scores from combos
            if combo > 0:
                if combo <= 8:
                    combo_scores = int((combo + 1) / 2)
                else: combo_scores = 4
            else:
                combo_scores = 0

            scores += combo_scores

            # 2 line tspin 
            if tspin and cleared == 2:
                scores += 3

            if pre_back2back:
                if tspin or tetris:
                    scores += 2

        return scores

    def clear(self):

        cleared = 0

        # self.tetris = 0

        is_combo = 0

        for y in reversed(range(GRID_DEPTH)):
            y = -(y + 1)
            row = 0 # starts checking from row zero
            for x in range(GRID_WIDTH):
                if self.grid[x][y] > 0 and self.grid[x][y] < 8:
                    row += 1

            if row == GRID_WIDTH:
                cleared += 1
                for i in range(GRID_WIDTH):
                    del self.grid[i][y] # deletes cleared lines
                    self.grid[i] = [0] + self.grid[i] # adds a row of zeros to the grid
                        
        if cleared >= 1: # for sending lines
            self.combo += 1
            if cleared == 4: # a tetris
                self.tetris = 1
            else:
                self.tetris = 0

            self.pre_back2back = self.now_back2back   
        else:
            self.combo = -1
            self.tetris = 0

        # compute scores
        scores = self.compute_scores(cleared, self.combo, self.tspin, self.tetris, self.pre_back2back)

        if cleared >= 1:
            if self.tspin or self.tetris:
                print("next backtoback")
                self.now_back2back = 1
            else:
                self.now_back2back = 0
        # print(self.pre_back2back, self.now_back2back)
        # self.tspin = 0

        self.cleared = cleared
        self.sent += scores

        real_attacked = max(0, self._attacked - scores)

        self.build_garbage(self.grid, real_attacked)

        self._attacked = 0
        
        return scores

        # return scores

    def check_KO(self):
        is_ko = False
        #if your grid hits the top ko = true
        excess = len(self.grid[0]) - GRID_DEPTH

        for i in range(GRID_WIDTH):
            if self.grid[i][excess] > 0:
                is_ko = True
                break

        return is_ko
        
    def clear_garbage(self):
        garbage = 0
        # excess = len(grid[0]) - GRID_DEPTH
        for y in range(0, len(self.grid[0])):
            for x in range(GRID_WIDTH):
                if self.grid[x][y] == 8:
                    garbage += 1
                    self.grid[x].pop(y)
                    self.grid[x] = [0] + self.grid[x]

    def build_garbage(self, grid, attacked):
        garbage_size = min(attacked, GRID_DEPTH)
        for y in range(0, garbage_size):    
            for i in range(GRID_WIDTH):
                # del player.grid[i][y] # deletes top of grid
                grid[i] = grid[i] + [8] # adds garbage lines at the bottom

        # return grid

    def check_combo(self):
        return self.combo - self.oldcombo >= 1

    def new_block(self):
        self.block = self.buffer.new_block()
        self.reset_pos()
        self.isholded = 0
        self.tspin = 0
        self._n_used_block += 1

    def update_ko(self):
        self.oldko = self._KO
        self._KO += 1

    def update_combo(self):
        self.oldcombo = self.combo
        self.combo += 1
