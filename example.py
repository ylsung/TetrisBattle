from TetrisBattle.envs.tetris_env import TetrisSingleEnv
import time
import numpy as np

np.set_printoptions(precision=1)

if __name__ == "__main__":

    env = TetrisSingleEnv(gridchoice="comboking", obs_type="grid", mode="rgb_array")

    ob = env.reset()

    for i in range(200000):

        env.take_turns() # take_turn() only work in double mode
        action = env.random_action()

        ob, reward, done, infos = env.step(action)

        # print(reward)
        print(np.array(ob[200:]).reshape(-1, 18)[:20, :10])
        # if len(infos) != 0:
            # print(infos)
        time.sleep(0.33)

        if done:
            ob = env.reset()
