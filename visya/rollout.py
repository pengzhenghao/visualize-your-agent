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


def get_best_rollout(compute_action, env, num_episodes=3, num_steps=1000,
                     return_all=False, close_env=False, render_kwargs=None,
                     seed_start=0):
    print("We will return the best one in {} episodes.".format(num_episodes))
    result_list = []
    for ep in range(num_episodes):
        result = rollout(compute_action, env, num_steps, 100 * ep + seed_start,
                         close_env, render_kwargs)
        result_list.append(result)
        print("Finished {}/{} episodes.".format(ep + 1, num_episodes))
    if return_all:
        return result_list
    return max(result_list, key=lambda i: i.episode_reward)


def rollout(compute_action, env, num_steps=1000, seed=0, close_env=False,
            render_kwargs=None):
    # Check environment
    if isinstance(env, str):
        logging.info("Use default gym environment for you.")
        env = gym.make(env)
    assert isinstance(env, gym.Env)

    env.seed(seed)

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
        if render_kwargs is not None:
            kwargs.update(render_kwargs)
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
