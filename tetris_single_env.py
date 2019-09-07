import os
import numpy as np
import random
import gym
from gym import spaces
from gym import utils
from gym.utils import seeding

from settings import *

from tetris import Tetris, Player, Judge, get_infos, freeze

from renderer import Renderer


pos_player1 = {
    'combo': (44, 437),
    'tetris': (314, 477),
    'tspin': (304, 477),
    'back2back': (314, 437),
    'board': (112, 138),
    'drawscreen': (112, 138),
    'big_ko': (44, 235),
    'ko': (140, 233),
    'transparent': (110, 135),
    'gamescreen': (0, 0), 
    'attack_clean': (298, 140, 3, 360),
    'attack_alarm': (298, 481, 3, 18)

}

pos_player2 = {
    'combo': (415, 437),
    'tetris': (685, 477),
    'tspin': (675, 477),
    'back2back': (685, 437),
    'board': (495, 138),
    'drawscreen': (495, 138),
    'big_ko': (426, 235),
    'ko': (527, 233),
    'transparent': (494, 135),
    'gamescreen': (0, 0), 
    'attack_clean': (680, 140, 3, 360),
    'attack_alarm': (680, 481, 3, 18)
}

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

        if mode == "rgb_array":
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) # SCREEN is 800*600 

        images = load_imgs()

        self.renderer = Renderer(self.screen, images)

        self._obs_type = obs_type

        self._mode = mode

        self.time = MAX_TIME

        self._action_meaning = {
            0: "NOOP",
            1: "hold",
            2: "drop",
            3: "rotate_right",
            4: "rotate_left",
            5: "right",
            6: "left",
            7: "down" 
        }

        self._n_actions = len(self._action_meaning)

        # print(self.action_space.n)

        self._action_set = list(range(self._n_actions))

        info_dict_1 = {
            "id": 0,
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

        self.tetris_list = []

        self.tetris_list.append({
            'info_dict': info_dict_1,
            'tetris': Tetris(Player(info_dict_1), gridchoice),
            'com_event': ComEvent(),
            'pos': pos_player1
        })

        # if num_players == 2:
        info_dict_2 = {
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
            info_dict_2[v] = k

        self.tetris_list.append({
            'info_dict': info_dict_2,
            'tetris': Tetris(Player(info_dict_2), gridchoice),
            'com_event': ComEvent(),
            'pos': pos_player2
        })
        

        # self.com_event = ComEvent()
        self.num_players = 1
        self.now_player = 0

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
        pass
        # return self.tetris.get_grid()

    def get_obs(self):
        if self._obs_type == "grid":
            return self.get_seen_grid()
        elif self._obs_type == "image":
            img = self.get_screen_shot()
        return img

    def random_action(self):
        return random.randint(0, self._n_actions - 1)

    def getCurrentPlayerID(self):
        return self.now_player

    def take_turns(self):
        self.now_player += 1
        self.now_player %= self.num_players
        return self.now_player
        
    def act(self, action):
        # Execute one time step within the environment
        end = 0
        scores = 0

        player, opponent = self.tetris_list[self.now_player], self.tetris_list[::-1][self.now_player]
        tetris = player["tetris"]
        com_event = player["com_event"]
        pos = player["pos"]

        tetris.natural_down()

        com_event.set([action])

        for evt in com_event.get():
            tetris.trigger(evt)

        tetris.move()

        if tetris.check_fallen():
            # compute the scores and attack the opponent
            cleared_scores = tetris.clear()

            scores += cleared_scores

            self.renderer.drawCombo(tetris, pos["combo"][0], pos["combo"][1])

            self.renderer.drawTetris(tetris, pos["tetris"][0], pos["tetris"][1])
            self.renderer.drawTspin(tetris, pos["tspin"][0], pos["tspin"][1])
            self.renderer.drawBack2Back(tetris, pos["back2back"][0], pos["back2back"][1])

            if tetris.check_KO():
                self.renderer.drawBoard(tetris, pos["board"][0], pos["board"][1])
                
                tetris.clear_garbage()

                self.renderer.drawByName("ko", pos["ko"][0], pos["ko"][1])
                self.renderer.drawByName("transparent", pos["transparent"][0], pos["transparent"][1])

                # screen.blit(kos[tetris_2.get_KO() - 1], (426, 235))
                pygame.display.flip()

                scores -= 1

                end = 1

            tetris.new_block()

        self.renderer.drawGameScreen(tetris)

        # if tetris.attacked == 0:
        #     pygame.draw.rect(self.screen, (30, 30, 30), pos["attack_clean"]) 

        # if tetris.attacked != 0:
            
        #     for j in range(tetris.attacked):
        #         pos_attack_alarm = list(pos["attack_alarm"])
        #         # modified the y axis of the rectangle, according to the strength of attack
        #         pos_attack_alarm[1] = pos_attack_alarm[1] - 18 * j
        #         pygame.draw.rect(self.screen, (255, 0, 0), pos_attack_alarm) 

        if tetris.KO > 0:
            self.renderer.drawKO(tetris.KO, pos["big_ko"][0], pos["big_ko"][1])
            
        self.renderer.drawScreen(tetris, pos["drawscreen"][0], pos["drawscreen"][1])

        self.renderer.drawByName("transparent", *opponent["pos"]["transparent"])

        if self.time >= 0:
            self.time -= self.timer2p.tick() * SPEED_UP
        else:
            self.time = 0
            end = 1

        self.renderer.drawTime2p(self.time)
        
        # time goes until it hits zero
        # when it hits zero return endgame screen
        
        self.myClock.tick(FPS)  
        pygame.display.flip()

        ob = self.get_obs()

        # height_sum, diff_sum, max_height, holes = get_infos(self.get_seen_grid())

        # if self.tetris.is_fallen:
        #     infos = {'height_sum': height_sum, 
        #              'diff_sum': diff_sum,
        #              'max_height': max_height,
        #              'holes': holes, 
        #              'n_used_block': tetris.n_used_block}
        # else:
        infos = {}

        if end:
            freeze(0.5)
            # self.reset()

        return ob, scores, end, infos

    def reset(self):
        # Reset the state of the environment to an initial state

        self.time = MAX_TIME
        self.now_player = random.randint(0, self.num_players - 1)

        for i, player in enumerate(self.tetris_list):
            if i + 1 > self.num_players:
                break 
            tetris = player["tetris"]
            com_event = player["com_event"]
            pos = player["pos"]
            tetris.reset()

            com_event.reset()
            self.renderer.drawByName("gamescreen", pos["gamescreen"][0], pos["gamescreen"][1]) # blitting the main background

            self.renderer.drawGameScreen(tetris)
            

        # SCREEN.blit(IMAGES["transparent"], (494, 135))

        # pygame.display.flip()

        self.renderer.drawTime2p(self.time)
        
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

    def take_turns(self):
        return self.game_interface.take_turns()
        
    def step(self, action):
        # Execute one time step within the environment

        ob, reward, end, infos = self.game_interface.act(action)


        # if len(infos) != 0:
        #     reward += infos['height_sum'] / 50 / 1000

        #     reward -= infos['diff_sum'] / 40 / 1000

        #     reward -= infos['max_height'] / 30 / 1000

        #     reward -= infos['holes'] / 20 / 1000

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

        if i % 5 == 0:
            env.take_turns()
            action = env.random_action()
        else:
            action = 0
        # if i % 2 == 0:
        #     action = 2
        # else:
        #     action = 0
        ob, reward, done, infos = env.step(action)
        # print(ob)
        print(reward)
        if len(infos) != 0:
            print(infos)
        # im = Image.fromarray(ob)
        # im.save("samples/%d.png" % i)
        if done:
            print(time.time() - start)
            print(i)
            # exit()
            ob = env.reset()



