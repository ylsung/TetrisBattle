from .settings import *
from .tetris import collideDown, hardDrop
import time as t
import pygame

class Renderer(object):

    def __init__(self, screen, images):
        self.screen = screen
        self.images = images

    # this function draws the combo number, return True if sucessfully draw
    def drawCombo(self, tetris, sx, sy):
        
        combos = self.images["combos"]
        if tetris.combo > 0:
            r = self.screen.blit(combos[min(tetris.combo, MAX_COMBO) - 1], (sx, sy)) #blits the combo number

            pygame.display.update(r)

            tetris.LAST_COMBO_DRAW_TIME = 0

            return True

        else:
            tetris.oldcombo = 0

        tetris.combo_counter = 0

        return False

    def drawTetris(self, tetris, sx, sy):
        if tetris.tetris:
            r = self.screen.blit(self.images["tetris_img"], (sx, sy))
            
            pygame.display.update(r)

            tetris.LAST_TETRIS_DRAW_TIME = 0
            tetris.tetris_drawing = 1

            # print("tetris")

            return True

        return False

    def drawTspin(self, tetris, sx, sy):
        if tetris.tspin:
            r = self.screen.blit(self.images["tspin_double_img"], (sx, sy))
            
            pygame.display.update(r)

            tetris.LAST_TSPIN_DRAW_TIME = 0
            tetris.tspin_drawing = 1

            return True

        return False

    def drawBack2Back(self, tetris, sx, sy):
        if tetris.pre_back2back and (tetris.tspin or tetris.tetris):
            r = self.screen.blit(self.images["back2back_img"], (sx, sy))
            
            pygame.display.update(r)

            tetris.LAST_BACK2BACK_DRAW_TIME = 0
            tetris.back2back_drawing = 1

            return True

        return False

    def drawGameScreen(self, tetris):
        if tetris.LAST_COMBO_DRAW_TIME > COMBO_COUNT_FREQ and tetris.check_combo():
            self.screen.blit(self.images["gamescreen"], (0, 0))
            tetris.oldcombo = tetris.combo

        if tetris.LAST_TSPIN_DRAW_TIME > TSPIN_FREQ and tetris.tspin_drawing:
            self.screen.blit(self.images["gamescreen"], (0, 0))
            tetris.tspin_drawing = 0

        if tetris.LAST_TETRIS_DRAW_TIME > TETRIS_FREQ and tetris.tetris_drawing:
            self.screen.blit(self.images["gamescreen"], (0, 0))
            tetris.tetris_drawing = 0

        if tetris.LAST_BACK2BACK_DRAW_TIME > BACK2BACK_FREQ and tetris.back2back_drawing:
            self.screen.blit(self.images["gamescreen"], (0, 0))
            tetris.back2back_drawing = 0
            # tetris.combo += 1

    #drawing the actual game self.screen     
    def drawScreen(self, tetris_1, sx, sy):
        self.drawHeld(tetris_1, sx - 56, sy + 23)  # draws held piece for grid1
        self.drawNext(tetris_1, sx + 206, sy + 23) # draws next piece for grid1
        self.drawNumbers(tetris_1, sx - 56, sy + 239) # draws the linessent on the self.screen for grid1
                        
        #this code blits the background grid for grid1
        excess = len(tetris_1.grid[0]) - GRID_DEPTH
        # print(player_1.grid)
        for x in range(GRID_WIDTH):
            for y in range(excess, len(tetris_1.grid[0])):
                if tetris_1.grid[x][y] == 0:
                    if (x + y) % 2 == 0:
                        self.screen.blit(self.images["dgrey"], (sx + x * 18, sy + (y - excess) * 18))
                    elif (x + y) % 2 == 1:
                        self.screen.blit(self.images["lgrey"], (sx + x * 18, sy + (y - excess) * 18))

        #drawing the ghost peices as long as there are no
        #pieces under the block ie collidedown==False
        if collideDown(tetris_1.grid, tetris_1.block, tetris_1.px, tetris_1.py) == False:
            self.drawGhostPiece(tetris_1, sx, sy)

        #drawing the pieces
        self.drawPiece(tetris_1, sx, sy)              
        #drawing the grid
        self.drawBoard(tetris_1, sx, sy)

    # drawing the held pieces
    # this function allows you to hold a piece
    # by hitting the respective hold button

    def drawHeld(self, tetris, sx, sy):
        grid, held = tetris.grid, tetris.held
        if held != None:
            # num = allpieces.index(held)
            _type = held.block_type()
            pos = []
            for x in range(4):
                for y in range(4):
                    if held.now_block()[x][y] > 0:
                        pos.append((x,y))

            self.screen.blit(self.images["holdback"], (sx - 8, 159))

            
            if _type == 'I':
                for i in range(len(pos)):#if its an o piece different x and y position
                    self.screen.blit(self.images["resizepics"][_type], (sx - 5 + int(pos[i][0] * 12), sy - 6 + int(pos[i][1] * 12)))
            elif _type == 'O':
                for i in range(len(pos)):#any other piece id the same x and y position
                    self.screen.blit(self.images["resizepics"][_type], (sx - 5 + int(pos[i][0] * 12), sy + int(pos[i][1] * 12)))

            else:
                for i in range(len(pos)):#if its an i piece different x and y position
                    self.screen.blit(self.images["resizepics"][_type], (sx + int(pos[i][0] * 12), sy + int(pos[i][1] * 12)))

    # drawing the next pieces 
    def drawNext(self, tetris, sx, sy): 
        grid, nextpieces = tetris.grid, tetris.buffer.now_list
        for i in range(5): # 5 different pieces 
            pos = []
            _type = nextpieces[i].block_type()
            b = nextpieces[i].now_block()
            for x in range(4):
                for y in range(4): #same procedure as the drawhed function
                    if b[x][y] > 0:
                        pos.append((x, y))
            
            if i == 0: # position 1
                self.screen.blit(self.images["holdback"], (sx - 1, 159))            
                if _type == 'I': # i piece is different x and y pos
                    for i in range(len(pos)):
                        self.screen.blit(self.images["resizepics"][_type], (sx + 1 + int(pos[i][0] * 12), 156 + int(pos[i][1] * 12)))
                elif _type == 'O': # o piece is different x and y pos
                    for i in range(len(pos)):
                        self.screen.blit(self.images["resizepics"][_type], (sx + 1 + int(pos[i][0] * 12), 158 + int(pos[i][1] * 12)))                
                else: # every other piece is the same x and y pos              
                    for i in range(len(pos)):
                        self.screen.blit(self.images["resizepics"][_type], (sx + 7 + int(pos[i][0] * 12), 159 + int(pos[i][1] * 12)))

            if i == 1: # position 2
                self.screen.blit(self.images["nextback2"], (sx + 2, 230))
                if _type == 'I': # i piece is differnet x and y pos
                    for i in range(len(pos)):
                        self.screen.blit(self.images["nextpics"][_type], (sx + 9 + int(pos[i][0] * 8), 235 + int(pos[i][1] * 8)))
                elif _type == 'O': # o piece is differnt x and y pos
                    for i in range(len(pos)):
                        self.screen.blit(self.images["nextpics"][_type], (sx + 10 + int(pos[i][0] * 8), 235 + int(pos[i][1] * 8)))
                else: # every other piece same x and y pos
                    for i in range(len(pos)):
                        self.screen.blit(self.images["nextpics"][_type], (sx + 13 + int(pos[i][0] * 8), 235 + int(pos[i][1] * 8)))

            if i >= 2: # position 3, 4, 5
                self.screen.blit(self.images["nextback3"], (sx + 4, 288 + 52 * (i - 2)))
                if _type == 'I': # same as above
                    for j in range(len(pos)):
                        self.screen.blit(self.images["nextpics"][_type], (sx + 9 + int(pos[j][0] * 8), 288 + (i - 2) * 51 + int(pos[j][1] * 8)))
                elif _type == 'O': # same as above
                    for j in range(len(pos)):
                        self.screen.blit(self.images["nextpics"][_type], (sx + 9 + int(pos[j][0] * 8), 292 + (i - 2) * 51 + int(pos[j][1] * 8)))
                else: # same as above
                    for j in range(len(pos)):
                        self.screen.blit(self.images["nextpics"][_type], (sx + 12 + int(pos[j][0] * 8), 292 + (i - 2) * 51 + int(pos[j][1] * 8)))

    #draws the ghost piece at where harddrop will take place
    #ghost goes where block will be when you harddrop
    def drawGhostPiece(self, tetris, sx, sy):
        grid, block, px, py = tetris.grid, tetris.block, tetris.px, tetris.py
        y = hardDrop(grid, block, px, py)
        py += y
        excess = len(grid[0]) - GRID_DEPTH
        b = block.now_block()
        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if b[x][y] > 0:
                    if GRID_WIDTH > px + x > -1 and len(grid[0]) > py + y > -1:
                        self.drawGhost(sx, sy, px + x, py + y - excess)
                        
    #draws the number of lines sent
    def drawNumbers(self, tetris, sx, sy):
        grid, sent = tetris.grid, tetris.sent
        number_digits = []

        sent = int(sent)
        while sent != 0:
            number_digits.append(sent % 10)
            sent /= 10
            sent = int(sent)

        if len(number_digits) == 0:
            number_digits.append(0)

        self.screen.blit(self.images["sentback"], (sx - 12, sy))

        # print(number_digits)

        if len(number_digits) == 1:
            self.screen.blit(self.images["numbers"][number_digits[0]], (sx, sy))

        elif len(number_digits) == 2:

            if number_digits[1] == 1:
                # blitting the self.images["numbers"] at the poisition in self.images["numbers"] list
                self.screen.blit(self.images["numbers"][number_digits[1]], (sx - 14, sy))
                self.screen.blit(self.images["numbers"][number_digits[0]], (sx + 7, sy))
            else:
                self.screen.blit(self.images["numbers"][number_digits[1]], (sx - 14, sy))
                self.screen.blit(self.images["numbers"][number_digits[0]], (sx + 14, sy))

        elif len(number_digits) == 3:
            if number_digits[2] == 1:
                self.screen.blit(self.images["numbers"][number_digits[2]], (sx - 26, sy))
                self.screen.blit(self.images["numbers"][number_digits[1]], (sx - 6, sy))
                self.screen.blit(self.images["numbers"][number_digits[0]], (sx + 18, sy))
            else:
                self.screen.blit(self.images["numbers"][number_digits[2]], (sx - 32, sy))
                self.screen.blit(self.images["numbers"][number_digits[1]], (sx - 6, sy))
                self.screen.blit(self.images["numbers"][number_digits[0]], (sx + 18, sy))

        else:
            raise ValueError('You get too many points!')

    # drawing the piece on the self.screen
    # calls on the drawblock funct in order to draw
    # the piece on the self.screen
    def drawPiece(self, tetris, sx, sy):
        grid, block, px, py = tetris.grid, tetris.block, tetris.px, tetris.py
        excess = len(grid[0]) - GRID_DEPTH
        b = block.now_block()
        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if b[x][y] > 0:
                    if -1 < px + x < 10 and -1 < py + y - excess < 20:
                        self.drawBlock(sx, sy, px + x, py + y - excess, b[x][y])

    # drawing the blocks on the grid
    # calls the drawblock function so that different self.images["numbers"] draw different colours on the self.screen
    def drawBoard(self, tetris, sx, sy):
        grid = tetris.grid
        excess = len(grid[0]) - GRID_DEPTH
        for x in range(GRID_WIDTH):
            for y in range(excess, len(grid[0])):
                if grid[x][y] > 0:
                    self.drawBlock(sx, sy, x, y - excess, grid[x][y])

        #the ghost block piece
    def drawGhost(self, sx, sy, x, y):
        self.screen.blit(self.images["ghost"], (sx + x * 18, sy + y * 18))
        
            
    #the timer for the game
    def drawTime2p(self, time):
        minutes = time / 60000 #integer div for minutes
        seconds = (time / 1000) % 60 #int and mod div for sec
        milliseconds = (time / 10) % 100# int and mod div for millisec

        x = 292 #position of the self.images["numbers"] 
        y = 67
        self.screen.blit(self.images["timeback"], (280, 63)) #background
        #minutes
        self.screen.blit(self.images["numbers"][int(minutes / 10)], (x, y))
        self.screen.blit(self.images["numbers"][int(minutes % 10)], (x + 27, y))
        self.screen.blit(self.images["decimal"], (x + 56, y))  #graphics
        self.screen.blit(self.images["decimal"], (x + 56, y + 14))  #graphics
        self.screen.blit(self.images["decimal"], (x + 127, y + 14)) #graphics
        #seconds
        self.screen.blit(self.images["numbers"][int(seconds / 10)], (x + 73, y))
        self.screen.blit(self.images["numbers"][int(seconds % 10)], (x + 100, y))
        #milliseconds
        self.screen.blit(self.images["numbers"][int(milliseconds / 10)], (x + 144, y))
        self.screen.blit(self.images["numbers"][int(milliseconds % 10)], (x + 171, y))

    # drawing the different blocks
    # different self.images["numbers"](vals) draws differnt colour blocks on the self.screen
    def drawBlock(self, sx, sy, x, y, val):
        # self.images["pics"] = [ipiece, opiece, jpiece, lpiece, zpiece, spiece, tpiece, lspiece]
        self.screen.blit(self.images["piecepics"][PIECE_NUM2TYPE[val]], (sx + x * 18, sy + y * 18))

    def drawByName(self, name, sx, sy):
        self.screen.blit(self.images[name], (sx, sy))
    def drawByObj(self, obj, sx, sy):
        self.screen.blit(obj, (sx, sy))

    def drawKO(self, ko, sx, sy):
        # print(ko)
        self.screen.blit(self.images["kos"][ko - 1], (sx, sy))
