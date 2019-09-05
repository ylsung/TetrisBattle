import os
import numpy as np
import random
import gym
from gym import spaces
from gym import utils
from gym.utils import seeding

from settings import *

from tetris import Tetris, Player, Judge, get_infos

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

                # freeze(0.5)

                scores -= 5

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
            self.time -= self.timer2p.tick() * SPEED_UP
        else:
            self.time = 0
            end = 1

        Renderer.drawTime2p(self.time)
        
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
                     'holes': holes, 
                     'n_used_block': tetris_1.n_used_block}
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

        Renderer.drawTime2p(self.time)
        
        # if player_2.check_combo():
        
       
        #time goes until it hits zero
        #when it hits zero return endgame screen
        
        pygame.display.flip()
        self.myClock.tick(FPS)  

        ob = self.get_obs()

        return ob

class TetrisSingleEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human', 'rgb_array'], 
                'obs_type': ['image', 'grid']}

    def __init__(self, gridchoice="none", obs_type="image", mode="rgb_array"):
        super(TetrisSingleEnv, self).__init__()

        # Define action and observation space
        # They must be gym.spaces objects

        # Example when using discrete actions:

        self.game_interface = TetrisSingleInterface(gridchoice=gridchoice, 
                                                    obs_type=obs_type, 
                                                    mode=mode)


        self._n_actions = self.game_interface.n_actions

        self.action_space = spaces.Discrete(self._n_actions)

        # print(self.action_space.n)

        self._action_set = self.game_interface.action_set

        self.action_meaning = self.game_interface.action_meaning

        self.seed()

        if obs_type == "image":
            self.observation_space = spaces.Box(low=0, high=255, 
                shape=self.game_interface.screen_size() + [3], dtype=np.uint8)

    def random_action(self):
        return self.game_interface.random_action()

    def get_action_meanings(self):
        return [self.action_meaning[i] for i in self._action_set]

    def seed(self, seed=None):
        self.np_random, seed1 = seeding.np_random(seed)
        
    def step(self, action):
        # Execute one time step within the environment

        ob, reward, end, infos = self.game_interface.act(action)


        if len(infos) != 0:
            reward += infos['height_sum'] / 50 / 1000

            reward -= infos['diff_sum'] / 40 / 1000

            reward -= infos['max_height'] / 30 / 1000

            reward -= infos['holes'] / 20 / 1000

        return ob, reward, end, infos

    def reset(self):
        # Reset the state of the environment to an initial state

        ob = self.game_interface.reset()

        return ob
    
    def render(self, mode='human', close=False):
        return None
        # # Render the environment to the screen
        # img = self.get_screen_shot()

        # if mode == 'rgb_array':
        #     return img
        # elif mode == 'human':
        #     from gym.envs.classic_control import rendering
        #     if self.viewer is None:
        #         self.viewer = rendering.SimpleImageViewer()
        #     self.viewer.imshow(img)

        #     return self.viewer.isopen


if __name__ == "__main__":
    # play()

    env = TetrisSingleEnv(gridchoice="none", obs_type="grid", mode="human")

    ob = env.reset()
    import time
    start = time.time()
    for i in range(200000):
        action = env.random_action()
        # if i % 2 == 0:
        #     action = 2
        # else:
        #     action = 0
        ob, reward, done, infos = env.step(action)
        print(ob)
        if len(infos) != 0:
            print(infos)
        # im = Image.fromarray(ob)
        # im.save("samples/%d.png" % i)
        if done:
            print(time.time() - start)
            print(i)
            # exit()
            ob = env.reset()



