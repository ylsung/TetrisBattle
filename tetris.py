'''
Tetris Battle
Created by Yuwei Xu, Eman Igbokwe
this is a similar version to the ever popular tetris battle
game with not many changes"
'''

#basic modules needed for game to run
import os
import pygame
import random

import numpy as np

from settings import *

from copy import deepcopy

import time as t
from collections import Counter

def combo_scores(combo):
    if combo > 0:
        if combo <= 8:
            return int((combo + 1) / 2)
        else: return 4

    return 0
    

def block_in_grid(grid, block, px, py):
    feasibles = block.return_pos_color(px, py)

    for x, y, c in feasibles:
        '''
        TODO: y boundary
        '''
        if -1 < x < GRID_WIDTH and -1 < y < len(grid[0]):
            grid[x][y] = c

#the ghost block piece
def drawGhost(sx, sy, x, y):
    SCREEN.blit(IMAGES["ghost"], (sx + x * 18, sy + y * 18))
    
        
#the timer for the game
def drawTime2p(time):
    minutes = time / 60000 #integer div for minutes
    seconds = (time / 1000) % 60 #int and mod div for sec
    milliseconds = (time / 10) % 100# int and mod div for millisec

    x = 292 #position of the IMAGES["numbers"] 
    y = 67
    SCREEN.blit(IMAGES["timeback"], (280, 63)) #background
    #minutes
    SCREEN.blit(IMAGES["numbers"][int(minutes / 10)], (x, y))
    SCREEN.blit(IMAGES["numbers"][int(minutes)], (x + 27, y))
    SCREEN.blit(IMAGES["decimal"], (x + 56, y))  #graphics
    SCREEN.blit(IMAGES["decimal"], (x + 56, y + 14))  #graphics
    SCREEN.blit(IMAGES["decimal"], (x + 127, y + 14)) #graphics
    #seconds
    SCREEN.blit(IMAGES["numbers"][int(seconds / 10)], (x + 73, y))
    SCREEN.blit(IMAGES["numbers"][int(seconds % 10)], (x + 100, y))
    #milliseconds
    SCREEN.blit(IMAGES["numbers"][int(milliseconds / 10)], (x + 144, y))
    SCREEN.blit(IMAGES["numbers"][int(milliseconds % 10)], (x + 171, y))

# drawing the different blocks
# different IMAGES["numbers"](vals) draws differnt colour blocks on the SCREEN
def drawBlock(sx, sy, x, y, val):
    # IMAGES["pics"] = [ipiece, opiece, jpiece, lpiece, zpiece, spiece, tpiece, lspiece]
    SCREEN.blit(IMAGES["piecepics"][PIECE_NUM2TYPE[val]], (sx + x * 18, sy + y * 18))

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

# ko Function
def KO(grid, block):
    ko = False
    #if your grid hits the top ko = true
    excess = len(grid[0]) - GRID_DEPTH

    for i in range(GRID_WIDTH):
        if grid[i][excess] > 0:
            ko = True
            break

    return ko
#def win(grid,gridb,kO,sent):
    
# clear lines function
# when you send lines the grid clears the line
# return scores
def clear(grid, block, combo, tspin, now_back2back, pre_back2back):
    cleared = 0

    tetris = 0

    scores = 0

    for y in reversed(range(GRID_DEPTH)):
        y = -(y + 1)
        row = 0 # starts checking from row zero
        for x in range(GRID_WIDTH):
            if grid[x][y] > 0 and grid[x][y] < 8:
                row += 1

        if row == GRID_WIDTH:
            # add -= 1
            # #print tspinCheck(grid,block,px,py,b)
            # if tspinCheck(grid, block, px, py, b) == True: # for tspin sends more lines than actually cleared
            #     scores += add
            #     tspin = 1
            #     print("Tspin")
                
            cleared += 1
            for i in range(GRID_WIDTH):
                del grid[i][y] # deletes cleared lines
                grid[i] = [0] + grid[i] # adds a row of zeros to the grid
                    
    if cleared >= 1: # for sending lines
        combo += 1
        # combo = min(combo, MAX_COMBO)

        if cleared == 4: # a tetris
            # SCREEN.blit(tetris,(330,465))
            scores += 4 
            tetris = 1
        else:
            scores += (cleared - 1)

            if tspin:
                scores += 3
        # for i in range(1, 4):#single, double, triple
            # if cleared == i:
                # scores += (i - 1)

        if pre_back2back:
            if tspin or tetris:
                scores += 2

        pre_back2back = now_back2back

        if tspin or tetris:
            print("next backtoback")
            now_back2back = 1
        else:
            now_back2back = 0

    if cleared == 0: # no lines cleared= no combo
        #SCREEN.blit(back,(315,440))
        combo = -1

    c_s = combo_scores(combo) # linessent increases with amount of combos

    scores += c_s
    # player.tspin = tspin
    # player.tetris = tetris
    

    return (scores, combo, tetris)



#getPositon function
#gets the position of the block falling
#position is sorted and returned to be used
#for the falling blocks
def getPositions(block, px, py):  
    positions = []
    for x in range(4):
        for y in range (4):
            if block[x][y] > 0:
                positions.append((px + x, py + y))
                sorted(positions, key=lambda pos: pos[1])
    return positions

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

def build_garbage(grid, attacked):
    garbage_size = min(attacked, GRID_DEPTH)
    for y in range(0, garbage_size):    
        for i in range(GRID_WIDTH):
            # del player.grid[i][y] # deletes top of grid
            grid[i] = grid[i] + [8] # adds garbage lines at the bottom

    return grid

