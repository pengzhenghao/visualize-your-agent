"""
This is the main entrance of this package.
First, initialize the policy and environment.
Second, rollout for episodes.
Third, generate video or animation for a given episode.
"""
import copy

from PIL import Image

from visya.visualize_utils import _check_frames, ImageEncoder, _check_path


def generate_gif(frames, path, fps=50):
    _check_frames(frames)
    _check_path(path, ".gif")
    duration = int(1 / fps * 1000)
    frames = copy.deepcopy(frames)
    images = [Image.fromarray(frame) for frame in frames]
    images[0].save(
        path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )
    return path


def generate_video(frames, path, fps=50):
    _check_frames(frames)
    _check_path(path, ".mp4")
    encoder = ImageEncoder(path, frames[0].shape, fps)
    for frame in frames:
        encoder.capture_frame(frame)
    encoder.close()
    return path
