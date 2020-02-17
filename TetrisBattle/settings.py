import os
import pygame

ROOT = os.path.abspath(os.path.dirname(__file__))

# PARAMETERS

GRID_WIDTH = 10
GRID_DEPTH = 20

BLOCK_LENGTH = 4
BLOCK_WIDTH = 4

FPS = 100

SCREENWIDTH  = 800
SCREENHEIGHT = 600

SPEED_UP = 1

MAX_TIME = 130000

PIECE_SHAPE_NUM = 4

# COLLIDE_DOWN_COUNT = 80 / SPEED_UP

# ROTATE_FREQ = 0.1 / SPEED_UP

# FALL_DOWN_FREQ = 0.4 / SPEED_UP

# NATRUAL_FALL_FREQ = 0.8 / SPEED_UP

# MOVE_SHIFT_FREQ = 0.13 / SPEED_UP

# MOVE_DOWN_FREQ = 0.1 / SPEED_UP

# COMBO_COUNT_FREQ = 0.3 / SPEED_UP

# TSPIN_FREQ = 0.8 / SPEED_UP

# TETRIS_FREQ = 0.8 / SPEED_UP

# BACK2BACK_FREQ = 0.8 / SPEED_UP

COLLIDE_DOWN_COUNT = 80.0 / SPEED_UP

ROTATE_FREQ = 10.0 / SPEED_UP

FALL_DOWN_FREQ = 40.0 / SPEED_UP

NATRUAL_FALL_FREQ = 80.0 / SPEED_UP

MOVE_SHIFT_FREQ = 10.0 / SPEED_UP

MOVE_DOWN_FREQ = 10.0 / SPEED_UP

COMBO_COUNT_FREQ = 30.0 / SPEED_UP

TSPIN_FREQ = 80.0 / SPEED_UP

TETRIS_FREQ = 80.0 / SPEED_UP

BACK2BACK_FREQ = 80.0 / SPEED_UP

MAX_COMBO = 10

# MUSIC_PATH

MUSIC_PATH = os.path.join(ROOT, "assets/tetris sounds/battlemusic.wav")

# BLOCKS


#these lists below are the different pieces in the game
#there are 4 different types of each list so that when you
#rotate the pygame.image will change
ipieces = [[[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]],
          [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]],
          [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
          [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]]
opieces = [[[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]],
          [[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]],
          [[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]],
          [[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]]]
jpieces = [[[0, 3, 3, 0], [0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 0, 0]],
          [[0, 0, 0, 0], [0, 3, 3, 3], [0, 3, 0, 0], [0, 0, 0, 0]],
          [[0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 3, 3], [0, 0, 0, 0]],
          [[0, 0, 0, 3], [0, 3, 3, 3], [0, 0, 0, 0], [0, 0, 0, 0]]]
lpieces = [[[0, 0, 4, 0], [0, 0, 4, 0], [0, 4, 4, 0], [0, 0, 0, 0]],
          [[0, 0, 0, 0], [0, 4, 4, 4], [0, 0, 0, 4], [0, 0, 0, 0]],
          [[0, 0, 4, 4], [0, 0, 4, 0], [0, 0, 4, 0], [0, 0, 0, 0]],
          [[0, 4, 0, 0], [0, 4, 4, 4], [0, 0, 0, 0], [0, 0, 0, 0]]]
