from TetrisBattle.envs.tetris_env import TetrisSingleEnv

import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines import PPO1

env = TetrisSingleEnv(gridchoice="none", obs_type="image", mode="rgb_array")

model = PPO1(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=25000)
model.save("ppo1_cartpole")

del model # remove to demonstrate saving and loading

model = PPO1.load("ppo1_cartpole")

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