def clear_garbage(grid):
    # for x in range(DEPTH)
    # if ko = true then all the garbage lines
    # are deleted. If there are no garbage lines then you lose

    garbage = 0
    # excess = len(grid[0]) - GRID_DEPTH
    for y in range(0, len(grid[0])):
        for x in range(GRID_WIDTH):
            if grid[x][y] == 8:
                garbage += 1
                grid[x].pop(y)
                grid[x] = [0] + grid[x]


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
        self.grid = deepcopy(self.o_grid)

        self.oldko = 0 # these two used to keep track of ko's

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
        self.KO = 0 

        self.attacked = 0
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

        self.LAST_ROTATE_TIME = t.time()
        self.LAST_MOVE_SHIFT_TIME = t.time()
        self.LAST_MOVE_DOWN_TIME = t.time()
        self.LAST_COMBO_DRAW_TIME = t.time()
        self.LAST_TETRIS_DRAW_TIME = t.time()
        self.LAST_TSPIN_DRAW_TIME = t.time()
        self.LAST_BACK2BACK_DRAW_TIME = t.time()
        self.LAST_NATRUAL_FALL_TIME = t.time()
        self.LAST_FALL_DOWN_TIME = t.time()


        self.tetris_drawing = 0
        self.tspin_drawing = 0
        self.back2back_drawing = 0

        self.combo_counter = 0

        self.natural_down_counter = 0

    def reset(self):
        self.grid = deepcopy(self.o_grid)

        self.oldko = 0 # these two used to keep track of ko's

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
        self.KO = 0 

        self.attacked = 0
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


        self.LAST_ROTATE_TIME = t.time()
        self.LAST_MOVE_SHIFT_TIME = t.time()
        self.LAST_MOVE_DOWN_TIME = t.time()
        self.LAST_COMBO_DRAW_TIME = t.time()
        self.LAST_TETRIS_DRAW_TIME = t.time()
        self.LAST_TSPIN_DRAW_TIME = t.time()
        self.LAST_BACK2BACK_DRAW_TIME = t.time()
        self.LAST_NATRUAL_FALL_TIME = t.time()
        self.LAST_FALL_DOWN_TIME = t.time()


        self.tetris_drawing = 0
        self.tspin_drawing = 0
        self.back2back_drawing = 0

        self.combo_counter = 0

        self.natural_down_counter = 0


    @property
    def is_fallen(self):
        return self._is_fallen
    

    def get_grid(self):
        excess = len(self.grid[0]) - GRID_DEPTH
        return_grids = np.zeros(shape=(GRID_WIDTH, GRID_DEPTH), dtype=np.float32)

        for i in range(len(self.grid)):
            return_grids[i] = np.array(self.grid[i][excess:GRID_DEPTH], dtype=np.float32)

        return return_grids

    def reset_pos(self):
        self.px = 4
        self.py = -2 + len(self.grid[0]) - GRID_DEPTH

    def get_id(self):
        return self.player.id

    def get_KO(self):
        return self.KO

    def add_attacked(self, attacked):
        self.attacked += attacked

    def natural_down(self):
        if t.time() - self.LAST_NATRUAL_FALL_TIME >= NATRUAL_FALL_FREQ:
            if collideDown(self.grid, self.block, self.px, self.py) == False:
                self.stopcounter = 0
                # self.block.move_down()
                self.py += 1
                # pass

            self.LAST_NATRUAL_FALL_TIME = t.time()
        # else:
        #     self.natural_down_counter += 1

    def trigger(self, evt):
        if evt.type == pygame.KEYDOWN:
            if evt.key == self.player.rotate_right and t.time() - self.LAST_ROTATE_TIME >= ROTATE_FREQ: # rotating
                self.block, self.px, self.py, self.tspin = rotate(self.grid, self.block, self.px, self.py, _dir=1)
                self.LAST_ROTATE_TIME = t.time()

            if evt.key == self.player.rotate_left and t.time() - self.LAST_ROTATE_TIME >= ROTATE_FREQ: # rotating
                self.block, self.px, self.py, self.tspin = rotate(self.grid, self.block, self.px, self.py, _dir=-1)
                self.LAST_ROTATE_TIME = t.time()

            if evt.key == self.player.drop: # harddrop
                y = hardDrop(self.grid, self.block, self.px, self.py) # parameters
                # self.block.move_down(y)
                self.py += y
                # self.stopcounter = COLLIDE_DOWN_COUNT
                self.LAST_FALL_DOWN_TIME = -FALL_DOWN_FREQ

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
        if self.pressedRight and t.time() - self.LAST_MOVE_SHIFT_TIME > MOVE_SHIFT_FREQ:
            if collideRight(self.grid, self.block, self.px, self.py) == False:    
                self.LAST_MOVE_SHIFT_TIME = t.time()

                # self.block.move_right()
                self.px += 1

        if self.pressedLeft and t.time() - self.LAST_MOVE_SHIFT_TIME > MOVE_SHIFT_FREQ:
            if collideLeft(self.grid, self.block, self.px, self.py) == False:
                self.LAST_MOVE_SHIFT_TIME = t.time()

                # self.block.move_left()
                self.px -= 1

        if self.pressedDown and t.time() - self.LAST_MOVE_DOWN_TIME > MOVE_DOWN_FREQ:
            if collideDown(self.grid, self.block, self.px, self.py) == False:
                self.LAST_MOVE_DOWN_TIME = t.time()
                # self.stopcounter = 0

                # self.block.move_down()
                self.py += 1

    def check_fallen(self):
        if collideDown(self.grid, self.block, self.px, self.py) == True:
            # self.stopcounter += 1
            if t.time() - self.LAST_FALL_DOWN_TIME >= FALL_DOWN_FREQ:
                self._is_fallen = 1
                block_in_grid(self.grid, self.block, self.px, self.py)
                # print("fallen")

                return True

        else:
            self._is_fallen = 0
            # self.stopcounter = 0
            self.LAST_FALL_DOWN_TIME = t.time()

        return False

        # if self.stopcounter >= COLLIDE_DOWN_COUNT: # adds adequate delay  
        #     if block_in_grid(self.grid, self.block):
        #         self.is_fallen = 1
        #         return True

        # return False

    # compute the scores when the block is fallen down.
    # return True if the computation is done.

    def compute_scores(self, tspin):
        cleared = 0

        scores = 0

        tetris = 0

        for y in reversed(range(GRID_DEPTH)):
            y = -(y + 1)
            row = 0 # starts checking from row zero
            for x in range(GRID_WIDTH):
                if self.grid[x][y] > 0 and self.grid[x][y] < 8:
                    row += 1

            if row == GRID_WIDTH:
                # add -= 1
                # #print tspinCheck(grid,block,px,py,b)
                # if tspinCheck(grid, block, px, py, b) == True: # for tspin sends more lines than actually cleared
                #     scores += add
                #     tspin = 1
                #     print("Tspin")
                    
                cleared += 1
                for i in range(GRID_WIDTH):
                    del self.grid[i][y] # deletes cleared lines
                    self.grid[i] = [0] + self.grid[i] # adds a row of zeros to the grid
                        
        if cleared >= 1: # for sending lines
            self.combo += 1
            # combo = min(combo, MAX_COMBO)

            if cleared == 4: # a tetris
                # SCREEN.blit(tetris,(330,465))
                scores += 4 
                tetris = 1
            else:
                scores += (cleared - 1)

                if cleared == 2 and tspin:
                    scores += 3
                else:
                    tspin = 0
            # for i in range(1, 4):#single, double, triple
                # if cleared == i:
                    # scores += (i - 1)

            self.pre_back2back = self.now_back2back

            if self.pre_back2back:
                if tspin or tetris:
                    scores += 2

            # self.pre_back2back = self.now_back2back

            if tspin or tetris:
                print("next backtoback")
                self.now_back2back = 1
            else:
                self.now_back2back = 0

        if cleared == 0: # no lines cleared= no combo
            #SCREEN.blit(back,(315,440))
            self.combo = -1

        c_s = combo_scores(self.combo) # linessent increases with amount of combos

        scores += c_s

        return scores, tetris, tspin

    def clear(self):
        scores = 0
        # if self.is_fallen:
        # self.pre_back2back = self.now_back2back
        # scores, self.combo, self.tetris = clear(self.grid,
        #                                         self.block,
        #                                         self.combo,
        #                                         self.tspin,
        #                                         self.now_back2back,
        #                                         self.pre_back2back)

        scores, self.tetris, self.tspin = self.compute_scores(self.tspin)

        # print(self.pre_back2back, self.now_back2back)
        # self.tspin = 0
        self.sent += scores

        real_attacked = max(0, self.attacked - scores)

        self.grid = build_garbage(self.grid, real_attacked)

        self.attacked = 0
        
        return scores

        # return scores

    def check_KO(self):
        ko = KO(self.grid, self.block)
        
        return ko

    def clear_garbage(self):
        clear_garbage(self.grid)

    def check_combo(self):
        return self.combo - self.oldcombo >= 1

    def new_block(self):
        self.block = self.buffer.new_block()
        self.reset_pos()
        self.isholded = 0
        self.tspin = 0

    def update_ko(self):
        self.oldko = self.KO
        self.KO += 1

    def update_combo(self):
        self.oldcombo = self.combo
        self.combo += 1

