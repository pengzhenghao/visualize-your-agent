# Visualize Your Agent!

Hi there! This repository provides a light interface to generate video and animation for arbitrary agent in arbitrary environment.

## Installation

```bash
git clone https://github.com/pengzhenghao/visualize-your-agent.git
cd visualize-your-agent
pip install -e .
```

## Usages

```python
from visya import rollout, generate_gif, generate_mp4

episode = rollout(lambda x: np.random.randint(2), "CartPole-v0")
generate_gif(episode.frames, "random_agent.gif")
generate_mp4(episode.frames, "random_agent.mp4")
```