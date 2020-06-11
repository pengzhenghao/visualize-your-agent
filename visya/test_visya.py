import os

import numpy as np

from visya import rollout, generate_gif, generate_mp4

if __name__ == '__main__':
    episode = rollout(lambda x: np.random.randint(2), "CartPole-v0")
    generate_gif(episode.frames, "deleteme.gif")
    generate_mp4(episode.frames, "deleteme.mp4")
    episode.env.close()
    os.remove("deleteme.gif")
    os.remove("deleteme.mp4")