class Renderer(object):

    
    # this function draws the combo number, return True if sucessfully draw
    @staticmethod
    def drawCombo(tetris, combos, sx, sy):

        if tetris.combo > 0:
            r = SCREEN.blit(combos[min(tetris.combo, MAX_COMBO) - 1], (sx, sy)) #blits the combo number

            pygame.display.update(r)

            tetris.LAST_COMBO_DRAW_TIME = t.time()

            return True

        else:
            tetris.oldcombo = 0

        tetris.combo_counter = 0

        return False

    @staticmethod
    def drawTetris(tetris, sx, sy):
        if tetris.tetris:
            r = SCREEN.blit(IMAGES["tetris_img"], (sx, sy))
            
            pygame.display.update(r)

            tetris.LAST_TETRIS_DRAW_TIME = t.time()
            tetris.tetris_drawing = 1

            # print("tetris")

            return True

        return False

    @staticmethod
    def drawTspin(tetris, sx, sy):
        if tetris.tspin:
            r = SCREEN.blit(IMAGES["tspin_double_img"], (sx, sy))
            
            pygame.display.update(r)

            tetris.LAST_TSPIN_DRAW_TIME = t.time()
            tetris.tspin_drawing = 1

            return True

        return False

    @staticmethod
    def drawBack2Back(tetris, sx, sy):
        if tetris.pre_back2back and (tetris.tspin or tetris.tetris):
            r = SCREEN.blit(IMAGES["back2back_img"], (sx, sy))
            
            pygame.display.update(r)

            tetris.LAST_BACK2BACK_DRAW_TIME = t.time()
            tetris.back2back_drawing = 1

            return True

        return False

    @staticmethod
    def drawGameScreen(tetris):
        if t.time() - tetris.LAST_COMBO_DRAW_TIME > COMBO_COUNT_FREQ and tetris.check_combo():
            SCREEN.blit(IMAGES["gamescreen"], (0, 0))
            tetris.oldcombo = tetris.combo

        if t.time() - tetris.LAST_TSPIN_DRAW_TIME > TSPIN_FREQ and tetris.tspin_drawing:
            SCREEN.blit(IMAGES["gamescreen"], (0, 0))
            tetris.tspin_drawing = 0

        if t.time() - tetris.LAST_TETRIS_DRAW_TIME > TETRIS_FREQ and tetris.tetris_drawing:
            SCREEN.blit(IMAGES["gamescreen"], (0, 0))
            tetris.tetris_drawing = 0

        if t.time() - tetris.LAST_BACK2BACK_DRAW_TIME > BACK2BACK_FREQ and tetris.back2back_drawing:
            SCREEN.blit(IMAGES["gamescreen"], (0, 0))
            tetris.back2back_drawing = 0
            # tetris.combo += 1

    #drawing the actual game SCREEN     
    @classmethod   
    def drawScreen(cls, tetris_1, sx, sy):
        cls.drawHeld(tetris_1, sx - 56, sy + 23)  # draws held piece for grid1
        cls.drawNext(tetris_1, sx + 206, sy + 23) # draws next piece for grid1
        cls.drawNumbers(tetris_1, sx - 56, sy + 239) # draws the linessent on the SCREEN for grid1
                        
        #this code blits the background grid for grid1
        excess = len(tetris_1.grid[0]) - GRID_DEPTH
        # print(player_1.grid)
        for x in range(GRID_WIDTH):
            for y in range(excess, len(tetris_1.grid[0])):
                if tetris_1.grid[x][y] == 0:
                    if (x + y) % 2 == 0:
                        SCREEN.blit(IMAGES["dgrey"], (sx + x * 18, sy + (y - excess) * 18))
                    elif (x + y) % 2 == 1:
                        SCREEN.blit(IMAGES["lgrey"], (sx + x * 18, sy + (y - excess) * 18))

        #drawing the ghost peices as long as there are no
        #pieces under the block ie collidedown==False
        if collideDown(tetris_1.grid, tetris_1.block, tetris_1.px, tetris_1.py) == False:
            cls.drawGhostPiece(tetris_1, sx, sy)

        #drawing the pieces
        cls.drawPiece(tetris_1, sx, sy)              
        #drawing the grid
        cls.drawBoard(tetris_1, sx, sy)

    # drawing the held pieces
    # this function allows you to hold a piece
    # by hitting the respective hold button

    @staticmethod
    def drawHeld(tetris, sx, sy):
        grid, held = tetris.grid, tetris.held
        if held != None:
            # num = allpieces.index(held)
            _type = held.block_type()
            pos = []
            for x in range(4):
                for y in range(4):
                    if held.now_block()[x][y] > 0:
                        pos.append((x,y))

            SCREEN.blit(IMAGES["holdback"], (sx - 8, 159))

            
            if _type == 'I':
                for i in range(len(pos)):#if its an o piece different x and y position
                    SCREEN.blit(IMAGES["resizepics"][_type], (sx - 5 + int(pos[i][0] * 12), sy - 6 + int(pos[i][1] * 12)))
            elif _type == 'O':
                for i in range(len(pos)):#any other piece id the same x and y position
                    SCREEN.blit(IMAGES["resizepics"][_type], (sx - 5 + int(pos[i][0] * 12), sy + int(pos[i][1] * 12)))

            else:
                for i in range(len(pos)):#if its an i piece different x and y position
                    SCREEN.blit(IMAGES["resizepics"][_type], (sx + int(pos[i][0] * 12), sy + int(pos[i][1] * 12)))

    # drawing the next pieces 
    @staticmethod
    def drawNext(tetris, sx, sy): 
        grid, nextpieces = tetris.grid, tetris.buffer.now_list
        for i in range(5): # 5 different pieces 
            pos = []
            _type = nextpieces[i]._type
            b = nextpieces[i].now_block()
            for x in range(4):
                for y in range(4): #same procedure as the drawhed function
                    if b[x][y] > 0:
                        pos.append((x, y))
            
            if i == 0: # position 1
                SCREEN.blit(IMAGES["holdback"], (sx - 1, 159))            
                if _type == 'I': # i piece is different x and y pos
                    for i in range(len(pos)):
                        SCREEN.blit(IMAGES["resizepics"][_type], (sx + 1 + int(pos[i][0] * 12), 156 + int(pos[i][1] * 12)))
                elif _type == 'O': # o piece is different x and y pos
                    for i in range(len(pos)):
                        SCREEN.blit(IMAGES["resizepics"][_type], (sx + 1 + int(pos[i][0] * 12), 158 + int(pos[i][1] * 12)))                
                else: # every other piece is the same x and y pos              
                    for i in range(len(pos)):
                        SCREEN.blit(IMAGES["resizepics"][_type], (sx + 7 + int(pos[i][0] * 12), 159 + int(pos[i][1] * 12)))

            if i == 1: # position 2
                SCREEN.blit(IMAGES["nextback2"], (sx + 2, 230))
                if _type == 'I': # i piece is differnet x and y pos
                    for i in range(len(pos)):
                        SCREEN.blit(IMAGES["nextpics"][_type], (sx + 9 + int(pos[i][0] * 8), 235 + int(pos[i][1] * 8)))
                elif _type == 'O': # o piece is differnt x and y pos
                    for i in range(len(pos)):
                        SCREEN.blit(IMAGES["nextpics"][_type], (sx + 10 + int(pos[i][0] * 8), 235 + int(pos[i][1] * 8)))
                else: # every other piece same x and y pos
                    for i in range(len(pos)):
                        SCREEN.blit(IMAGES["nextpics"][_type], (sx + 13 + int(pos[i][0] * 8), 235 + int(pos[i][1] * 8)))

            if i >= 2: # position 3, 4, 5
                SCREEN.blit(IMAGES["nextback3"], (sx + 4, 288 + 52 * (i - 2)))
                if _type == 'I': # same as above
                    for j in range(len(pos)):
                        SCREEN.blit(IMAGES["nextpics"][_type], (sx + 9 + int(pos[j][0] * 8), 288 + (i - 2) * 51 + int(pos[j][1] * 8)))
                elif _type == 'O': # same as above
                    for j in range(len(pos)):
                        SCREEN.blit(IMAGES["nextpics"][_type], (sx + 9 + int(pos[j][0] * 8), 292 + (i - 2) * 51 + int(pos[j][1] * 8)))
                else: # same as above
                    for j in range(len(pos)):
                        SCREEN.blit(IMAGES["nextpics"][_type], (sx + 12 + int(pos[j][0] * 8), 292 + (i - 2) * 51 + int(pos[j][1] * 8)))

    #draws the ghost piece at where harddrop will take place
    #ghost goes where block will be when you harddrop
    @staticmethod
    def drawGhostPiece(tetris, sx, sy):
        grid, block, px, py = tetris.grid, tetris.block, tetris.px, tetris.py
        y = hardDrop(grid, block, px, py)
        py += y
        excess = len(grid[0]) - GRID_DEPTH
        b = block.now_block()
        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if b[x][y] > 0:
                    if GRID_WIDTH > px + x > -1 and len(grid[0]) > py + y > -1:
                        drawGhost(sx, sy, px + x, py + y - excess)
                        
    #draws the number of lines sent
    @staticmethod
    def drawNumbers(tetris, sx, sy):
        grid, sent = tetris.grid, tetris.sent
        number_digits = []

        sent = int(sent)
        while sent != 0:
            number_digits.append(sent % 10)
            sent /= 10
            sent = int(sent)

        if len(number_digits) == 0:
            number_digits.append(0)

        SCREEN.blit(IMAGES["sentback"], (sx - 12, sy))

        # print(number_digits)

        if len(number_digits) == 1:
            SCREEN.blit(IMAGES["numbers"][number_digits[0]], (sx, sy))

        elif len(number_digits) == 2:

            if number_digits[1] == 1:
                # blitting the IMAGES["numbers"] at the poisition in IMAGES["numbers"] list
                SCREEN.blit(IMAGES["numbers"][number_digits[1]], (sx - 14, sy))
                SCREEN.blit(IMAGES["numbers"][number_digits[0]], (sx + 7, sy))
            else:
                SCREEN.blit(IMAGES["numbers"][number_digits[1]], (sx - 14, sy))
                SCREEN.blit(IMAGES["numbers"][number_digits[0]], (sx + 14, sy))

        elif len(number_digits) == 3:
            if number_digits[2] == 1:
                SCREEN.blit(IMAGES["numbers"][number_digits[2]], (sx - 26, sy))
                SCREEN.blit(IMAGES["numbers"][number_digits[1]], (sx - 6, sy))
                SCREEN.blit(IMAGES["numbers"][number_digits[0]], (sx + 18, sy))
            else:
                SCREEN.blit(IMAGES["numbers"][number_digits[2]], (sx - 32, sy))
                SCREEN.blit(IMAGES["numbers"][number_digits[1]], (sx - 6, sy))
                SCREEN.blit(IMAGES["numbers"][number_digits[0]], (sx + 18, sy))

        else:
            raise ValueError('You get too many points!')

    # drawing the piece on the SCREEN
    # calls on the drawblock funct in order to draw
    # the piece on the SCREEN
    @staticmethod
    def drawPiece(tetris, sx, sy):
        grid, block, px, py = tetris.grid, tetris.block, tetris.px, tetris.py
        excess = len(grid[0]) - GRID_DEPTH
        b = block.now_block()
        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if b[x][y] > 0:
                    if -1 < px + x < 10 and -1 < py + y - excess < 20:
                        drawBlock(sx, sy, px + x, py + y - excess, b[x][y])

    # drawing the blocks on the grid
    # calls the drawblock function so that different IMAGES["numbers"] draw different colours on the SCREEN
    @staticmethod
    def drawBoard(tetris, sx, sy):
        grid = tetris.grid
        excess = len(grid[0]) - GRID_DEPTH
        for x in range(GRID_WIDTH):
            for y in range(excess, len(grid[0])):
                if grid[x][y] > 0:
                    drawBlock(sx, sy, x, y - excess, grid[x][y])


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
    def check_ko_win(tetris):
        if tetris.KO >= 3:
            return 1

        return 0

    @staticmethod
    def who_win(tetris_1, tetris_2):
        if tetris_2.KO > tetris_1.KO: # Checks who is the winner of the game
            return tetris_2.player.id # a is screebn.copy,endgame ends the game,2 is player 2 wins
        if tetris_1.KO > tetris_2.KO:
            return tetris_1.player.id # a is screebn.copy,endgame ends the game,1 is player 1 wins
        if tetris_1.KO == tetris_2.KO:
            if tetris_2.sent > tetris_1.sent:
                return tetris_2.player.id # a is screebn.copy,endgame ends the game,2 is player 2 wins
            elif tetris_1.sent > tetris_2.sent:
                return tetris_1.player.id # a is screebn.copy,endgame ends the game,1 is player 1 wins

            else:
                return tetris_1.player.id


