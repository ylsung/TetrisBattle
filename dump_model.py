from TetrisBattle.envs.tetris_env import TetrisSingleEnv

import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines import PPO2
from stable_baselines.common import make_vec_env

import pickle

env = make_vec_env(TetrisSingleEnv, n_envs=1, env_kwargs={"gridchoice": "none", "obs_type": "grid", "mode": "rgb_array"})

model = PPO2.load("tmp/best_model/236000.zip", env=env)

params = model.get_parameters()

print(params)

with open('./tmp/best_model/236000.pkl', 'wb') as outfile:
    pickle.dump(params, outfile)

#obs = env.reset()
#while True:
#    action, _states = model.predict(obs)
#    obs, rewards, dones, info = env.step(action)
#    env.render()
