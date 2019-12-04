import os
import abc
import numpy as np
import random
import gym
from gym import spaces
from gym import utils
from gym.utils import seeding

from TetrisBattle.envs.tetris_interface import TetrisInterface, TetrisDoubleInterface, \
    TetrisSingleInterface

class TetrisEnv(gym.Env, abc.ABC):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human', 'rgb_array'], 
                'obs_type': ['image', 'grid']}

    def __init__(self, interface, gridchoice="none", obs_type="image", mode="rgb_array"):
        super(TetrisEnv, self).__init__()

        # Define action and observation space
        # They must be gym.spaces objects

        # Example when using discrete actions:

        self.game_interface = interface(gridchoice=gridchoice, 
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
        elif obs_type == "grid":
            self.observation_space = spaces.Box(low=0, high=1, 
                shape=list(self.game_interface.get_seen_grid().shape), dtype=np.float32)

        self.reset()

    def random_action(self):
        return self.game_interface.random_action()

    def get_action_meanings(self):
        return [self.action_meaning[i] for i in self._action_set]

    def seed(self, seed=None):
        self.np_random, seed1 = seeding.np_random(seed)

    def take_turns(self):
        return self.game_interface.take_turns()
        
    def reset(self):

        self.accum_rewards = 0
        self.infos = {}
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


class TetrisSingleEnv(TetrisEnv):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human', 'rgb_array'], 
                'obs_type': ['image', 'grid']}

    def __init__(self, gridchoice="none", obs_type="image", mode="rgb_array"):
        super(TetrisSingleEnv, self).__init__(TetrisSingleInterface, gridchoice, obs_type, mode)

    def step(self, action):
        # Execute one time step within the environment

        ob, reward, end, infos = self.game_interface.act(action)

        # if 'height_sum' in infos:
        #     # print(infos)
        #     reward -= infos['height_sum'] * 0.2

        self.accum_rewards += reward

        if end:
            infos['episode'] = {'r': self.accum_rewards}

        # if len(infos) != 0:
        #     reward += infos['height_sum'] / 50 / 1000

        #     reward -= infos['diff_sum'] / 40 / 1000

        #     reward -= infos['max_height'] / 30 / 1000

        #     reward -= infos['holes'] / 20 / 1000

        return ob, reward, end, infos

class TetrisDoubleEnv(TetrisEnv):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human', 'rgb_array'], 
                'obs_type': ['image', 'grid']}

    def __init__(self, gridchoice="none", obs_type="image", mode="rgb_array"):
        super(TetrisDoubleEnv, self).__init__(TetrisDoubleInterface, gridchoice, obs_type, mode)
  
    def step(self, action):
        # Execute one time step within the environment

        ob, reward, end, infos = self.game_interface.act(action)

        # if len(infos) != 0:
        #     reward += infos['height_sum'] / 50 / 1000

        #     reward -= infos['diff_sum'] / 40 / 1000

        #     reward -= infos['max_height'] / 30 / 1000

        #     reward -= infos['holes'] / 20 / 1000

        return ob, reward, end, infos

if __name__ == "__main__":

    import time

    env = TetrisSingleEnv(gridchoice="none", obs_type="grid", mode="human")

    ob = env.reset()
    
    start = time.time()

    last = 0
    for i in range(200000):

        # if i % 5 == 0:
        #     env.take_turns()
        #     action = env.random_action()
        # else:
        #     action = 0
        env.take_turns()
        action = env.random_action()
        # if i % 2 == 0:
        #     action = 2
        # else:
        #     action = 0
        ob, reward, done, infos = env.step(action)
        # print(ob)
        # print(reward)
        if len(infos) != 0:
            print(infos)
        
        # im = Image.fromarray(ob)
        # im.save("samples/%d.png" % i)
        if done:
            print(time.time() - start)
            print(i)
            print("avg number for loop per second: ", (i - last) / (time.time() - start))
            start = time.time()
            last = i

            # exit()
            ob = env.reset()