zpieces = [[[0, 5, 0, 0], [0, 5, 5, 0], [0, 0, 5, 0], [0, 0, 0, 0]],
          [[0, 0, 0, 0], [0, 5, 5, 0], [5, 5, 0, 0], [0, 0, 0, 0]],
          [[0, 5, 0, 0], [0, 5, 5, 0], [0, 0, 5, 0], [0, 0, 0, 0]],
          [[0, 0, 5, 5], [0, 5, 5, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
spieces = [[[0, 0, 6, 0], [0, 6, 6, 0], [0, 6, 0, 0], [0, 0, 0, 0]],
          [[0, 0, 0, 0], [0, 6, 6, 0], [0, 0, 6, 6], [0, 0, 0, 0]],
          [[0, 0, 6, 0], [0, 6, 6, 0], [0, 6, 0, 0], [0, 0, 0, 0]],
          [[6, 6, 0, 0], [0, 6, 6, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
tpieces = [[[0, 0, 7, 0], [0, 7, 7, 0], [0, 0, 7, 0], [0, 0, 0, 0]],
          [[0, 0, 0, 0], [0, 7, 7, 7], [0, 0, 7, 0], [0, 0, 0, 0]],
          [[0, 0, 7, 0], [0, 0, 7, 7], [0, 0, 7, 0], [0, 0, 0, 0]],
          [[0, 0, 7, 0], [0, 7, 7, 7], [0, 0, 0, 0], [0, 0, 0, 0]]]
lspieces = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8] #this is the lines sent piece aka garbage lines

PIECES_DICT = {
    'I': ipieces, 'O': opieces, 'J': jpieces,
    'L': lpieces, 'Z': zpieces, 'S': spieces,
    'T': tpieces, 'G': lspieces
}

PIECE_NUM2TYPE = {1: 'I', 2: 'O', 3: 'J', 4: 'L', 5: 'Z', 6: 'S', 7: 'T', 8: 'G'}
PIECE_TYPE2NUM = {val: key for key, val in PIECE_NUM2TYPE.items()}
POSSIBLE_KEYS = ['I', 'O', 'J', 'L', 'Z', 'S', 'T']

# POSSIBLE_KEYS = ['I', 'O', 'L', 'L', 'L', 'I', 'O']
# POSSIBLE_KEYS = ['L', 'L', 'J', 'J', 'J', 'L', 'L']


# POSSIBLE_KEYS = ['I', 'I', 'I', 'I', 'O', 'O', 'O']

# IMAGES

def load_imgs():
    images_dict = {}

    #the code below imports many of the images that will be used
    images_dict["gamescreen"] = pygame.image.load(
        os.path.join(ROOT, "assets/gamescreen.png")) # backscreen
    images_dict["lgrey"] = pygame.image.load(
        os.path.join(ROOT, "assets/lightgreysquare.png")) # square for grid background
    images_dict["dgrey"] = pygame.image.load(
        os.path.join(ROOT, "assets/darkgreysquare.png")) # smae as above
    # sentpiece = pygame.image.load(ROOT + "assets/tetris blocks/linessent block.png")#dark block for garbage lines
    images_dict["ghost"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris blocks/ghost block.png")) # ghost block 
    images_dict["decimal"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris numbers/decimal.png")) # for timer
    images_dict["ko"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris icons/KO.png")) # knockout image
    images_dict["holdback"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris icons/holdback.png")) # background for pic blitting
    images_dict["sentback"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris icons/sentback.png")) # same as above
    images_dict["nextback2"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris icons/holdback2.png")) # same as above
    images_dict["nextback3"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris icons/holdback3.png")) # same as above
    images_dict["timeback"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris icons/timeback.png")) # same as above
    images_dict["back2back_img"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris icons/backtoback.png"))
    images_dict["tetris_img"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris icons/tetris.png"))
    images_dict["tspin_double_img"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris icons/tspin double.png"))
    images_dict["transparent"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris icons/transparent.png")) #l ooking good
    images_dict["back1"] = pygame.image.load(
        os.path.join(ROOT, "assets/menu pics/mainsetmap.png"))
    images_dict["outline"] = pygame.image.load(
        os.path.join(ROOT, "assets/menu pics/outline.png"))
    images_dict["back2"] = pygame.image.load(
        os.path.join(ROOT, "assets/menu pics/mainhelp.png"))
    images_dict["intro"] = pygame.image.load(
        os.path.join(ROOT, "assets/menu pics/intro screen.png"))
    images_dict["startbutton"] = pygame.image.load(
        os.path.join(ROOT, "assets/menu pics/start.png"))
    images_dict["setmapbutton"] = pygame.image.load(
        os.path.join(ROOT, "assets/menu pics/setmap.png"))
    images_dict["helpbutton"] = pygame.image.load(
        os.path.join(ROOT, "assets/menu pics/help.png"))
    images_dict["quitbutton"] = pygame.image.load(
        os.path.join(ROOT, "assets/menu pics/quit.png"))

    images_dict["you_win"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris icons/you win.png"))
    images_dict["you_lose"] = pygame.image.load(
        os.path.join(ROOT, "assets/tetris icons/you lose.png"))

    kos = [] #ko pictures
    for i in range(1, 4):#putting kO pictures in the list 
        kos.append(pygame.image.load(
            os.path.join(ROOT, "assets/tetris icons/ko" + str(i) + ".png")))

    images_dict["kos"] = kos

    numbers = []#imputing the numbers from 1 to 10 into list 
    for i in range(10): #to be used for timer and sent lines
        numbers.append(pygame.image.load(
            os.path.join(ROOT, "assets/tetris numbers/" + str(i) + ".png")))

    images_dict["numbers"] = numbers

    combos = []#inputs the combo pictures
    for i in range(1, MAX_COMBO + 1):
        combos.append(pygame.image.load(
            os.path.join(ROOT, "assets/combo/" + str(i) + "combo.png")))

    images_dict["combos"] = combos

    ipiece = pygame.image.load(
        os.path.join(ROOT, "assets/tetris blocks/lightblue block.png")) 
    opiece = pygame.image.load(
        os.path.join(ROOT, "assets/tetris blocks/yellow block.png"))
    jpiece = pygame.image.load(
        os.path.join(ROOT, "assets/tetris blocks/blue block.png"))
    lpiece = pygame.image.load(
        os.path.join(ROOT, "assets/tetris blocks/orange block.png"))
    zpiece = pygame.image.load(
        os.path.join(ROOT, "assets/tetris blocks/red block.png"))
    spiece = pygame.image.load(
        os.path.join(ROOT, "assets/tetris blocks/green block.png"))
    tpiece = pygame.image.load(
        os.path.join(ROOT, "assets/tetris blocks/purple block.png"))
    lspiece = pygame.image.load(
        os.path.join(ROOT, "assets/tetris blocks/linessent block.png"))

    piecepics = {
        'I': ipiece, 'O': opiece, 'J': jpiece,
        'L': lpiece, 'Z': zpiece, 'S': spiece,
        'T': tpiece, 'G': lspiece
    }

    images_dict["piecepics"] = piecepics

    # resizepics = []#blocks will be resized for hold piece 
    # for i in range(7):
    #     resizepics.append(transform.smoothscale(piecepics[i], (12, 12))) #12 x12 blocks

    resizepics = {} # blocks will be resized for hold piece 

    for key in list(piecepics.keys()):
        resizepics[key] = pygame.transform.smoothscale(piecepics[key], (12, 12)) # 12 x12 blocks

    images_dict["resizepics"] = resizepics

    nextpics = {} # blocks will be resized for next pieces

    for key in list(piecepics.keys()):
        nextpics[key] = pygame.transform.smoothscale(piecepics[key], (8, 8)) # 8 x8 blocks

    images_dict["nextpics"] = nextpics




    return images_dict