class TetrisGame:
    #first function
    #will be used for choosing what map you want to play on

    def __init__(self):
        global SCREEN, IMAGES
        SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) # SCREEN is 800*600 

        IMAGES = load_imgs()

    def setmap(self):
        running = True
        #loading images
        
        #defining rectangles for collision checking
        map1 = pygame.Rect(155,75,200,200)
        map2 = pygame.Rect(439,75,200,200)
        map3 = pygame.Rect(155,309,200,200)
        map4 = pygame.Rect(439,309,200,200)
        buttons = [map1, map2, map3, map4]#preparing a buttons and names list to be zipped together
        names = ["none", "classic", "comboking", "lunchbox"]# 
        SCREEN.blit(IMAGES["back1"], (0, 0))#IMAGES["back1"] is the main background
        while running:
            mpos = pygame.mouse.get_pos()
            mb = pygame.mouse.get_pressed()
            for evnt in pygame.event.get():          
                if evnt.type == pygame.QUIT:
                    running = False

            for b, n in zip(buttons, names): #zipping buttons and names together       
                if b.collidepoint(mpos):   #for very easy collision checking            
                    if mb[0] == 1:
                        return n#return the name of the map chosen

            #this chunk of code is just making pretty pictures       
            if map1.collidepoint(mpos):
                SCREEN.blit(IMAGES["outline"], (149, 64))
            elif map2.collidepoint(mpos):
                SCREEN.blit(IMAGES["outline"], (431, 64))
            elif map3.collidepoint(mpos):
                SCREEN.blit(IMAGES["outline"], (149, 301))
            elif map4.collidepoint(mpos):
                SCREEN.blit(IMAGES["outline"], (431, 301))
            else:
                SCREEN.blit(IMAGES["back1"], (0, 0))#keeping it fresh
            
            pygame.display.flip() #necessities
    #gridchoice=""    

    #################################################################################
    def viewmap(self):#viewmap function
        running = True
        #making it look nice
    #defining rectangles for collision checking
        map1 = pygame.Rect(155, 75, 200, 200)
        map2 = pygame.Rect(439, 75, 200, 200)
        map3 = pygame.Rect(155, 309, 200, 200)
        map4 = pygame.Rect(439, 309, 200, 200)
        buttons = [map1, map2, map3, map4]#preparing a buttons and names list to be zipped together
        names = ["none", "classic", "comboking", "lunchbox"]# 
        SCREEN.blit(IMAGES["back1"], (0, 0))#back1 is the main background
        while running:

            for evnt in pygame.event.get():          
                if evnt.type == pygame.QUIT:
                    running = False

            mpos = pygame.mouse.get_pos()
            mb = pygame.mouse.get_pressed()
            #print mpos

            #for b,n in zip(buttons,names): #zipping buttons and names together       
                #if b.collidepoint(mpos):   #for very easy collision checking            
                    #if mb[0]==1:
                        

            #this chunk of code is just making pretty pictures       
            if map1.collidepoint(mpos):
                SCREEN.blit(IMAGES["outline"], (149, 64))
            elif map2.collidepoint(mpos):
                SCREEN.blit(IMAGES["outline"], (431, 64))
            elif map3.collidepoint(mpos):
                SCREEN.blit(IMAGES["outline"], (149, 301))
            elif map4.collidepoint(mpos):
                SCREEN.blit(IMAGES["outline"], (431, 301))
            else:
                SCREEN.blit(IMAGES["back1"], (0, 0))#keeping it fresh
            pygame.display.flip() #necessities

        return "menu"

    #instructions page
    def instructions(self):
        running = True
        SCREEN.blit(IMAGES["back2"], (0, 0))
        #SCREEN.blit(inst,(173,100))
        while running:
            for evnt in pygame.event.get():          
                if evnt.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
        return "menu"

    #menu page
    def menu(self, page):
        running = True
        myClock = pygame.time.Clock()
        button1 = pygame.Rect(320, 204, 146, 50)#start rect
        buttons = [pygame.Rect(325, y * 42 + 275, 135, 30) for y in range(3)]#other three rects 
        vals = ["viewmap", "instructions", "exit"]#values of other three rects
        
        
        SCREEN.blit(IMAGES["intro"], (0, 0))
        pygame.display.set_caption("Tetris Battle", "tetris battle")
        while running:
            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    return "exit"
            mpos = pygame.mouse.get_pos()
            mb = pygame.mouse.get_pressed()
            #print mpos

            #thank u for the code
            #zips button and vals and when
            #a collision and a click occurs
            #returns vals
            for r,v in zip(buttons, vals):
                if r.collidepoint(mpos):
                    #print r,v
                    if mb[0] == 1:
                        return v # page to go to
           
            if button1.collidepoint(mpos):
                SCREEN.blit(IMAGES["startbutton"], (319, 207))
                if mb[0] == 1:
                    return "start"#starting the game
                #making the game look pretty
            elif buttons[0].collidepoint(mpos):
                SCREEN.blit(IMAGES["setmapbutton"], (325, 274))
            elif buttons[1].collidepoint(mpos):
                SCREEN.blit(IMAGES["helpbutton"], (325, 317))
            elif buttons[2].collidepoint(mpos):
                SCREEN.blit(IMAGES["quitbutton"], (325, 360))
                if mb[0] == 1:
                    return "exit"#quitting the game
            else:
                SCREEN.blit(IMAGES["intro"], (0, 0))#reblit the background
            
            #draw.rect(SCREEN,(0,0,0),button1,2)
            myClock.tick(FPS)            
            pygame.display.flip()

    def endgame(self, a, winner):
        raise NotImplementedError
    #main game function
    def start(self, myClock, timer2p):
        raise NotImplementedError
    

