import numpy as np
import gym
from gym import spaces
from gym import utils
from gym.utils import seeding

from tetris import TetrisSingleInterface

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
        # action = 3
        ob, reward, done, infos = env.step(action)
        # print(ob)
        if len(infos) != 0:
            print(infos)
        # im = Image.fromarray(ob)
        # im.save("samples/%d.png" % i)
        if done:
            print(time.time() - start)
            print(i)
            # exit()
            ob = env.reset()



