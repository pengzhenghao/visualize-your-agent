from __future__ import absolute_import, division, print_function

import logging
import time
from collections import namedtuple

import gym
import numpy as np

RolloutResult = namedtuple(
    "RolloutResult", ["episode_reward", "episode_length", "frames", "env"]
)

logger = logging.getLogger(__name__)

LOG_INTERVAL_STEPS = 1000


def rollout(compute_action, env, num_steps=1000, close_env=False):
    # Check environment
    if isinstance(env, str):
        logging.info("Use default gym environment for you.")
        env = gym.make(env)
    assert isinstance(env, gym.Env)

    # Setup variable
    steps = 0
    start = now = time.time()
    frames = []
    ep_reward = 0.0
    done = False
    obs = env.reset()

    # Collect one episode
    while not done and steps < (num_steps or steps + 1):
        if steps % LOG_INTERVAL_STEPS == (LOG_INTERVAL_STEPS - 1):
            logging.info(
                "Current Steps: {}, Time Elapsed: {:.2f}s, "
                "Last {} Steps Time: {:.2f}s".format(
                    steps,
                    time.time() - start, LOG_INTERVAL_STEPS,
                    time.time() - now
                )
            )
            now = time.time()
        action = compute_action(obs)
        next_obs, reward, done, _ = env.step(action)
        kwargs = {"mode": "rgb_array"}
        frame = env.render(**kwargs).copy()
        frames.append(frame)
        ep_reward += reward
        obs = next_obs
        steps += 1
    info = RolloutResult(
        episode_reward=ep_reward,
        episode_length=steps,
        frames=np.array(frames),
        env=env
    )
    if close_env:
        info.env = None
        env.close()
    return info


if __name__ == '__main__':
    result = rollout(lambda x: 0, "CartPole-v0")
    result.env.close()