class TetrisGameDouble(TetrisGame):


    def endgame(self, a, winner):#parameters
        counter = 0
        # pretty stuff
        while True:
            counter += 1
            SCREEN.blit(a, (0, 0))
            SCREEN.blit(IMAGES["transparent"], (110, 135))
            SCREEN.blit(IMAGES["transparent"], (494, 135))
            SCREEN.blit(IMAGES["pics"][winner - 1], (135, 230))
            SCREEN.blit(IMAGES["pics"][(2 - winner)], (500, 230))
            pygame.display.flip()
            if counter == 1000: # time waiting
                return "menu"

    def start(self, myClock, timer2p):#parameters are FP/s rate and timer countdown
    ################################################################################
        
        gridchoice = self.setmap()#calling the setmap function for a choice of grid
        timer2p.tick()
        #the code below is what happens when you set a map
        #different maps = differnet grids
               
        pygame.init() #for music
        battlemusic = pygame.mixer.Sound(MUSIC_PATH)#importing sound file

        #SCREEN=pygame.display.set_mode((800,600))
        running = True #necessity
        SCREEN.blit(IMAGES["gamescreen"], (0, 0))#blitting the main background
        # a = SCREEN.copy()#used for image coverage

        #these two used for countdown
        #of the timer
        time = MAX_TIME
        delaytime = time

        info_dict_1 = {
        "id": 1,
        "hold": pygame.K_c,
        "drop": pygame.K_SPACE,
        "rotate_right": pygame.K_UP,
        "rotate_left": pygame.K_z,
        "right": pygame.K_RIGHT,
        "left": pygame.K_LEFT,
        "down": pygame.K_DOWN
        }

        info_dict_2 = {
        "id": 2,
        "hold": pygame.K_e,
        "drop": pygame.K_w,
        "rotate_right": pygame.K_u,
        "rotate_left": pygame.K_q,
        "right": pygame.K_k,
        "left": pygame.K_h,
        "down": pygame.K_j
        }


        tetris_1 = Tetris(Player(info_dict_1), gridchoice)
        tetris_2 = Tetris(Player(info_dict_2), gridchoice)
        
        #main loop
        while running:
            # battlemusic.play()#plays music
            
            tetris_1.natural_down()
            tetris_2.natural_down()

            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    running = False
                tetris_1.trigger(evt)
                tetris_2.trigger(evt)

            tetris_1.move()
            tetris_2.move()

            # if kocounter1>=1:
            #     kocounter1+=1
            # if kocounter2>=1:
            #     kocounter2+=1

            if tetris_1.check_fallen():
                # print("fall")
                # print(tetris_1.stopcounter)
                # print(tetris_1.px, tetris_1.py)
                # compute the scores and attack the opponent
                scores = tetris_1.clear()

                tetris_2.add_attacked(scores)

                # Renderer.drawBoard(tetris_2, 495, 138)

                Renderer.drawCombo(tetris_1, IMAGES["combos"], 164 - 120, 377 + 60)

                Renderer.drawTetris(tetris_1, 164 + 150, 377 + 100)
                Renderer.drawTspin(tetris_1, 164 + 140, 377 + 100)
                Renderer.drawBack2Back(tetris_1, 164 + 150, 377 + 60)

                # pygame.display.flip()

                if tetris_1.check_KO():
                    Renderer.drawBoard(tetris_1, 112, 138)
                    tetris_2.update_ko()
                    tetris_1.clear_garbage()

                    SCREEN.blit(IMAGES["ko"], (140, 233))
                    SCREEN.blit(IMAGES["transparent"], (110, 135))


                    # SCREEN.blit(kos[tetris_2.get_KO() - 1], (426, 235))
                    # pygame.display.flip()
                    # pygame.display.update(r)
                    pygame.display.flip()
                    freeze(0.5)

                tetris_1.new_block()

            Renderer.drawGameScreen(tetris_1)

            if tetris_2.check_fallen():
                # compute the scores and attack the opponent
                scores = tetris_2.clear()

                tetris_1.add_attacked(scores)

                # Renderer.drawBoard(tetris_1, 112, 138)

                Renderer.drawCombo(tetris_2, IMAGES["combos"], 535 - 120, 377 + 60)

                Renderer.drawTetris(tetris_2, 535 + 150, 377 + 100)
                Renderer.drawTspin(tetris_2, 535 + 140, 377 + 100)
                Renderer.drawBack2Back(tetris_2, 535 + 150, 377 + 60)

                # pygame.display.flip()

                if tetris_2.check_KO():
                    Renderer.drawBoard(tetris_2, 495, 138)

                    tetris_1.update_ko()
                    tetris_2.clear_garbage()

                    SCREEN.blit(IMAGES["ko"], (527, 233))
                    SCREEN.blit(IMAGES["transparent"], (494, 135))

                    # SCREEN.blit(kos[tetris_1.get_KO() - 1], (44, 235))
                    # pygame.display.update(r)
                    pygame.display.flip()

                    freeze(0.5)

                tetris_2.new_block()

            Renderer.drawGameScreen(tetris_2)

            if tetris_1.get_KO() > 0:
                SCREEN.blit(IMAGES["kos"][tetris_1.get_KO() - 1], (44, 235))
                # pygame.display.flip()

            if tetris_2.get_KO() > 0:
                SCREEN.blit(IMAGES["kos"][tetris_2.get_KO() - 1], (426, 235))
                # pygame.display.flip()

                
            #parameters for getting position of
            #falling block
            # positions1 = getPositions(player_1.block, player_1.px, player_1.py)
            # positions2 = getPositions(player_2.block, player_2.px, player_2.py)     

            Renderer.drawScreen(tetris_1, 112, 138)

            Renderer.drawScreen(tetris_2, 495, 138)

            # pygame.display.flip()

            if Judge.check_ko_win(tetris_1):
                # exit()
                b = SCREEN.copy()
                return [b, "endgame", tetris_1.get_id()]
            if Judge.check_ko_win(tetris_2):
                b = SCREEN.copy()
                return [b, "endgame", tetris_2.get_id()]
            
            if time >= 0:
                time -= timer2p.tick()
            else:
                time = 0
                drawTime2p(time)
                pygame.display.flip()
                a = SCREEN.copy()
                win_player = Judge.who_win(tetris_1, tetris_2)
                
                return [a, "endgame", win_player] # a is screebn.copy,endgame ends the game,1 is player 1 wins

            drawTime2p(time)
            
            # if player_2.check_combo():
            
           
            #time goes until it hits zero
            #when it hits zero return endgame SCREEN
            myClock.tick(FPS)   
            pygame.display.flip()

        pygame.quit()

