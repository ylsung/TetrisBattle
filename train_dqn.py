from TetrisBattle.envs.tetris_env import TetrisSingleEnv

import gym
import numpy as np

import pickle
from stable_baselines.deepq.policies import MlpPolicy, CnnPolicy
from stable_baselines import DQN
from stable_baselines.common import make_vec_env
from stable_baselines.common.callbacks import BaseCallback
from stable_baselines.bench import Monitor
from stable_baselines.common.noise import AdaptiveParamNoiseSpec
import os

CASE_NAME = 'tetris_dqn'

class SaveOnBestTrainingRewardCallback(BaseCallback):
    """
    Callback for saving a model (the check is done every ``check_freq`` steps)
    based on the training reward (in practice, we recommend using ``EvalCallback``).

    :param check_freq: (int)
    :param log_dir: (str) Path to the folder where the model will be saved.
      It must contains the file created by the ``Monitor`` wrapper.
    :param verbose: (int)
    """
    def __init__(self, check_freq: int, log_dir: str, verbose=1):
        super(SaveOnBestTrainingRewardCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.log_dir = log_dir
        self.save_path = os.path.join(log_dir, CASE_NAME)
        self.best_mean_reward = -np.inf

    def _init_callback(self) -> None:
        # Create folder if needed
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:
            tmp_path = os.path.join(self.save_path, "%d.pkl" % self.n_calls)
            with open(tmp_path, 'wb') as outfile:
                params = self.model.get_parameters()
                pickle.dump(params, outfile)
            tmp_path = os.path.join(self.save_path, "%d" % self.n_calls)
            self.model.save(tmp_path)
            if self.verbose > 0:
            	print("Saving {}th model to {}".format(self.n_calls, tmp_path))

        return True


# Create log dir
log_dir = "tmp/"
os.makedirs(log_dir, exist_ok=True)

env = make_vec_env(TetrisSingleEnv, n_envs=1, env_kwargs={"gridchoice": "none", "obs_type": "grid", "mode": "rgb_array"})

# Create the callback: check every 1000 steps
callback = SaveOnBestTrainingRewardCallback(check_freq=10000, log_dir=log_dir)
# Train the agent
time_steps = 1e12
model = DQN(MlpPolicy, env, verbose=1, tensorboard_log="./dqn_%s_tensorboard/" % CASE_NAME)

load_steps = 0

if load_steps > 0:
    tmp_path = os.path.join('./tmp/%s' % CASE_NAME, "%d" % load_steps)
    del model

    model = DQN.load(tmp_path, learning_rate=0.00025, env=env, verbose=1, tensorboard_log="./dqn_%s_tensorboard/" % CASE_NAME)
    model.num_timesteps = load_steps

model.learn(total_timesteps=int(time_steps), callback=callback)
model.save("dqn_%s" % CASE_NAME)

del model # remove to demonstrate saving and loading

model = DQN.load("dqn_%s" % CASE_NAME)

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
