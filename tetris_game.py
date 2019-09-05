import pygame
import argparse
from settings import *

import time as t

from renderer import Renderer

from tetris import Tetris, Player, Judge, collideDown, collide, collideLeft, collideRight, \
    hardDrop, freeze, get_infos

class TetrisGame:
    #first function
    #will be used for choosing what map you want to play on

    def __init__(self):
        # SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.FULLSCREEN) # SCREEN is 800*600 
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) # SCREEN is 800*600 
        images = load_imgs()
        self.renderer = Renderer(self.screen, images)

    def play(self):
        page = "menu"
        myClock = pygame.time.Clock() # this will be used to set the FPS(frames/s) 

        timer2p = pygame.time.Clock() # this will be used for counting down time in our game
        while page != "exit":
            if page == "menu":
                page = self.menu(page)
            if page == "start":
                page = self.start(myClock, timer2p)
            if page == "viewmap":
                page = self.viewmap()    
            if page == "instructions":
                page = self.instructions()    
            # if page == "pygame.quit":
            #     page = (page)    
            # if page == "credits":
            #     page = self.credit(page)
        # pygame.quit()

    def setmap(self):
        running = True
        # loading images
        
        # defining rectangles for collision checking
        map1 = pygame.Rect(155,75,200,200)
        map2 = pygame.Rect(439,75,200,200)
        map3 = pygame.Rect(155,309,200,200)
        map4 = pygame.Rect(439,309,200,200)
        buttons = [map1, map2, map3, map4]# preparing a buttons and names list to be zipped together
        names = ["none", "classic", "comboking", "lunchbox"]# 
        self.renderer.drawByName("back1", 0, 0) # IMAGES["back1"] is the main background
        while running:
            mpos = pygame.mouse.get_pos()
            mb = pygame.mouse.get_pressed()
            for evnt in pygame.event.get():          
                if evnt.type == pygame.QUIT:
                    running = False

            for b, n in zip(buttons, names): # zipping buttons and names together       
                if b.collidepoint(mpos):   # for very easy collision checking            
                    if mb[0] == 1:
                        return n # return the name of the map chosen

            # this chunk of code is just making pretty pictures       
            if map1.collidepoint(mpos):
                self.renderer.drawByName("outline", 149, 64)
            elif map2.collidepoint(mpos):
                self.renderer.drawByName("outline", 431, 64)
            elif map3.collidepoint(mpos):
                self.renderer.drawByName("outline", 149, 301)
            elif map4.collidepoint(mpos):
                self.renderer.drawByName("outline", 149, 301)
            else:
                self.renderer.drawByName("back1", 0, 0) # keeping it fresh
            
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
        self.renderer.drawByName("back1", 0, 0) # back1 is the main background
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
                self.renderer.drawByName("outline", 149, 64)
            elif map2.collidepoint(mpos):
                self.renderer.drawByName("outline", 431, 64)
            elif map3.collidepoint(mpos):
                self.renderer.drawByName("outline", 149, 301)
            elif map4.collidepoint(mpos):
                self.renderer.drawByName("outline", 149, 301)
            else:
                self.renderer.drawByName("back1", 0, 0) # keeping it fresh

            pygame.display.flip() #necessities

        return "menu"

    #instructions page
    def instructions(self):
        running = True
        self.renderer.drawByName("back2", 0, 0)
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
        
        
        self.renderer.drawByName("intro", 0, 0)
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
                self.renderer.drawByName("startbutton", 319, 207)
                if mb[0] == 1:
                    return "start"#starting the game
                #making the game look pretty
            elif buttons[0].collidepoint(mpos):
                self.renderer.drawByName("startbutton", 319, 207)
                self.renderer.drawByName("setmapbutton", 325, 274)
            elif buttons[1].collidepoint(mpos):
                self.renderer.drawByName("helpbutton", 325, 317)
            elif buttons[2].collidepoint(mpos):
                self.renderer.drawByName("quitbutton", 325, 360)
                if mb[0] == 1:
                    return "exit" # quitting the game
            else:
                self.renderer.drawByName("intro", 0, 0) # reblit the background
            
            #draw.rect(SCREEN,(0,0,0),button1,2)
            myClock.tick(FPS)            
            pygame.display.flip()

    #main game function
    def start(self, myClock, timer2p):
        raise NotImplementedError
    