class TetrisGameSingle(TetrisGame):
    def endgame(self, a, winner):#parameters
        counter = 0
        # pretty stuff
        while True:
            counter += 1
            SCREEN.blit(a, (0, 0))
            SCREEN.blit(IMAGES["transparent"], (110, 135))
            # SCREEN.blit(IMAGES["transparent"], (494, 135))
            # SCREEN.blit(IMAGES["pics"][winner - 1], (135, 230))
            # SCREEN.blit(IMAGES["pics"][(2 - winner)], (500, 230))
            pygame.display.flip()
            if counter == 1000: # time waiting
                return "menu"

    def start(self, myClock, timer2p):#parameters are FP/s rate and timer countdown
    ################################################################################

        gridchoice = self.setmap()#calling the setmap function for a choice of grid

        timer2p.tick()
        #the code below is what happens when you set a map
        #different maps = differnet grids

        pygame.init() #for music

        battlemusic = pygame.mixer.Sound(MUSIC_PATH)#importing sound file
        #SCREEN=pygame.display.set_mode((800,600))
        running = True #necessity
        SCREEN.blit(IMAGES["gamescreen"], (0, 0))#blitting the main background
        # a = SCREEN.copy()#used for image coverage

        #these two used for countdown
        #of the timer
        time = MAX_TIME
        delaytime = time

        info_dict_1 = {
        "id": 1,
        "hold": pygame.K_c,
        "drop": pygame.K_SPACE,
        "rotate_right": pygame.K_UP,
        "rotate_left": pygame.K_z,
        "right": pygame.K_RIGHT,
        "left": pygame.K_LEFT,
        "down": pygame.K_DOWN
        }

        tetris_1 = Tetris(Player(info_dict_1), gridchoice)
        # print("213")
        
        #main loop
        while running:
            # battlemusic.play()#plays music
            
            tetris_1.natural_down()

            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    running = False
                tetris_1.trigger(evt)

            tetris_1.move()

            if tetris_1.check_fallen():
                # print("fall")
                # print(tetris_1.stopcounter)
                # print(tetris_1.px, tetris_1.py)
                # compute the scores and attack the opponent
                scores = tetris_1.clear()

                # tetris_2.add_attacked(scores)

                Renderer.drawCombo(tetris_1, IMAGES["combos"], 164 - 120, 377 + 60)

                Renderer.drawTetris(tetris_1, 164 + 150, 377 + 100)
                Renderer.drawTspin(tetris_1, 164 + 140, 377 + 100)
                Renderer.drawBack2Back(tetris_1, 164 + 150, 377 + 60)

                if tetris_1.check_KO():
                    # tetris_2.update_ko()
                    Renderer.drawBoard(tetris_1, 112, 138)

                    tetris_1.clear_garbage()

                    b = SCREEN.copy()

                    SCREEN.blit(IMAGES["ko"], (140, 233))
                    SCREEN.blit(IMAGES["transparent"], (110, 135))

                    # SCREEN.blit(kos[tetris_2.get_KO() - 1], (426, 235))
                    pygame.display.flip()

                    freeze(0.5)

                    return [b, "endgame", tetris_1.get_id()]

                tetris_1.new_block()

            Renderer.drawGameScreen(tetris_1)
                
            #parameters for getting position of
            #falling block
            # positions1 = getPositions(player_1.block, player_1.px, player_1.py)
            # positions2 = getPositions(player_2.block, player_2.px, player_2.py)     

            Renderer.drawScreen(tetris_1, 112, 138)

            SCREEN.blit(IMAGES["transparent"], (494, 135))

            # pygame.display.update(r)

            if time >= 0:
                time -= timer2p.tick()
            else:
                time = 0

                drawTime2p(time)

                pygame.display.flip()

                a = SCREEN.copy()
                
                return [a, "endgame", 1] # a is screebn.copy,endgame ends the game,1 is player 1 wins

            drawTime2p(time)
            
            # if player_2.check_combo():
            
           
            #time goes until it hits zero
            #when it hits zero return endgame SCREEN
            myClock.tick(FPS)   
            pygame.display.flip()

        pygame.quit()



