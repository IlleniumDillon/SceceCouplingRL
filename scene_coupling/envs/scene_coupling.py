import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

import Simulation

import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces


class SceneCouplingEnv(gym.Env):
    def __init__(self, *, sceneFile:str, puzzleFile:str) -> None:
        super().__init__()