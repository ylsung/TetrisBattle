from TetrisBattle.envs.tetris_env import TetrisSingleEnv

import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines import PPO2
from stable_baselines.common import make_vec_env

import pickle
import numpy as np
import time
import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0" #(or "1" or "2")

np.set_printoptions(edgeitems=30, linewidth=20000, 
    formatter=dict(float=lambda x: "%3.1g" % x))

env = make_vec_env(TetrisSingleEnv, n_envs=1, env_kwargs={"gridchoice": "none", "obs_type": "grid", "mode": "rgb_array"})

model = PPO2(MlpPolicy, env, verbose=1)

with open('./tmp/tetris_only_core_with_suggestion/830000.pkl', 'rb') as outfile:
    params = pickle.load(outfile)
    # print(params)

    model.load_parameters(params)

action_meaning = {
    0: "NOOP",
    1: "hold",
    2: "drop",
    3: "rotate_right",
    4: "rotate_left",
    5: "right",
    6: "left",
    7: "down"
}

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    
    # print(np.array(obs[0][360:]).reshape(-1, 18)[:20, :10])

    print(action_meaning[action[0]])
    time.sleep(1/60 * 10)
    
    if dones[0]:
        print("///")
        print("///")
        print("///")
        print("///")
        print("///")
        print("///")
        print("///")
        time.sleep(5)
        env.reset()
    else:
        print(np.array(obs[0][360:]).reshape(-1, 18))
    # env.render()