class ComEvent:
    def __init__(self):
        self._pre_evt_list = []
        self._now_evt_list = []

    def get(self):
        return self._now_evt_list

    def set(self, actions):
        # action: list of int

        self._now_evt_list = []

        for evt in self._pre_evt_list:
            if evt.type == pygame.KEYDOWN or evt.type == "HOLD":
                if evt.key not in actions:
                # if evt.key != action:
                    self._now_evt_list.append(ComEvt(pygame.KEYUP, evt.key))

        for action in actions:
            hold = 0
            for evt in self._pre_evt_list:
                if evt.key == action:
                    if evt.type == pygame.KEYDOWN or evt.type == "HOLD":
                        hold = 1
                        self._now_evt_list.append(ComEvt("HOLD", action))
            if not hold:
                self._now_evt_list.append(ComEvt(pygame.KEYDOWN, action))

        self._pre_evt_list = self._now_evt_list

    def reset(self):
        del self._pre_evt_list[:]
        del self._now_evt_list[:]

class ComEvt:

    def __init__(self, type_, key_):
        self._type = type_
        self._key = key_

    @property
    def key(self):
        return self._key

    @property
    def type(self):
        return self._type

class TetrisSingleInterface:

    metadata = {'render.modes': ['human', 'rgb_array'], 
                'obs_type': ['image', 'grid']}

    #######################################
    # observation type: 
    # "image" => screen shot of the game 
    # "grid"  => the row data array of the game

    def __init__(self, gridchoice="none", obs_type="image", mode="rgb_array"):

        global SCREEN, IMAGES

        if mode == "rgb_array":
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) # SCREEN is 800*600 

        IMAGES = load_imgs()

        self._obs_type = obs_type

        self._mode = mode

        self.time = MAX_TIME

        self._action_meaning = {
            # 0: "NOOP",
            # 0: "hold",
            # 1: "drop",
            # 2: "rotate_right",
            0: "rotate_left",
            1: "right",
            2: "left",
            3: "down" 
        }

        self._n_actions = len(self._action_meaning)

        # print(self.action_space.n)

        self._action_set = list(range(self._n_actions))

        info_dict_1 = {
            "id": 1,
            # "hold": 0,
            # "drop": 1,
            # "rotate_right": 2,
            # "rotate_left": 3,
            # "right": 4,
            # "left": 5,
            # "down": 6
            }

        for k, v in self._action_meaning.items():
            info_dict_1[v] = k

        # print(info_dict_1)

        self.tetris_1 = Tetris(Player(info_dict_1), gridchoice)


        self.com_event = ComEvent()

        self.myClock = pygame.time.Clock() # this will be used to set the FPS(frames/s) 

        self.timer2p = pygame.time.Clock() # this will be used for counting down time in our game

    @property 
    def action_meaning(self):
        return self._action_meaning

    @property
    def n_actions(self):
        return self._n_actions

    @property
    def action_set(self):
        return self._action_set

    def screen_size(self):
        # return (x, y)
        return [SCREENHEIGHT, SCREENWIDTH]
    
    def get_screen_shot(self):
        ob = pygame.surfarray.array3d(pygame.display.get_surface())
        ob = np.transpose(ob, (1, 0, 2))
        return ob

    def get_seen_grid(self):
        return self.tetris_1.get_grid()

    def get_obs(self):
        if self._obs_type == "grid":
            return self.get_seen_grid()
        elif self._obs_type == "image":
            img = self.get_screen_shot()
        return img

    def random_action(self):
        return random.randint(0, self._n_actions - 1)
        
    def act(self, action):
        # Execute one time step within the environment

        end = 0
        scores = 0

        tetris_1 = self.tetris_1

        tetris_1.natural_down()

        self.com_event.set([action])

        for evt in self.com_event.get():
            tetris_1.trigger(evt)

        tetris_1.move()

        if tetris_1.check_fallen():
            # print("fall")
            # print(tetris_1.stopcounter)
            # print(tetris_1.px, tetris_1.py)
            # compute the scores and attack the opponent
            scores = tetris_1.clear()

            # tetris_2.add_attacked(scores)

            Renderer.drawCombo(tetris_1, IMAGES["combos"], 164 - 120, 377 + 60)

            Renderer.drawTetris(tetris_1, 164 + 150, 377 + 100)
            Renderer.drawTspin(tetris_1, 164 + 140, 377 + 100)
            Renderer.drawBack2Back(tetris_1, 164 + 150, 377 + 60)

            if tetris_1.check_KO():
                # tetris_2.update_ko()
                Renderer.drawScreen(tetris_1, 112, 138)
                tetris_1.clear_garbage()

                SCREEN.blit(IMAGES["ko"], (140, 233))
                SCREEN.blit(IMAGES["transparent"], (110, 135))

                # screen.blit(kos[tetris_2.get_KO() - 1], (426, 235))
                pygame.display.flip()

                freeze(0.5)

                scores -= 1

                end = 1

            tetris_1.new_block()

        Renderer.drawGameScreen(tetris_1)
            
        #parameters for getting position of
        #falling block
        # positions1 = getPositions(player_1.block, player_1.px, player_1.py)
        # positions2 = getPositions(player_2.block, player_2.px, player_2.py)     

        Renderer.drawScreen(tetris_1, 112, 138)

        SCREEN.blit(IMAGES["transparent"], (494, 135))

        # pygame.display.flip()

        if self.time >= 0:
            self.time -= self.timer2p.tick()
        else:
            self.time = 0
            end = 1

        drawTime2p(self.time)
        
        # if player_2.check_combo():
        
       
        #time goes until it hits zero
        #when it hits zero return endgame screen
        
        pygame.display.flip()
        self.myClock.tick(FPS)  

        ob = self.get_obs()

        height_sum, diff_sum, max_height, holes = get_infos(self.get_seen_grid())

        if self.tetris_1.is_fallen:
            infos = {'height_sum': height_sum, 
                     'diff_sum': diff_sum,
                     'max_height': max_height,
                     'holes': holes}
        else:
            infos = {}

        if end:
            self.reset()

        return ob, scores, end, infos

    def reset(self):
        # Reset the state of the environment to an initial state

        self.tetris_1.reset()

        self.com_event.reset()

        tetris_1 = self.tetris_1
        
        self.time = MAX_TIME

        SCREEN.blit(IMAGES["gamescreen"], (0, 0)) # blitting the main background

        Renderer.drawGameScreen(tetris_1)
            
        #parameters for getting position of
        #falling block
        # positions1 = getPositions(player_1.block, player_1.px, player_1.py)
        # positions2 = getPositions(player_2.block, player_2.px, player_2.py)     

        Renderer.drawScreen(tetris_1, 112, 138)

        SCREEN.blit(IMAGES["transparent"], (494, 135))

        # pygame.display.flip()

        drawTime2p(self.time)
        
        # if player_2.check_combo():
        
       
        #time goes until it hits zero
        #when it hits zero return endgame screen
        
        pygame.display.flip()
        self.myClock.tick(FPS)  

        ob = self.get_obs()

        return ob
