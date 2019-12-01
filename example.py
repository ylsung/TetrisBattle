from TetrisBattle.envs.tetris_single_env import TetrisSingleEnv


if __name__ == "__main__":

    env = TetrisSingleEnv(gridchoice="none", obs_type="grid", mode="rgb_array")

    ob = env.reset()

    for i in range(200000):

        env.take_turns() # take_turn() only work in double mode
        action = env.random_action()

        ob, reward, done, infos = env.step(action)

        print(reward)

        if len(infos) != 0:
            print(infos)

        if done:
            ob = env.reset()