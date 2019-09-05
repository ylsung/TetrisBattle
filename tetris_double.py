import pygame

from tetris import TetrisGameDouble

def play():
    # allowing for the menu to
    # switch between pages 

    myClock = pygame.time.Clock() # this will be used to set the FPS(frames/s) 

    timer2p = pygame.time.Clock() # this will be used for counting down time in our game

    game = TetrisGameDouble()

    page = "menu"
    while page != "exit":
        if page == "menu":
            page = game.menu(page)
        if page == "start":
            x = game.start(myClock, timer2p)
            b = x[2]
            a = x[0]
            page = x[1]
        if page == "endgame":    
            page = game.endgame(a, b)
        if page == "viewmap":
            page = game.viewmap()    
        if page == "instructions":
            page = game.instructions()    
        if page == "pygame.quit":
            page = (page)    
        if page == "credits":
            page = game.credit(page)
    pygame.quit()


if __name__ == "__main__":
    
    play()