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
import math

import numpy as np

from .settings import *

from .tetris_core import TetrisCore

from copy import deepcopy

import time as t
from collections import Counter

from .sound_manager import SoundManager


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


def freeze(last_time):
    start = t.time()
    while t.time() - start < last_time:
        pass

class Tetris(object):
    def __init__(self, player, gridchoice, training=False):

        # if gridchoice == "none":
        #     self.o_grid = [[0] * GRID_DEPTH for i in range(GRID_WIDTH)]

        # if gridchoice == "classic":
        #     self.o_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 3],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # if gridchoice == "comboking":
        #     self.o_grid = [[0, 0, 0, 0, 0, 5, 5, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        #                   [0, 0, 0, 0, 0, 6, 6, 6, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 4, 5],
        #                   [0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        #                   [0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
        #                   [0, 0, 0, 0, 0, 6, 6, 6, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 4, 5],
        #                   [0, 0, 0, 0, 0, 5, 5, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]

        # if gridchoice == "lunchbox":
        #     self.o_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 5, 5, 5, 5, 5, 5, 5, 1],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 2, 2, 2, 2, 2, 2, 5, 1],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 2, 4, 4, 4, 4, 2, 5, 1],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 5, 2, 4, 4, 4, 4, 2, 5, 6],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 5, 2, 2, 2, 2, 2, 2, 5, 6],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 5, 5, 5, 5, 5, 5, 5, 5, 6],
        #                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]]

        self.core = TetrisCore(gridchoice=gridchoice)

        self.player = player
        self.sound_manager = SoundManager.get_instance()

        if training == True:
            self.sound_manager.mute()

        self.reset()

    @property
    def grid(self):
        return self.core.grid

    @property
    def held(self):
        return self.core.held

    @property
    def buffer(self):
        return self.core.buffer

    @property
    def block(self):
        return self.core.block

    @property
    def px(self):
        return self.core.px

    @property
    def py(self):
        return self.core.py

    def reset(self):
        # self.grid = deepcopy(self.o_grid)

        self.core.reset()

        self.oldko = 0 # these two used to keep track of ko's

        self._n_used_block = 1

        # self.buffer = Buffer()
        # list of the held piece
        # self.held = None
        # self.block = self.buffer.new_block()

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

        # self.px = 4
        # self.py = -2

        # DEFINING VARIABLES
        self.cleared = 0
        self.kocounter = 0
        self.stopcounter = 0

        # self.isholded = 0

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

    def get_diff_grid(self):
        return self.core.get_diff_grid()

        # excess = len(self.grid[0]) - GRID_DEPTH
        # return_grids = np.zeros(shape=(GRID_WIDTH, GRID_DEPTH), dtype=np.float32)

        # block, px, py = self.block, self.px, self.py
        # excess = len(self.grid[0]) - GRID_DEPTH
        # b = block.now_block()

        # for i in range(len(self.grid)):
        #     return_grids[i] = np.array(self.grid[i][excess:GRID_DEPTH], dtype=np.float32)
        # return_grids[return_grids > 0] = 1

        # diff_grid = np.zeros(shape=(GRID_WIDTH), dtype=np.float32)
        # for col in range(return_grids.shape[0]):
        #     for row in range(return_grids.shape[1]):
        #         if return_grids[col, row] >= 1:
        #             diff_grid[col] = row - py

        # informations = np.zeros(shape=((len(PIECE_NUM2TYPE) - 1)*2 + 2), dtype=np.float32)
        # # current block
        # informations[PIECE_TYPE2NUM[self.block.block_type()] - 1] = 1

        # # hold block
        # if self.held != None:
        #     informations[len(PIECE_NUM2TYPE) - 1 + PIECE_TYPE2NUM[self.held.block_type()] - 1] = 1
    
        # informations[len(PIECE_NUM2TYPE) - 1 + 0] = px
        # informations[len(PIECE_NUM2TYPE) - 1 + 1] = py

        # return_grids = np.concatenate((diff_grid, informations), axis=0)

        # return np.transpose(return_grids)

    def get_grid(self):
        return self.core.get_grid()
        # excess = len(self.grid[0]) - GRID_DEPTH
        # return_grids = np.zeros(shape=(GRID_WIDTH, GRID_DEPTH), dtype=np.float32)

        # block, px, py = self.block, self.px, self.py
        # excess = len(self.grid[0]) - GRID_DEPTH
        # b = block.now_block()

        # for i in range(len(self.grid)):
        #     return_grids[i] = np.array(self.grid[i][excess:GRID_DEPTH], dtype=np.float32)
        # return_grids[return_grids > 0] = 1

        # add_y = hardDrop(self.grid, self.block, self.px, self.py)

        # for x in range(BLOCK_WIDTH):
        #     for y in range(BLOCK_LENGTH):
        #         if b[x][y] > 0:
        #             # draw ghost grid
        #             if -1 < px + x < 10 and -1 < py + y + add_y - excess < 20:
        #                 return_grids[px + x][py + y + add_y - excess] = 0.3

        #             if -1 < px + x < 10 and -1 < py + y - excess < 20:
        #                 return_grids[px + x][py + y - excess] = 0.7

        # informations = np.zeros(shape=(len(PIECE_NUM2TYPE) - 1, GRID_DEPTH), dtype=np.float32)
        # if self.held != None:
        #     informations[PIECE_TYPE2NUM[self.held.block_type()] - 1][0] = 1

        # nextpieces = self.buffer.now_list
        # for i in range(5): # 5 different pieces
        #     _type = nextpieces[i].block_type()
        #     informations[PIECE_TYPE2NUM[_type] - 1][i + 1] = 1
        # # index start from 6

        # informations[0][6] = self.sent / 100
        # informations[1][6] = self.combo / 10
        # informations[2][6] = self.pre_back2back
        # informations[3][6] = self._attacked / GRID_DEPTH
        # # informations[3][7] = self.time / MAX_TIME

        # return_grids = np.concatenate((return_grids, informations), axis=0)

        # return np.transpose(return_grids, (1, 0))

    def get_board(self):
        return self.core.get_board()

        # excess = len(self.grid[0]) - GRID_DEPTH
        # return_grids = np.zeros(shape=(GRID_WIDTH, GRID_DEPTH), dtype=np.float32)

        # block, px, py = self.block, self.px, self.py
        # excess = len(self.grid[0]) - GRID_DEPTH
        # # b = block.now_block()

        # for i in range(len(self.grid)):
        #     return_grids[i] = np.array(self.grid[i][excess:GRID_DEPTH], dtype=np.float32)
        # return_grids[return_grids > 0] = 1
        # # for x in range(BLOCK_WIDTH):
        # #     for y in range(BLOCK_LENGTH):
        # #         if b[x][y] > 0:
        # #             if -1 < px + x < 10 and -1 < py + y - excess < 20:
        # #                 return_grids[px + x][py + y - excess] = 0.5


        # return return_grids

    def get_maximum_height(self):
        return self.core.get_maximum_height()
        # max_height = 0
        # for i in range(0, len(self.grid)):  # Select a column
        #     for j in range(0, len(self.grid[0])):  # Search down starting from the top of the board
        #         if int(self.grid[i][j]) > 0:  # Is the cell occupied?
        #             max_height = max(max_height, len(self.grid[0]) - j)
        #             break
        # return max_height

    def reset_pos(self):
        self.reset_pos()
        # self.px = 4
        # self.py = -2 + len(self.grid[0]) - GRID_DEPTH

    def get_id(self):
        return self.player.id

    def add_attacked(self, attacked):
        self._attacked += attacked
        self._attacked = min(self._attacked, GRID_DEPTH)

    def natural_down(self):
        if self.LAST_NATRUAL_FALL_TIME >= NATRUAL_FALL_FREQ:
            self.core.natural_down()
            # if collideDown(self.grid, self.block, self.px, self.py) == False:
            #     self.stopcounter = 0
            #     # self.block.move_down()
            #     self.py += 1
            #     # pass

            self.LAST_NATRUAL_FALL_TIME = 0
        # else:
        #     self.natural_down_counter += 1

    def trigger(self, evt):
        # if (hasattr(evt, "key")):
        #     print(evt.key)
        if evt.type == pygame.KEYDOWN:
            if evt.key == self.player.rotate_right and self.LAST_ROTATE_TIME >= ROTATE_FREQ: # rotating
                # self.block, self.px, self.py, self.tspin = rotate(self.grid, self.block, self.px, self.py, _dir=1)
                self.tspin = self.core.rotate(_dir=1)
                self.LAST_ROTATE_TIME = 0
                self.sound_manager.play_sound('rotate')

            if evt.key == self.player.rotate_left and self.LAST_ROTATE_TIME >= ROTATE_FREQ: # rotating
                # self.block, self.px, self.py, self.tspin = rotate(self.grid, self.block, self.px, self.py, _dir=-1)
                self.tspin = self.core.rotate(_dir=-1)
                self.LAST_ROTATE_TIME = 0
                self.sound_manager.play_sound('rotate')

            if evt.key == self.player.drop: # harddrop
                # y = hardDrop(self.grid, self.block, self.px, self.py) # parameters
                # # self.block.move_down(y)
                # self.py += y
                self.core.hardDrop()
                # self.stopcounter = COLLIDE_DOWN_COUNT
                # self.LAST_FALL_DOWN_TIME = -FALL_DOWN_FREQ
                self.LAST_FALL_DOWN_TIME = FALL_DOWN_FREQ
                self.sound_manager.play_sound('harddrop')

            if evt.key == self.player.hold: #holding

                if self.core.hold():
                    self.sound_manager.play_sound('hold')

                # if not self.isholded:

                #     self.block, self.held = hold(self.block, self.held, self.buffer) # parameters
                #     self.held.reset()
                #     self.reset_pos()
                #     self.isholded = 1
                #     self.sound_manager.play_sound('hold')

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

            if evt.key == pygame.K_a:
                # self.build_chance(self.grid, height=1, holes=2, chance_type='left')
                self.core.build_chance(height=1, holes=2, chance_type='left')

            if evt.key == pygame.K_s:
                # self.build_chance(self.grid, height=1, holes=2, chance_type='right')
                self.core.build_chance(height=1, holes=2, chance_type='right')

            if evt.key == pygame.K_d:
                # self.build_chance(self.grid, height=1, holes=3, chance_type='left')
                self.core.build_chance(height=1, holes=3, chance_type='left')

            if evt.key == pygame.K_f:
                # self.build_chance(self.grid, height=1, holes=3, chance_type='right')
                self.core.build_chance(height=1, holes=3, chance_type='right')

            if evt.key == pygame.K_v:
                # self.build_chance(self.grid, height=1, holes=4, chance_type='left')
                self.core.build_chance(height=1, holes=4, chance_type='left')

            if evt.key == pygame.K_b:
                # self.build_chance(self.grid, height=1, holes=4, chance_type='right')
                self.core.build_chance(height=1, holes=4, chance_type='right')

        return 'none'

    # move function
    # when respective buttons are pressed
    def move(self):
        # if keys[self.right]:
        if self.pressedRight and self.LAST_MOVE_SHIFT_TIME > MOVE_SHIFT_FREQ:
            if self.core.move_right():
                self.LAST_MOVE_SHIFT_TIME = 0

            # if collideRight(self.grid, self.block, self.px, self.py) == False:
            #     self.LAST_MOVE_SHIFT_TIME = 0

            #     # self.block.move_right()
            #     self.px += 1

        if self.pressedLeft and self.LAST_MOVE_SHIFT_TIME > MOVE_SHIFT_FREQ:
            if self.core.move_left():
                self.LAST_MOVE_SHIFT_TIME = 0

            # if collideLeft(self.grid, self.block, self.px, self.py) == False:
            #     self.LAST_MOVE_SHIFT_TIME = 0

            #     # self.block.move_left()
            #     self.px -= 1

        if self.pressedDown and self.LAST_MOVE_DOWN_TIME > MOVE_DOWN_FREQ:
            if self.core.move_down():
                self.LAST_MOVE_DOWN_TIME = 0

            # if collideDown(self.grid, self.block, self.px, self.py) == False:
            #     self.LAST_MOVE_DOWN_TIME = 0
            #     # self.stopcounter = 0

            #     # self.block.move_down()
            #     self.py += 1

    def check_fallen(self):
        # if collideDown(self.grid, self.block, self.px, self.py) == True:
        if self.core.collideDown() == True:
            # self.stopcounter += 1
            if self.LAST_FALL_DOWN_TIME >= FALL_DOWN_FREQ:
                self._is_fallen = 1
                # put_block_in_grid(self.grid, self.block, self.px, self.py)
                self.core.put_block_in_grid()
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

        cleared, bomb_cleared = self.core.get_cleared()

        if cleared >= 1: # for sending lines
            self.sound_manager.play_sound('clear')
            self.combo += 1

            if self.combo == 1:
                self.sound_manager.play_sound('combo1')
            elif self.combo == 2:
                self.sound_manager.play_sound('combo2')
            elif self.combo == 3:
                self.sound_manager.play_sound('combo3')
            elif self.combo == 4:
                self.sound_manager.play_sound('combo4')
            elif self.combo == 5:
                self.sound_manager.play_sound('combo5')
            elif self.combo >= 6:
                self.sound_manager.play_sound('combo6')

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

        self.cleared = cleared
        self.sent += scores

        real_attacked = max(0, self._attacked - scores)

        self.build_garbage(real_attacked)

        self._attacked = 0

        return scores

    def check_KO(self):
        return self.core.check_KO()

    def clear_garbage(self):
        self.core.clear_garbage
        # garbage = 0
        # # excess = len(grid[0]) - GRID_DEPTH
        # for y in range(0, len(self.grid[0])):
        #     for x in range(GRID_WIDTH):
        #         if self.grid[x][y] == 8 or self.grid[x][y] == 9:
        #             garbage += 1
        #             self.grid[x].pop(y)
        #             self.grid[x] = [0] + self.grid[x]

    # def build_chance(self, grid, height, holes=2, chance_type='random'):
    #     for y in range(0, height):
    #         hole_pos = []
    #         if chance_type  == 'random':
    #             hole_pos = random.choices(range(1, GRID_WIDTH), k=holes)
    #         elif chance_type == 'left':
    #             hole_pos = range(0, holes)
    #         elif chance_type == 'right':
    #             hole_pos = range(GRID_WIDTH - holes, GRID_WIDTH)

    #         for i in range(GRID_WIDTH):
    #             if i not in hole_pos:
    #                 grid[i] = grid[i] + [1]
    #             else:
    #                 grid[i] = grid[i] + [0]


    def build_garbage(self, attacked):
        self.core.build_garbage(attacked)
        # garbage_size = min(attacked, GRID_DEPTH)
        # for y in range(0, garbage_size):
        #     rand_pos = random.randint(0, GRID_WIDTH - 1)
        #     for i in range(GRID_WIDTH):
        #         # del player.grid[i][y] # deletes top of grid
        #         # adds garbage lines at the bottom
        #         if i == rand_pos :
        #             grid[i] = grid[i] + [9] # bomb block
        #         else:
        #             grid[i] = grid[i] + [8]

        # # return grid

    def check_combo(self):
        return self.combo - self.oldcombo >= 1

    def new_block(self):
        # self.block = self.buffer.new_block()
        # self.reset_pos()
        # self.isholded = 0
        self.core.new_block()
        self.tspin = 0
        self._n_used_block += 1

    def update_ko(self):
        self.oldko = self._KO
        self._KO += 1

    def update_combo(self):
        self.oldcombo = self.combo
        self.combo += 1