class TetrisGameDouble(TetrisGame):

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
        # SCREEN.blit(IMAGES["gamescreen"], (0, 0))# blitting the main background
        self.renderer.drawByName("gamescreen", 0, 0)

        #these two used for countdown
        #of the timer
        time = MAX_TIME
        delaytime = time

        info_dict_1 = {
        "id": 0,
        "hold": pygame.K_c,
        "drop": pygame.K_SPACE,
        "rotate_right": pygame.K_UP,
        "rotate_left": pygame.K_z,
        "right": pygame.K_RIGHT,
        "left": pygame.K_LEFT,
        "down": pygame.K_DOWN
        }

        info_dict_2 = {
        "id": 1,
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
        winner = 0
        force_quit = 0
        #main loop
        while running:
            # battlemusic.play()#plays music
            
            tetris_1.natural_down()
            tetris_2.natural_down()

            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    running = False
                    force_quit = 1
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

                # if tetris_2.attacked == 0:
                #     pygame.draw.rect(self.screen, (255, 255, 255), (680, 135, 3, 365)) 

                # self.renderer.drawBoard(tetris_2, 495, 138)

                self.renderer.drawCombo(tetris_1, 164 - 120, 377 + 60)

                self.renderer.drawTetris(tetris_1, 164 + 150, 377 + 100)
                self.renderer.drawTspin(tetris_1, 164 + 140, 377 + 100)
                self.renderer.drawBack2Back(tetris_1, 164 + 150, 377 + 60)

                # pygame.display.flip()

                if tetris_1.check_KO():
                    
                    self.renderer.drawBoard(tetris_1, 112, 138)
                    tetris_2.update_ko()
                    tetris_1.clear_garbage()

                    self.renderer.drawByName("ko", 140, 233)
                    self.renderer.drawByName("transparent", 110, 135)

                    # SCREEN.blit(kos[tetris_2.get_KO() - 1], (426, 235))
                    # pygame.display.flip()
                    # pygame.display.update(r)
                    pygame.display.flip()
                    freeze(0.5)

                tetris_1.new_block()

            self.renderer.drawGameScreen(tetris_1)

            if tetris_2.check_fallen():
                # compute the scores and attack the opponent
                scores = tetris_2.clear()

                tetris_1.add_attacked(scores)

                # red block: for attacking alarm
                

                # self.renderer.drawBoard(tetris_1, 112, 138)

                self.renderer.drawCombo(tetris_2, 535 - 120, 377 + 60)

                self.renderer.drawTetris(tetris_2, 535 + 150, 377 + 100)
                self.renderer.drawTspin(tetris_2, 535 + 140, 377 + 100)
                self.renderer.drawBack2Back(tetris_2, 535 + 150, 377 + 60)

                # pygame.display.flip()

                if tetris_2.check_KO():
                    self.renderer.drawBoard(tetris_2, 495, 138)

                    tetris_1.update_ko()
                    tetris_2.clear_garbage()

                    self.renderer.drawByName("ko", 527, 233)
                    self.renderer.drawByName("transparent", 494, 135)

                    # SCREEN.blit(kos[tetris_1.get_KO() - 1], (44, 235))
                    # pygame.display.update(r)
                    pygame.display.flip()

                    freeze(0.5)

                tetris_2.new_block()

            self.renderer.drawGameScreen(tetris_2)

            if tetris_1.attacked == 0:
                pygame.draw.rect(self.screen, (30, 30, 30), (298, 140, 3, 360)) 

            if tetris_1.attacked != 0:
                for i in range(tetris_2.attacked):
                    pygame.draw.rect(self.screen, (255, 0, 0), (298, 481 - 18 * i, 3, 18)) 

            if tetris_2.attacked == 0:
                pygame.draw.rect(self.screen, (30, 30, 30), (680, 140, 3, 360)) 

            if tetris_2.attacked != 0:
                for i in range(tetris_2.attacked):
                    pygame.draw.rect(self.screen, (255, 0, 0), (680, 481 - 18 * i, 3, 18)) 

            

            if tetris_1.KO > 0:
                self.renderer.drawKO(tetris_1.KO, 44, 235)
                # pygame.display.flip()

            if tetris_2.KO > 0:
                self.renderer.drawKO(tetris_2.KO, 426, 235)
                # pygame.display.flip()

                
            #parameters for getting position of
            #falling block
            # positions1 = getPositions(player_1.block, player_1.px, player_1.py)
            # positions2 = getPositions(player_2.block, player_2.px, player_2.py)     

            self.renderer.drawScreen(tetris_1, 112, 138)

            self.renderer.drawScreen(tetris_2, 495, 138)

            # pygame.display.flip()

            if Judge.check_ko_win(tetris_1, max_ko=3):
                # exit()
                running = False
                winner = tetris_1.get_id()
                # b = SCREEN.copy()
                # return [b, "endgame", tetris_1.get_id()]
            if Judge.check_ko_win(tetris_2, max_ko=3):
                # b = SCREEN.copy()
                # return [b, "endgame", tetris_2.get_id()]

                running = False
                winner = tetris_2.get_id()
            
            if time >= 0:
                time -= timer2p.tick() * SPEED_UP
            else:
                time = 0

                running = False
                winner = Judge.who_win(tetris_1, tetris_2)
                
            self.renderer.drawTime2p(time)
            # pygame.display.flip()

            # set FPS
            myClock.tick(FPS)   
            pygame.display.flip()

        if force_quit:
            return "menu"
        # end game
        # self.renderer.drawByObj(a, 0, 0)
        self.renderer.drawByName("transparent", 110, 135)
        self.renderer.drawByName("transparent", 494, 135)
        self.renderer.drawByName("transparent", 494, 135)
        self.renderer.drawByName("transparent", 494, 135)

        if winner == 0:
            self.renderer.drawByName("you_win", 120, 230)
            self.renderer.drawByName("you_lose", 515, 230)
        else:
            self.renderer.drawByName("you_win", 520, 230)
            self.renderer.drawByName("you_lose", 115, 230)

        pygame.display.flip()

        freeze(2.0)

        return "menu"

        # pygame.quit()

class TetrisGameSingle(TetrisGame):
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
        self.renderer.drawByName("gamescreen", 0, 0)
        # a = SCREEN.copy()#used for image coverage

        #these two used for countdown
        #of the timer
        time = MAX_TIME
        delaytime = time

        info_dict_1 = {
        "id": 0,
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
        force_quit = 0
        kk = 0
        while running:
            # battlemusic.play()#plays music
            
            tetris_1.natural_down()

            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    running = False
                    force_quit = 1
                tetris_1.trigger(evt)

            tetris_1.move()

            if tetris_1.check_fallen():
                # print("fall")
                # print(tetris_1.stopcounter)
                # print(tetris_1.px, tetris_1.py)
                # compute the scores and attack the opponent
                scores = tetris_1.clear()

                kk += 1

                # tetris_2.add_attacked(scores)

                self.renderer.drawCombo(tetris_1, 164 - 120, 377 + 60)

                self.renderer.drawTetris(tetris_1, 164 + 150, 377 + 100)
                self.renderer.drawTspin(tetris_1, 164 + 140, 377 + 100)
                self.renderer.drawBack2Back(tetris_1, 164 + 150, 377 + 60)

                if tetris_1.check_KO():
                    # tetris_2.update_ko()
                    self.renderer.drawBoard(tetris_1, 112, 138)

                    tetris_1.clear_garbage()

                    # b = SCREEN.copy()

                    # self.renderer.drawByName("ko", 140, 233)
                    # self.renderer.drawByName("transparent", 110, 135)

                    # SCREEN.blit(kos[tetris_2.get_KO() - 1], (426, 235))
                    pygame.display.flip()
                    running = False

                    # break

                tetris_1.new_block()

            self.renderer.drawGameScreen(tetris_1)
                
            #parameters for getting position of
            #falling block
            # positions1 = getPositions(player_1.block, player_1.px, player_1.py)
            # positions2 = getPositions(player_2.block, player_2.px, player_2.py)     

            self.renderer.drawScreen(tetris_1, 112, 138)

            # draw transparent on player 2's grid
            self.renderer.drawByName("transparent", 494, 135)

            # pygame.display.update(r)

            if time >= 0:
                time -= timer2p.tick() * SPEED_UP
            else:
                time = 0

                running = False

            self.renderer.drawTime2p(time)

            # if player_2.check_combo():
            
           
            #time goes until it hits zero
            #when it hits zero return endgame SCREEN
            myClock.tick(FPS)   
            pygame.display.flip()

        if force_quit:
            return "menu"
        # self.renderer.drawByObj(a, 0, 0)
        self.renderer.drawByName("transparent", 110, 135)
        # SCREEN.blit(IMAGES["transparent"], (494, 135))
        # SCREEN.blit(IMAGES["pics"][winner - 1], (135, 230))
        # SCREEN.blit(IMAGES["pics"][(2 - winner)], (500, 230))
        pygame.display.flip()
        freeze(2.0)
        # pygame.quit()
        return "menu"

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["single", "double"], default="single")

    return parser.parse_args()

if __name__ == "__main__":
    args = parser()
    if args.mode == "single":
        game = TetrisGameSingle()
    else:
        game = TetrisGameDouble()
    game.play()