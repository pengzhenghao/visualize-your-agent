from setuptools import setup

setup(
    name="visya",
    version="0.0.1",
    author="pengzhenghao",
    author_email="pengzh@ie.cuhk.edu.hk",
    packages=['visya'],
    install_requires=[
        "yapf==0.27",
        "gym==0.17.2",
        "gym[box2d]",
        "opencv-python"
    ]
)
